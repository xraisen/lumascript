from typing import List, Dict, Any
import struct

class WASMEncoder:
    def __init__(self):
        self.position = 0
    
    def encode_module(self, sections: List[bytes]) -> bytes:
        """Encode complete WASM module"""
        # Magic number and version
        header = bytes([0x00, 0x61, 0x73, 0x6D,  # Magic number
                       0x01, 0x00, 0x00, 0x00])  # Version
        
        # Combine all sections
        return header + b''.join(sections)
    
    def encode_type_section(self, types: List[Dict[str, Any]]) -> bytes:
        """Encode type section"""
        # Section ID (1) and size
        section_id = bytes([0x01])
        content = self._encode_types(types)
        size = self._encode_leb128(len(content))
        
        return section_id + size + content
    
    def encode_function_section(self, indices: List[int]) -> bytes:
        """Encode function section"""
        # Section ID (3) and size
        section_id = bytes([0x03])
        content = self._encode_function_indices(indices)
        size = self._encode_leb128(len(content))
        
        return section_id + size + content
    
    def encode_export_section(self, exports: List[Dict[str, Any]]) -> bytes:
        """Encode export section"""
        # Section ID (7) and size
        section_id = bytes([0x07])
        content = self._encode_exports(exports)
        size = self._encode_leb128(len(content))
        
        return section_id + size + content
    
    def encode_code_section(self, bodies: List[Dict[str, Any]]) -> bytes:
        """Encode code section"""
        # Section ID (10) and size
        section_id = bytes([0x0A])
        content = self._encode_code_bodies(bodies)
        size = self._encode_leb128(len(content))
        
        return section_id + size + content
    
    def _encode_types(self, types: List[Dict[str, Any]]) -> bytes:
        """Encode type definitions"""
        count = self._encode_leb128(len(types))
        encoded_types = []
        
        for type_def in types:
            encoded_types.append(self._encode_type(type_def))
            
        return count + b''.join(encoded_types)
    
    def _encode_type(self, type_def: Dict[str, Any]) -> bytes:
        """Encode single type definition"""
        if type_def['form'] == 0x60:  # function type
            return self._encode_function_type(type_def)
        raise ValueError(f"Unknown type form: {type_def['form']}")
    
    def _encode_function_type(self, type_def: Dict[str, Any]) -> bytes:
        """Encode function type"""
        form = bytes([type_def['form']])
        param_count = self._encode_leb128(len(type_def['params']))
        params = b''.join(self._encode_value_type(t) for t in type_def['params'])
        result_count = self._encode_leb128(len(type_def['results']))
        results = b''.join(self._encode_value_type(t) for t in type_def['results'])
        
        return form + param_count + params + result_count + results
    
    def _encode_function_indices(self, indices: List[int]) -> bytes:
        """Encode function indices"""
        count = self._encode_leb128(len(indices))
        encoded_indices = b''.join(self._encode_leb128(i) for i in indices)
        return count + encoded_indices
    
    def _encode_exports(self, exports: List[Dict[str, Any]]) -> bytes:
        """Encode exports"""
        count = self._encode_leb128(len(exports))
        encoded_exports = []
        
        for export in exports:
            name = export['name'].encode('utf-8')
            name_len = self._encode_leb128(len(name))
            kind = bytes([export['kind']])
            index = self._encode_leb128(export['index'])
            encoded_exports.append(name_len + name + kind + index)
            
        return count + b''.join(encoded_exports)
    
    def _encode_code_bodies(self, bodies: List[Dict[str, Any]]) -> bytes:
        """Encode function bodies"""
        count = self._encode_leb128(len(bodies))
        encoded_bodies = []
        
        for body in bodies:
            encoded_bodies.append(self._encode_code_body(body))
            
        return count + b''.join(encoded_bodies)
    
    def _encode_code_body(self, body: Dict[str, Any]) -> bytes:
        """Encode single function body"""
        locals_count = self._encode_leb128(len(body['locals']))
        locals_ = b''.join(self._encode_local(l) for l in body['locals'])
        instructions = self._encode_instructions(body['instructions'])
        
        # Calculate total size
        content = locals_count + locals_ + instructions
        size = self._encode_leb128(len(content))
        
        return size + content
    
    def _encode_local(self, local: Dict[str, Any]) -> bytes:
        """Encode local variable"""
        count = self._encode_leb128(local['count'])
        type_ = self._encode_value_type(local['type'])
        return count + type_
    
    def _encode_instructions(self, instructions: List[Dict[str, Any]]) -> bytes:
        """Encode WASM instructions"""
        encoded = []
        for instr in instructions:
            encoded.append(self._encode_instruction(instr))
        return b''.join(encoded)
    
    def _encode_instruction(self, instruction: Dict[str, Any]) -> bytes:
        """Encode single instruction"""
        opcode = bytes([instruction['opcode']])
        operands = b''
        
        if 'operands' in instruction:
            operands = b''.join(self._encode_operand(o) for o in instruction['operands'])
            
        return opcode + operands
    
    def _encode_operand(self, operand: Any) -> bytes:
        """Encode instruction operand"""
        if isinstance(operand, int):
            return self._encode_leb128(operand)
        elif isinstance(operand, float):
            return struct.pack('<f', operand)  # 32-bit float
        elif isinstance(operand, str):
            return operand.encode('utf-8')
        raise ValueError(f"Unknown operand type: {type(operand)}")
    
    def _encode_value_type(self, type_: str) -> bytes:
        """Encode value type"""
        types = {
            'i32': 0x7F,
            'i64': 0x7E,
            'f32': 0x7D,
            'f64': 0x7C,
            'v128': 0x7B,
            'funcref': 0x70,
            'externref': 0x6F
        }
        return bytes([types.get(type_, 0x7F)])  # Default to i32 if unknown
    
    def _encode_leb128(self, value: int) -> bytes:
        """Encode LEB128 variable-length integer"""
        if value < 0:
            return self._encode_sleb128(value)
            
        result = bytearray()
        while True:
            byte = value & 0x7F
            value >>= 7
            if value == 0:
                result.append(byte)
                break
            result.append(byte | 0x80)
        return bytes(result)
    
    def _encode_sleb128(self, value: int) -> bytes:
        """Encode signed LEB128 variable-length integer"""
        result = bytearray()
        while True:
            byte = value & 0x7F
            value >>= 7
            if (value == 0 and not (byte & 0x40)) or (value == -1 and (byte & 0x40)):
                result.append(byte)
                break
            result.append(byte | 0x80)
        return bytes(result) 