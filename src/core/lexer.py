"""
LumaScript Lexer - Converts source code into tokens
"""
from dataclasses import dataclass
from typing import List, Optional
import re

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

class Lexer:
    # Token types
    KEYWORDS = {
        'func': 'FUNCTION',
        'return': 'RETURN',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'let': 'LET',
        'i32': 'TYPE',
        'i64': 'TYPE',
        'f32': 'TYPE',
        'f64': 'TYPE',
        'alloc': 'ALLOC',      # Memory allocation
        'free': 'FREE',        # Memory deallocation
        'sizeof': 'SIZEOF',    # Size of type
        'ptr': 'PTR',         # Pointer type
        'ref': 'REF',         # Reference operator
        'deref': 'DEREF',      # Dereference operator
        'string': 'TYPE',      # String type
        'len': 'LEN',         # String length
        'concat': 'CONCAT',   # String concatenation
        'substr': 'SUBSTR'    # Substring operation
    }
    
    OPERATORS = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULTIPLY',
        '/': 'DIVIDE',
        '=': 'ASSIGN',
        '==': 'EQUALS',
        '<': 'LESS',
        '>': 'GREATER',
        '<=': 'LESS_EQUAL',
        '>=': 'GREATER_EQUAL',
        '(': 'LPAREN',
        ')': 'RPAREN',
        '{': 'LBRACE',
        '}': 'RBRACE',
        ':': 'COLON',
        ';': 'SEMICOLON',
        ',': 'COMMA',
        '->': 'ARROW',
        '+=': 'PLUS_ASSIGN',
        '-=': 'MINUS_ASSIGN',
        '*=': 'MULTIPLY_ASSIGN',
        '/=': 'DIVIDE_ASSIGN',
        '&': 'ADDRESS_OF',     # Get address
        '@': 'DEREFERENCE',    # Dereference pointer
        '.': 'DOT'            # Member access
    }

    def __init__(self):
        self.source = ""
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = None

    def init(self, source: str):
        """Initialize lexer with source code"""
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source else None

    def advance(self):
        """Move to next character"""
        self.pos += 1
        if self.pos > len(self.source) - 1:
            self.current_char = None
        else:
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current_char = self.source[self.pos]

    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        """Skip single-line comments"""
        while self.current_char and self.current_char != '\n':
            self.advance()

    def number(self) -> Token:
        """Parse a number token"""
        result = ''
        start_column = self.column
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()

        if '.' in result:
            return Token('FLOAT', float(result), self.line, start_column)
        return Token('INTEGER', int(result), self.line, start_column)

    def identifier(self) -> Token:
        """Parse an identifier or keyword token"""
        result = ''
        start_column = self.column
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        token_type = self.KEYWORDS.get(result, 'IDENTIFIER')
        return Token(token_type, result, self.line, start_column)

    def operator(self) -> Optional[Token]:
        """Parse an operator token"""
        if not self.current_char:
            return None
            
        start_column = self.column
        if self.current_char == '/' and self.peek() == '/':
            self.advance()
            self.advance()
            self.skip_comment()
            return None

        # Check for two-character operators
        if self.current_char + (self.peek() or '') in self.OPERATORS:
            op = self.current_char + self.peek()
            self.advance()
            self.advance()
            return Token(self.OPERATORS[op], op, self.line, start_column)

        # Single-character operators
        if self.current_char in self.OPERATORS:
            op = self.current_char
            self.advance()
            return Token(self.OPERATORS[op], op, self.line, start_column)

        return None

    def peek(self) -> Optional[str]:
        """Look at the next character without advancing"""
        peek_pos = self.pos + 1
        if peek_pos > len(self.source) - 1:
            return None
        return self.source[peek_pos]

    def string_literal(self) -> Token:
        """Parse a string literal"""
        result = ''
        start_column = self.column
        
        # Skip opening quote
        self.advance()
        
        while self.current_char and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == '"':
                    result += '"'
                elif self.current_char == '\\':
                    result += '\\'
                else:
                    raise SyntaxError(
                        f"Invalid escape sequence '\\{self.current_char}' at line {self.line}, column {self.column}"
                    )
            else:
                result += self.current_char
            self.advance()
            
        if not self.current_char:
            raise SyntaxError(
                f"Unterminated string at line {self.line}, column {start_column}"
            )
            
        # Skip closing quote
        self.advance()
        
        return Token('STRING', result, self.line, start_column)

    def tokenize(self, source: str) -> List[Token]:
        """Convert source code to list of tokens"""
        self.init(source)
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                tokens.append(self.number())
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.identifier())
                continue

            if self.current_char == '"':
                tokens.append(self.string_literal())
                continue

            op_token = self.operator()
            if op_token:
                tokens.append(op_token)
                continue

            raise SyntaxError(
                f"Invalid character '{self.current_char}' at line {self.line}, column {self.column}"
            )

        tokens.append(Token('EOF', '', self.line, self.column))
        return tokens 