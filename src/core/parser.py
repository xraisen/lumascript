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
    statements: List['Statement']

@dataclass
class Statement(Node):
    """Base class for statements"""
    pass

@dataclass
class ReturnStatement(Statement):
    """Return statement"""
    expression: 'Expression'

@dataclass
class IfStatement(Statement):
    """If statement"""
    condition: 'Expression'
    then_block: Block
    else_block: Optional[Block] = None

@dataclass
class WhileStatement(Statement):
    """While loop statement"""
    condition: 'Expression'
    body: Block

@dataclass
class LetStatement(Statement):
    """Variable declaration statement"""
    name: str
    type: str
    initializer: 'Expression'

@dataclass
class AssignStatement(Statement):
    """Variable assignment statement"""
    name: str
    operator: str  # '=', '+=', '-=', '*=', '/='
    value: 'Expression'

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

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

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

    def statement(self) -> Statement:
        """Parse a statement"""
        if self.match('RETURN'):
            return self.return_statement()
        if self.match('IF'):
            return self.if_statement()
        if self.match('WHILE'):
            return self.while_statement()
        if self.match('LET'):
            return self.let_statement()
        if self.match('IDENTIFIER'):
            return self.assignment_statement()
        raise SyntaxError(f"Unexpected token {self.peek().type}")

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

    def expression(self) -> Expression:
        """Parse an expression"""
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
            
        if self.match('IDENTIFIER'):
            return Identifier(self.previous().value)
            
        raise SyntaxError(f"Expect expression, got {self.peek().type}")

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