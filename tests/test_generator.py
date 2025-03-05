"""
Tests for the LumaScript WASM generator
"""
import pytest
from src.core.lexer import Lexer
from src.core.parser import Parser
from src.core.generator import WASMGenerator

def compile_source(source: str) -> bytes:
    """Helper function to compile source code to WASM"""
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    generator = WASMGenerator()
    return generator.generate(ast)

def test_wasm_header():
    """Test WASM header generation"""
    wasm = compile_source("")
    # Check magic number and version
    assert wasm[:4] == b'\x00asm'
    assert wasm[4:8] == b'\x01\x00\x00\x00'

def test_simple_function():
    """Test generation of a simple function"""
    source = """
    func add(a: i32, b: i32) -> i32 {
        return a + b;
    }
    """
    wasm = compile_source(source)
    
    # Verify sections exist
    assert len(wasm) > 8  # Header size
    
    # Check for required sections
    section_ids = []
    pos = 8  # Skip header
    while pos < len(wasm):
        section_id = wasm[pos]
        section_ids.append(section_id)
        # Skip section id and size
        pos += 1
        size = 0
        shift = 0
        while True:
            byte = wasm[pos]
            pos += 1
            size |= (byte & 0x7f) << shift
            if not (byte & 0x80):
                break
            shift += 7
        pos += size
    
    # Verify required sections are present
    assert 1 in section_ids  # Type section
    assert 3 in section_ids  # Function section
    assert 7 in section_ids  # Export section
    assert 10 in section_ids  # Code section

def test_number_constant():
    """Test generation of number constant"""
    source = """
    func answer() -> i32 {
        return 42;
    }
    """
    wasm = compile_source(source)
    
    # Find code section
    pos = 8  # Skip header
    while pos < len(wasm):
        if wasm[pos] == 10:  # Code section
            pos += 1  # Skip section id
            # Skip section size
            while wasm[pos] & 0x80:
                pos += 1
            pos += 1
            # Skip vector count
            while wasm[pos] & 0x80:
                pos += 1
            pos += 1
            # Skip function body size
            while wasm[pos] & 0x80:
                pos += 1
            pos += 1
            # Skip locals count
            while wasm[pos] & 0x80:
                pos += 1
            pos += 1
            # Now at instruction stream
            assert wasm[pos] == 0x41  # i32.const
            break
    
    assert pos < len(wasm)  # Found the instruction

def test_binary_operations():
    """Test generation of binary operations"""
    source = """
    func calc(x: i32, y: i32) -> i32 {
        return x * y + 1;
    }
    """
    wasm = compile_source(source)
    
    # Find code section (similar to above)
    pos = 8
    while pos < len(wasm) and wasm[pos] != 10:
        pos += 1
        while pos < len(wasm) and wasm[pos] & 0x80:
            pos += 1
        pos += 1
    
    assert pos < len(wasm)  # Found code section
    
    # Verify multiplication and addition opcodes exist
    code_bytes = wasm[pos:]
    assert bytes([0x6C]) in code_bytes  # i32.mul
    assert bytes([0x6A]) in code_bytes  # i32.add

def test_multiple_functions():
    """Test generation of multiple functions"""
    source = """
    func add(a: i32, b: i32) -> i32 {
        return a + b;
    }
    func sub(a: i32, b: i32) -> i32 {
        return a - b;
    }
    """
    wasm = compile_source(source)
    
    # Find export section
    pos = 8
    while pos < len(wasm) and wasm[pos] != 7:  # Export section
        pos += 1
        while pos < len(wasm) and wasm[pos] & 0x80:
            pos += 1
        pos += 1
    
    assert pos < len(wasm)  # Found export section
    
    # Skip section id and size
    pos += 1
    while wasm[pos] & 0x80:
        pos += 1
    pos += 1
    
    # Check number of exports
    count = 0
    while wasm[pos] & 0x80:
        count |= (wasm[pos] & 0x7f)
        pos += 1
    count |= (wasm[pos] & 0x7f)
    
    assert count == 2  # Two exported functions

def test_error_handling():
    """Test generator error handling"""
    invalid_sources = [
        # Undefined variable
        """
        func test() -> i32 {
            return x;
        }
        """,
        # Invalid operator
        """
        func test(a: i32, b: i32) -> i32 {
            return a % b;
        }
        """
    ]
    
    for source in invalid_sources:
        with pytest.raises((ValueError, KeyError)):
            compile_source(source)

if __name__ == "__main__":
    pytest.main([__file__]) 