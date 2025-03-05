"""
Tests for the LumaScript lexer
"""
import pytest
from src.core.lexer import Lexer, Token

def test_empty_source():
    """Test lexer with empty source"""
    lexer = Lexer()
    tokens = lexer.tokenize("")
    assert len(tokens) == 1
    assert tokens[0].type == 'EOF'

def test_simple_function():
    """Test lexing a simple function"""
    source = """
    func add(a: i32, b: i32) -> i32 {
        return a + b;
    }
    """
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    
    expected = [
        ('FUNCTION', 'func'),
        ('IDENTIFIER', 'add'),
        ('LPAREN', '('),
        ('IDENTIFIER', 'a'),
        ('COLON', ':'),
        ('TYPE', 'i32'),
        ('COMMA', ','),
        ('IDENTIFIER', 'b'),
        ('COLON', ':'),
        ('TYPE', 'i32'),
        ('RPAREN', ')'),
        ('ARROW', '->'),
        ('TYPE', 'i32'),
        ('LBRACE', '{'),
        ('RETURN', 'return'),
        ('IDENTIFIER', 'a'),
        ('PLUS', '+'),
        ('IDENTIFIER', 'b'),
        ('SEMICOLON', ';'),
        ('RBRACE', '}'),
        ('EOF', '')
    ]
    
    assert len(tokens) == len(expected)
    for token, (exp_type, exp_value) in zip(tokens, expected):
        assert token.type == exp_type
        assert str(token.value) == exp_value

def test_numbers():
    """Test lexing numbers"""
    source = "42 3.14"
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    
    assert len(tokens) == 3  # 2 numbers + EOF
    assert tokens[0].type == 'INTEGER'
    assert tokens[0].value == 42
    assert tokens[1].type == 'FLOAT'
    assert tokens[1].value == 3.14

def test_operators():
    """Test lexing operators"""
    source = "+ - * / = == < > -> ;"
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    
    expected = [
        'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE',
        'ASSIGN', 'EQUALS', 'LESS', 'GREATER',
        'ARROW', 'SEMICOLON', 'EOF'
    ]
    
    assert len(tokens) == len(expected)
    for token, exp_type in zip(tokens, expected):
        assert token.type == exp_type

def test_comments():
    """Test lexing with comments"""
    source = """
    // This is a comment
    func main() -> i32 {
        return 42; // Return value
    }
    """
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    
    # Comments should be ignored
    assert 'comment' not in [t.value for t in tokens]
    
    # Check function structure is preserved
    types = [t.type for t in tokens]
    assert 'FUNCTION' in types
    assert 'IDENTIFIER' in types
    assert 'INTEGER' in types
    assert 'RETURN' in types

def test_error_handling():
    """Test lexer error handling"""
    source = "func test() { @ }"  # Invalid character @
    lexer = Lexer()
    
    with pytest.raises(SyntaxError) as exc_info:
        lexer.tokenize(source)
    
    assert "Invalid character '@'" in str(exc_info.value)

def test_line_column_tracking():
    """Test line and column number tracking"""
    source = """
    func add(
        a: i32,
        b: i32
    ) -> i32
    """
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    
    # Check a few key positions
    func_token = next(t for t in tokens if t.type == 'FUNCTION')
    assert func_token.line == 2
    
    first_i32_token = next(t for t in tokens if t.type == 'TYPE')
    assert first_i32_token.line == 3

if __name__ == "__main__":
    pytest.main([__file__]) 