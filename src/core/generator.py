"""
LumaScript WASM Generator - Converts AST to WASM binary
"""
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from .parser import (
    Program, Function, Parameter, Block, ReturnStatement, IfStatement,
    WhileStatement, LetStatement, AssignStatement,
    BinaryOp, Identifier, NumberLiteral, Node
)

@dataclass
class WASMSection:
    """WASM section data"""
    id: int
    data: bytes

class WASMGenerator:
    # WASM section IDs
    TYPE_SECTION = 1
    FUNCTION_SECTION = 3
    MEMORY_SECTION = 5
    EXPORT_SECTION = 7
    CODE_SECTION = 10

    # WASM type encodings
    FUNC_TYPE = 0x60
    I32_TYPE = 0x7F
    I64_TYPE = 0x7E
    F32_TYPE = 0x7D
    F64_TYPE = 0x7C

    # WASM instructions
    I32_CONST = 0x41
    I32_ADD = 0x6A
    I32_SUB = 0x6B
    I32_MUL = 0x6C
    I32_DIV = 0x6D
    I32_LT = 0x48
    I32_GT = 0x4A
    I32_EQ = 0x46
    LOCAL_GET = 0x20
    LOCAL_SET = 0x21
    LOCAL_TEE = 0x22
    BLOCK = 0x02
    LOOP = 0x03
    IF = 0x04
    ELSE = 0x05
    BR = 0x0C
    BR_IF = 0x0D
    END = 0x0B

    def __init__(self):
        self.functions: List[Function] = []
        self.function_types: Dict[str, int] = {}  # Maps function signature to type index
        self.local_vars: Dict[str, int] = {}      # Maps variable names to local indices
        self.next_local_index: int = 0            # Next available local index

    def generate(self, ast: Program) -> bytes:
        """Generate WASM binary from AST"""
        self.functions = ast.functions
        
        # Generate sections
        type_section = self.generate_type_section()
        function_section = self.generate_function_section()
        export_section = self.generate_export_section()
        code_section = self.generate_code_section()
        
        # Combine sections
        wasm = (
            # Magic number and version
            bytes([0x00, 0x61, 0x73, 0x6D]) +  # \0asm
            bytes([0x01, 0x00, 0x00, 0x00]) +  # version 1
            # Sections
            self.encode_section(self.TYPE_SECTION, type_section) +
            self.encode_section(self.FUNCTION_SECTION, function_section) +
            self.encode_section(self.EXPORT_SECTION, export_section) +
            self.encode_section(self.CODE_SECTION, code_section)
        )
        
        return wasm

    def generate_type_section(self) -> bytes:
        """Generate type section containing function signatures"""
        types = []
        
        for func in self.functions:
            # Parameter types
            param_types = [self.get_wasm_type(param.type) for param in func.params]
            # Return type
            return_types = [self.get_wasm_type(func.return_type)]
            
            # Create function type
            func_type = (
                bytes([self.FUNC_TYPE]) +
                self.encode_vector(param_types) +
                self.encode_vector(return_types)
            )
            
            # Store type index
            signature = (tuple(param_types), tuple(return_types))
            if signature not in self.function_types:
                self.function_types[signature] = len(types)
                types.append(func_type)
        
        return self.encode_vector(types)

    def generate_function_section(self) -> bytes:
        """Generate function section containing type indices"""
        indices = []
        
        for func in self.functions:
            param_types = tuple(self.get_wasm_type(p.type) for p in func.params)
            return_types = tuple([self.get_wasm_type(func.return_type)])
            type_idx = self.function_types[(param_types, return_types)]
            indices.append(type_idx)
        
        return self.encode_vector([bytes([idx]) for idx in indices])

    def generate_export_section(self) -> bytes:
        """Generate export section for function exports"""
        exports = []
        
        for i, func in enumerate(self.functions):
            # Export name
            name_bytes = func.name.encode('utf-8')
            export = (
                self.encode_vector(name_bytes) +  # name
                bytes([0x00]) +                  # export kind (function)
                self.encode_unsigned_leb128(i)   # function index
            )
            exports.append(export)
        
        return self.encode_vector(exports)

    def generate_code_section(self) -> bytes:
        """Generate code section containing function bodies"""
        bodies = []
        
        for func in self.functions:
            # Reset local variables for each function
            self.local_vars = {}
            self.next_local_index = 0
            
            # Add parameters to local variables
            for param in func.params:
                self.local_vars[param.name] = self.next_local_index
                self.next_local_index += 1
            
            # Generate function body
            body = self.generate_function_body(func)
            bodies.append(body)
        
        return self.encode_vector(bodies)

    def generate_function_body(self, func: Function) -> bytes:
        """Generate code for a function body"""
        # Collect local variable declarations
        locals_count = 0
        for stmt in func.body.statements:
            if isinstance(stmt, LetStatement):
                self.local_vars[stmt.name] = self.next_local_index
                self.next_local_index += 1
                locals_count += 1
        
        # Encode local declarations (all i32 for now)
        locals = self.encode_vector([bytes([1, self.I32_TYPE]) for _ in range(locals_count)])
        
        # Function code
        code = bytearray()
        for stmt in func.body.statements:
            code.extend(self.generate_statement(stmt))
        code.append(self.END)
        
        # Combine locals and code
        body = locals + bytes(code)
        return self.encode_vector([body])

    def generate_statement(self, stmt: Node) -> bytes:
        """Generate code for a statement"""
        if isinstance(stmt, ReturnStatement):
            return self.generate_expression(stmt.expression)
            
        if isinstance(stmt, IfStatement):
            return self.generate_if_statement(stmt)
            
        if isinstance(stmt, WhileStatement):
            return self.generate_while_statement(stmt)
            
        if isinstance(stmt, LetStatement):
            return self.generate_let_statement(stmt)
            
        if isinstance(stmt, AssignStatement):
            return self.generate_assignment(stmt)
            
        raise ValueError(f"Unsupported statement type: {type(stmt)}")

    def generate_if_statement(self, stmt: IfStatement) -> bytes:
        """Generate code for an if statement"""
        code = bytearray()
        
        # Generate condition
        code.extend(self.generate_expression(stmt.condition))
        
        # If instruction with result type void (0x40)
        code.append(self.IF)
        code.append(0x40)
        
        # Then block
        for s in stmt.then_block.statements:
            code.extend(self.generate_statement(s))
        
        # Optional else block
        if stmt.else_block:
            code.append(self.ELSE)
            for s in stmt.else_block.statements:
                code.extend(self.generate_statement(s))
        
        code.append(self.END)
        return bytes(code)

    def generate_while_statement(self, stmt: WhileStatement) -> bytes:
        """Generate code for a while statement"""
        code = bytearray()
        
        # Block for break
        code.append(self.BLOCK)
        code.append(0x40)  # void type
        
        # Loop instruction
        code.append(self.LOOP)
        code.append(0x40)  # void type
        
        # Condition
        code.extend(self.generate_expression(stmt.condition))
        
        # Branch if zero (condition false)
        code.append(self.BR_IF)
        code.append(0x01)  # Break to outer block
        
        # Loop body
        for s in stmt.body.statements:
            code.extend(self.generate_statement(s))
        
        # Branch back to loop start
        code.append(self.BR)
        code.append(0x00)
        
        # End loop and block
        code.append(self.END)
        code.append(self.END)
        
        return bytes(code)

    def generate_let_statement(self, stmt: LetStatement) -> bytes:
        """Generate code for a variable declaration"""
        code = bytearray()
        
        # Generate initializer
        code.extend(self.generate_expression(stmt.initializer))
        
        # Store in local variable
        code.append(self.LOCAL_SET)
        code.append(self.local_vars[stmt.name])
        
        return bytes(code)

    def generate_assignment(self, stmt: AssignStatement) -> bytes:
        """Generate code for a variable assignment"""
        code = bytearray()
        
        if stmt.operator == '=':
            # Simple assignment
            code.extend(self.generate_expression(stmt.value))
            code.append(self.LOCAL_SET)
            code.append(self.local_vars[stmt.name])
        else:
            # Compound assignment (+=, -=, *=, /=)
            # Get current value
            code.append(self.LOCAL_GET)
            code.append(self.local_vars[stmt.name])
            
            # Get new value
            code.extend(self.generate_expression(stmt.value))
            
            # Apply operation
            op = stmt.operator[0]  # Get the operator without the =
            code.append(self.get_binary_op(op))
            
            # Store result
            code.append(self.LOCAL_SET)
            code.append(self.local_vars[stmt.name])
        
        return bytes(code)

    def generate_expression(self, expr: Node) -> bytes:
        """Generate code for an expression"""
        if isinstance(expr, NumberLiteral):
            return (
                bytes([self.I32_CONST]) +
                self.encode_signed_leb128(int(expr.value))
            )
            
        if isinstance(expr, Identifier):
            if expr.name not in self.local_vars:
                raise ValueError(f"Undefined variable: {expr.name}")
            return bytes([
                self.LOCAL_GET,
                self.local_vars[expr.name]
            ])
            
        if isinstance(expr, BinaryOp):
            code = bytearray()
            code.extend(self.generate_expression(expr.left))
            code.extend(self.generate_expression(expr.right))
            code.append(self.get_binary_op(expr.operator))
            return bytes(code)
            
        raise ValueError(f"Unsupported expression type: {type(expr)}")

    # Helper methods
    def get_wasm_type(self, type_str: str) -> int:
        """Convert type string to WASM type"""
        return {
            'i32': self.I32_TYPE,
            'i64': self.I64_TYPE,
            'f32': self.F32_TYPE,
            'f64': self.F64_TYPE,
        }[type_str]

    def get_binary_op(self, op: str) -> int:
        """Convert operator to WASM instruction"""
        return {
            '+': self.I32_ADD,
            '-': self.I32_SUB,
            '*': self.I32_MUL,
            '/': self.I32_DIV,
            '<': self.I32_LT,
            '>': self.I32_GT,
            '==': self.I32_EQ,
        }[op]

    def encode_section(self, section_id: int, content: bytes) -> bytes:
        """Encode a WASM section"""
        return bytes([section_id]) + self.encode_unsigned_leb128(len(content)) + content

    def encode_vector(self, items: List[bytes]) -> bytes:
        """Encode a vector of items"""
        content = b''.join(items)
        return self.encode_unsigned_leb128(len(items)) + content

    def encode_unsigned_leb128(self, value: int) -> bytes:
        """Encode an unsigned integer as LEB128"""
        result = bytearray()
        while True:
            byte = value & 0x7f
            value >>= 7
            if value:
                byte |= 0x80
            result.append(byte)
            if not value:
                break
        return bytes(result)

    def encode_signed_leb128(self, value: int) -> bytes:
        """Encode a signed integer as LEB128"""
        result = bytearray()
        while True:
            byte = value & 0x7f
            value >>= 7
            if (value == 0 and byte & 0x40 == 0) or (value == -1 and byte & 0x40):
                result.append(byte)
                break
            result.append(byte | 0x80)
        return bytes(result) 