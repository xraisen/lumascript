"""
Tests for LumaScript memory management features
"""
import pytest
from src.core.lexer import Lexer
from src.core.parser import Parser
from src.core.generator import WASMGenerator

def parse_source(source: str) -> bytes:
    """Helper function to parse source code into WASM binary"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    generator = WASMGenerator()
    return generator.generate(ast)

def test_memory_allocation():
    """Test memory allocation"""
    source = """
    function allocate_array(size: i32) -> i32 {
        let ptr = alloc(i32, size);
        return ptr;
    }
    """
    wasm = parse_source(source)
    assert wasm is not None
    # Verify memory section exists
    assert bytes([0x05]) in wasm  # Memory section ID

def test_memory_deallocation():
    """Test memory deallocation"""
    source = """
    function deallocate(ptr: i32) -> i32 {
        free(ptr);
        return 0;
    }
    """
    wasm = parse_source(source)
    assert wasm is not None

def test_sizeof_operator():
    """Test sizeof operator"""
    source = """
    function get_type_size() -> i32 {
        return sizeof(i32);
    }
    """
    wasm = parse_source(source)
    assert wasm is not None
    # Verify i32.const 4 instruction exists (size of i32)
    assert bytes([0x41, 0x04]) in wasm

def test_pointer_operations():
    """Test pointer operations"""
    source = """
    function pointer_ops(x: i32) -> i32 {
        let ptr = &x;
        let val = @ptr;
        return val;
    }
    """
    wasm = parse_source(source)
    assert wasm is not None

def test_array_operations():
    """Test array operations with pointers"""
    source = """
    function array_sum(arr: ptr<i32>, size: i32) -> i32 {
        let sum = 0;
        let i = 0;
        while (i < size) {
            sum += @(arr + i);
            i += 1;
        }
        return sum;
    }
    """
    wasm = parse_source(source)
    assert wasm is not None

def test_memory_error_handling():
    """Test memory error handling"""
    with pytest.raises(ValueError):
        parse_source("""
        function invalid_free() {
            free(123);  # Can't free a literal
        }
        """)

def test_complex_memory_operations():
    """Test complex memory operations"""
    source = """
    function matrix_alloc(rows: i32, cols: i32) -> ptr<i32> {
        let size = rows * cols;
        let matrix = alloc(i32, size);
        return matrix;
    }

    function matrix_free(matrix: ptr<i32>) {
        free(matrix);
    }

    function matrix_set(matrix: ptr<i32>, row: i32, col: i32, value: i32, cols: i32) {
        let index = row * cols + col;
        @(matrix + index) = value;
    }

    function matrix_get(matrix: ptr<i32>, row: i32, col: i32, cols: i32) -> i32 {
        let index = row * cols + col;
        return @(matrix + index);
    }
    """
    wasm = parse_source(source)
    assert wasm is not None 