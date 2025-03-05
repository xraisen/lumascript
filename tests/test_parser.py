"""
Tests for the LumaScript parser
"""
import pytest
from src.core.lexer import Lexer
from src.core.parser import Parser, Program, Function, Parameter, Block, ReturnStatement, IfStatement, BinaryOp, Identifier, NumberLiteral

def parse_source(source: str) -> Program:
    """Helper function to parse source code"""
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    parser = Parser(tokens)
    return parser.parse()

def test_empty_program():
    """Test parsing empty program"""
    ast = parse_source("")
    assert isinstance(ast, Program)
    assert len(ast.functions) == 0

def test_simple_function():
    """Test parsing simple function"""
    source = """
    func add(a: i32, b: i32) -> i32 {
        return a + b;
    }
    """
    ast = parse_source(source)
    
    assert isinstance(ast, Program)
    assert len(ast.functions) == 1
    
    func = ast.functions[0]
    assert isinstance(func, Function)
    assert func.name == "add"
    assert len(func.params) == 2
    assert func.return_type == "i32"
    
    # Check parameters
    assert func.params[0].name == "a"
    assert func.params[0].type == "i32"
    assert func.params[1].name == "b"
    assert func.params[1].type == "i32"
    
    # Check function body
    assert isinstance(func.body, Block)
    assert len(func.body.statements) == 1
    
    # Check return statement
    ret_stmt = func.body.statements[0]
    assert isinstance(ret_stmt, ReturnStatement)
    assert isinstance(ret_stmt.expression, BinaryOp)
    assert ret_stmt.expression.operator == "+"
    assert isinstance(ret_stmt.expression.left, Identifier)
    assert ret_stmt.expression.left.name == "a"
    assert isinstance(ret_stmt.expression.right, Identifier)
    assert ret_stmt.expression.right.name == "b"

def test_function_with_numbers():
    """Test parsing function with number literals"""
    source = """
    func answer() -> i32 {
        return 42;
    }
    """
    ast = parse_source(source)
    
    func = ast.functions[0]
    ret_stmt = func.body.statements[0]
    assert isinstance(ret_stmt.expression, NumberLiteral)
    assert ret_stmt.expression.value == 42

def test_complex_expression():
    """Test parsing complex expressions"""
    source = """
    func calc(x: i32) -> i32 {
        return 2 * x + 1;
    }
    """
    ast = parse_source(source)
    
    func = ast.functions[0]
    ret_stmt = func.body.statements[0]
    expr = ret_stmt.expression
    
    assert isinstance(expr, BinaryOp)
    assert expr.operator == "+"
    
    assert isinstance(expr.left, BinaryOp)
    assert expr.left.operator == "*"
    assert isinstance(expr.left.left, NumberLiteral)
    assert expr.left.left.value == 2
    assert isinstance(expr.left.right, Identifier)
    assert expr.left.right.name == "x"
    
    assert isinstance(expr.right, NumberLiteral)
    assert expr.right.value == 1

def test_multiple_functions():
    """Test parsing multiple functions"""
    source = """
    func add(a: i32, b: i32) -> i32 {
        return a + b;
    }
    func sub(a: i32, b: i32) -> i32 {
        return a - b;
    }
    """
    ast = parse_source(source)
    
    assert len(ast.functions) == 2
    assert ast.functions[0].name == "add"
    assert ast.functions[1].name == "sub"

def test_if_statement():
    """Test parsing if statements"""
    source = """
    func max(a: i32, b: i32) -> i32 {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }
    """
    ast = parse_source(source)
    
    func = ast.functions[0]
    if_stmt = func.body.statements[0]
    assert isinstance(if_stmt, IfStatement)
    
    # Check condition
    assert isinstance(if_stmt.condition, BinaryOp)
    assert if_stmt.condition.operator == ">"
    assert isinstance(if_stmt.condition.left, Identifier)
    assert if_stmt.condition.left.name == "a"
    assert isinstance(if_stmt.condition.right, Identifier)
    assert if_stmt.condition.right.name == "b"
    
    # Check then block
    assert isinstance(if_stmt.then_block, Block)
    assert len(if_stmt.then_block.statements) == 1
    assert isinstance(if_stmt.then_block.statements[0], ReturnStatement)
    assert isinstance(if_stmt.then_block.statements[0].expression, Identifier)
    assert if_stmt.then_block.statements[0].expression.name == "a"
    
    # Check else block
    assert isinstance(if_stmt.else_block, Block)
    assert len(if_stmt.else_block.statements) == 1
    assert isinstance(if_stmt.else_block.statements[0], ReturnStatement)
    assert isinstance(if_stmt.else_block.statements[0].expression, Identifier)
    assert if_stmt.else_block.statements[0].expression.name == "b"

def test_if_without_else():
    """Test parsing if statement without else block"""
    source = """
    func is_positive(x: i32) -> i32 {
        if (x > 0) {
            return 1;
        }
        return 0;
    }
    """
    ast = parse_source(source)
    
    func = ast.functions[0]
    if_stmt = func.body.statements[0]
    assert isinstance(if_stmt, IfStatement)
    assert if_stmt.else_block is None

def test_comparison_operators():
    """Test parsing comparison operators"""
    operators = {
        '<': 'LESS',
        '>': 'GREATER',
        '==': 'EQUALS'
    }
    
    for op_str, op_type in operators.items():
        source = f"""
        func compare(a: i32, b: i32) -> i32 {{
            return a {op_str} b;
        }}
        """
        ast = parse_source(source)
        
        func = ast.functions[0]
        ret_stmt = func.body.statements[0]
        expr = ret_stmt.expression
        
        assert isinstance(expr, BinaryOp)
        assert expr.operator == op_str

def test_syntax_errors():
    """Test parser error handling"""
    invalid_sources = [
        # Missing return type
        """
        func test(x: i32) {
            return x;
        }
        """,
        # Missing parameter type
        """
        func test(x) -> i32 {
            return x;
        }
        """,
        # Missing semicolon
        """
        func test() -> i32 {
            return 42
        }
        """,
        # Invalid if statement syntax
        """
        func test(x: i32) -> i32 {
            if x > 0 {
                return 1;
            }
        }
        """
    ]
    
    for source in invalid_sources:
        with pytest.raises(SyntaxError):
            parse_source(source)

if __name__ == "__main__":
    pytest.main([__file__]) 