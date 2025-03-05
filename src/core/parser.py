"""
LumaScript Parser - Converts tokens into an Abstract Syntax Tree (AST)
"""
from dataclasses import dataclass
from typing import List, Optional
from .lexer import Token

@dataclass
class Node:
    """Base class for AST nodes"""
    pass

@dataclass
class Program(Node):
    """Root node of the program"""
    functions: List['Function']

@dataclass
class Function(Node):
    """Function definition node"""
    name: str
    params: List['Parameter']
    return_type: str
    body: 'Block'

@dataclass
class Parameter(Node):
    """Function parameter node"""
    name: str
    type: str

@dataclass
class Block(Node):
    """Block of statements"""
    statements: List['Node']

@dataclass
class Statement(Node):
    """Base class for statements"""
    pass

@dataclass
class ReturnStatement(Statement):
    """Return statement"""
    expression: 'Node'

@dataclass
class IfStatement(Statement):
    """If statement"""
    condition: 'Node'
    then_block: Block
    else_block: Optional[Block]

@dataclass
class WhileStatement(Statement):
    """While loop statement"""
    condition: 'Node'
    body: Block

@dataclass
class LetStatement(Statement):
    """Variable declaration statement"""
    name: str
    type: str
    initializer: 'Node'

@dataclass
class AssignStatement(Statement):
    """Variable assignment statement"""
    name: str
    operator: str  # '=', '+=', '-=', '*=', '/='
    value: 'Node'

@dataclass
class Expression(Node):
    """Base class for expressions"""
    pass

@dataclass
class BinaryOp(Expression):
    """Binary operation"""
    operator: str
    left: Expression
    right: Expression

@dataclass
class Identifier(Expression):
    """Variable or function name"""
    name: str

@dataclass
class NumberLiteral(Expression):
    """Numeric literal"""
    value: float

@dataclass
class AllocExpression(Node):
    """Memory allocation expression"""
    type: str
    size: 'Node'

@dataclass
class FreeStatement(Node):
    """Memory deallocation statement"""
    pointer: 'Node'

@dataclass
class SizeofExpression(Node):
    """Sizeof expression"""
    type: str

@dataclass
class AddressOfExpression(Node):
    """Address-of expression"""
    expression: 'Node'

@dataclass
class DereferenceExpression(Node):
    """Dereference expression"""
    pointer: 'Node'

@dataclass
class PointerType(Node):
    """Pointer type node"""
    base_type: str

@dataclass
class StringLiteral(Expression):
    """String literal node"""
    value: str

@dataclass
class StringLength(Expression):
    """String length operation"""
    string: Expression

@dataclass
class StringConcat(Expression):
    """String concatenation"""
    left: Expression
    right: Expression

@dataclass
class Substring(Expression):
    """Substring operation"""
    string: Expression
    start: Expression
    length: Expression

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.types = {'i32', 'i64', 'f32', 'f64', 'ptr', 'string'}

    def parse(self) -> Program:
        """Parse the tokens into an AST"""
        functions = []
        while not self.is_at_end():
            functions.append(self.function())
        return Program(functions)

    def function(self) -> Function:
        """Parse a function definition"""
        self.consume('FUNCTION', "Expect 'func' keyword")
        name = self.consume('IDENTIFIER', "Expect function name").value
        
        self.consume('LPAREN', "Expect '(' after function name")
        params = []
        if not self.check('RPAREN'):
            params = self.parameters()
        self.consume('RPAREN', "Expect ')' after parameters")
        
        self.consume('ARROW', "Expect '->' before return type")
        return_type = self.consume('TYPE', "Expect return type").value
        
        self.consume('LBRACE', "Expect '{' before function body")
        body = self.block()
        self.consume('RBRACE', "Expect '}' after function body")
        
        return Function(name, params, return_type, body)

    def parameters(self) -> List[Parameter]:
        """Parse function parameters"""
        params = []
        
        while True:
            name = self.consume('IDENTIFIER', "Expect parameter name").value
            self.consume('COLON', "Expect ':' after parameter name")
            type_ = self.consume('TYPE', "Expect parameter type").value
            params.append(Parameter(name, type_))
            
            if not self.match('COMMA'):
                break
                
        return params

    def block(self) -> Block:
        """Parse a block of statements"""
        statements = []
        while not self.check('RBRACE') and not self.is_at_end():
            statements.append(self.statement())
        return Block(statements)

    def statement(self) -> Node:
        """Parse a statement"""
        if self.match('RETURN'):
            return self.return_statement()
        elif self.match('IF'):
            return self.if_statement()
        elif self.match('WHILE'):
            return self.while_statement()
        elif self.match('LET'):
            return self.let_statement()
        elif self.match('FREE'):
            return self.free_statement()
        elif self.check('IDENTIFIER'):
            return self.assignment_statement()
        else:
            return self.expression()

    def return_statement(self) -> ReturnStatement:
        """Parse a return statement"""
        value = self.expression()
        self.consume('SEMICOLON', "Expect ';' after return value")
        return ReturnStatement(value)

    def if_statement(self) -> IfStatement:
        """Parse an if statement"""
        self.consume('LPAREN', "Expect '(' after 'if'")
        condition = self.expression()
        self.consume('RPAREN', "Expect ')' after if condition")
        
        self.consume('LBRACE', "Expect '{' before then block")
        then_block = self.block()
        self.consume('RBRACE', "Expect '}' after then block")
        
        else_block = None
        if self.match('ELSE'):
            self.consume('LBRACE', "Expect '{' before else block")
            else_block = self.block()
            self.consume('RBRACE', "Expect '}' after else block")
        
        return IfStatement(condition, then_block, else_block)

    def while_statement(self) -> WhileStatement:
        """Parse a while statement"""
        self.consume('LPAREN', "Expect '(' after 'while'")
        condition = self.expression()
        self.consume('RPAREN', "Expect ')' after while condition")
        
        self.consume('LBRACE', "Expect '{' before while body")
        body = self.block()
        self.consume('RBRACE', "Expect '}' after while body")
        
        return WhileStatement(condition, body)

    def let_statement(self) -> LetStatement:
        """Parse a variable declaration"""
        name = self.consume('IDENTIFIER', "Expect variable name").value
        self.consume('COLON', "Expect ':' after variable name")
        type_ = self.consume('TYPE', "Expect variable type").value
        
        self.consume('ASSIGN', "Expect '=' after variable type")
        initializer = self.expression()
        self.consume('SEMICOLON', "Expect ';' after variable initializer")
        
        return LetStatement(name, type_, initializer)

    def assignment_statement(self) -> AssignStatement:
        """Parse a variable assignment"""
        name = self.previous().value
        
        # Check for compound assignment operators
        if self.match('PLUS_ASSIGN', 'MINUS_ASSIGN', 'MULTIPLY_ASSIGN', 'DIVIDE_ASSIGN'):
            operator = self.previous().value
        else:
            self.consume('ASSIGN', "Expect '=' after variable name")
            operator = '='
            
        value = self.expression()
        self.consume('SEMICOLON', "Expect ';' after assignment")
        
        return AssignStatement(name, operator, value)

    def expression(self) -> Node:
        """Parse an expression"""
        if self.match('ALLOC'):
            return self.alloc_expression()
        elif self.match('SIZEOF'):
            return self.sizeof_expression()
        elif self.match('ADDRESS_OF'):
            return self.address_of_expression()
        elif self.match('DEREFERENCE'):
            return self.dereference_expression()
        else:
            return self.comparison()

    def comparison(self) -> Expression:
        """Parse comparison expressions"""
        expr = self.addition()
        
        while self.match('LESS', 'GREATER', 'EQUALS', 'LESS_EQUAL', 'GREATER_EQUAL'):
            operator = self.previous().value
            right = self.addition()
            expr = BinaryOp(operator, expr, right)
            
        return expr

    def addition(self) -> Expression:
        """Parse addition and subtraction"""
        expr = self.multiplication()
        
        while self.match('PLUS', 'MINUS'):
            operator = self.previous().value
            right = self.multiplication()
            expr = BinaryOp(operator, expr, right)
            
        return expr

    def multiplication(self) -> Expression:
        """Parse multiplication and division"""
        expr = self.primary()
        
        while self.match('MULTIPLY', 'DIVIDE'):
            operator = self.previous().value
            right = self.primary()
            expr = BinaryOp(operator, expr, right)
            
        return expr

    def primary(self) -> Expression:
        """Parse primary expressions"""
        if self.match('INTEGER', 'FLOAT'):
            return NumberLiteral(float(self.previous().value))
            
        if self.match('STRING'):
            return StringLiteral(self.previous().value)
            
        if self.match('IDENTIFIER'):
            return Identifier(self.previous().value)
            
        if self.match('LEN'):
            self.consume('LPAREN', "Expected '(' after 'len'")
            expr = self.expression()
            self.consume('RPAREN', "Expected ')' after expression")
            return StringLength(expr)
            
        if self.match('CONCAT'):
            self.consume('LPAREN', "Expected '(' after 'concat'")
            left = self.expression()
            self.consume('COMMA', "Expected ',' after first string")
            right = self.expression()
            self.consume('RPAREN', "Expected ')' after second string")
            return StringConcat(left, right)
            
        if self.match('SUBSTR'):
            self.consume('LPAREN', "Expected '(' after 'substr'")
            string = self.expression()
            self.consume('COMMA', "Expected ',' after string")
            start = self.expression()
            self.consume('COMMA', "Expected ',' after start index")
            length = self.expression()
            self.consume('RPAREN', "Expected ')' after length")
            return Substring(string, start, length)
            
        raise SyntaxError(f"Expect expression, got {self.peek().type}")

    def alloc_expression(self) -> AllocExpression:
        """Parse memory allocation"""
        self.consume('LPAREN', "Expected '(' after 'alloc'")
        type_token = self.consume('TYPE', "Expected type in alloc expression")
        self.consume('COMMA', "Expected ',' after type")
        size = self.expression()
        self.consume('RPAREN', "Expected ')' after size")
        return AllocExpression(type_token.value, size)

    def free_statement(self) -> FreeStatement:
        """Parse memory deallocation"""
        self.consume('LPAREN', "Expected '(' after 'free'")
        pointer = self.expression()
        self.consume('RPAREN', "Expected ')' after pointer")
        self.consume('SEMICOLON', "Expected ';' after free statement")
        return FreeStatement(pointer)

    def sizeof_expression(self) -> SizeofExpression:
        """Parse sizeof expression"""
        self.consume('LPAREN', "Expected '(' after 'sizeof'")
        type_token = self.consume('TYPE', "Expected type in sizeof expression")
        self.consume('RPAREN', "Expected ')' after type")
        return SizeofExpression(type_token.value)

    def address_of_expression(self) -> AddressOfExpression:
        """Parse address-of expression"""
        expression = self.expression()
        return AddressOfExpression(expression)

    def dereference_expression(self) -> DereferenceExpression:
        """Parse dereference expression"""
        pointer = self.expression()
        return DereferenceExpression(pointer)

    def type_specifier(self) -> str:
        """Parse a type specifier"""
        if self.match('PTR'):
            self.consume('LESS', "Expected '<' after 'ptr'")
            base_type = self.consume('TYPE', "Expected base type").value
            self.consume('GREATER', "Expected '>' after base type")
            return f"ptr<{base_type}>"
        else:
            return self.consume('TYPE', "Expected type").value

    # Helper methods
    def match(self, *types) -> bool:
        """Check if current token matches any of the given types"""
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def check(self, type_: str) -> bool:
        """Check if current token is of given type"""
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self) -> Token:
        """Move to next token"""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        """Check if we've reached the end of tokens"""
        return self.peek().type == 'EOF'

    def peek(self) -> Token:
        """Look at current token"""
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Get previous token"""
        return self.tokens[self.current - 1]

    def consume(self, type_: str, message: str) -> Token:
        """Consume token of expected type or raise error"""
        if self.check(type_):
            return self.advance()
        raise SyntaxError(f"{message} at token {self.peek().type}") 