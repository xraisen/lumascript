"""
Test script for fibonacci.ls example program
"""
from pathlib import Path
import wasmtime
from src.core.lexer import Lexer
from src.core.parser import Parser
from src.core.generator import WASMGenerator

def compile_file(source_path: str) -> bytes:
    """Compile a LumaScript file to WASM"""
    with open(source_path, 'r') as f:
        source = f.read()
    
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    generator = WASMGenerator()
    return generator.generate(ast)

def fibonacci_py(n: int) -> int:
    """Python implementation of fibonacci for comparison"""
    if n <= 1:
        return n
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

def sum_to_py(n: int) -> int:
    """Python implementation of sum_to for comparison"""
    return sum(range(1, n + 1))

def main():
    # Compile fibonacci.ls to WASM
    wasm_bytes = compile_file('examples/fibonacci.ls')
    
    # Save WASM binary for inspection
    with open('examples/fibonacci.wasm', 'wb') as f:
        f.write(wasm_bytes)
    
    # Create WASM runtime
    store = wasmtime.Store()
    module = wasmtime.Module(store.engine, wasm_bytes)
    instance = wasmtime.Instance(store, module, [])
    
    # Get exported functions
    fibonacci = instance.exports(store)["fibonacci"]
    sum_to = instance.exports(store)["sum_to"]
    
    # Test fibonacci function
    print("Testing fibonacci function:")
    test_cases = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for n in test_cases:
        result = fibonacci(store, n)
        expected = fibonacci_py(n)
        print(f"fibonacci({n}) = {result}")
        assert result == expected, f"Expected {expected}, got {result}"
    
    # Test sum_to function
    print("\nTesting sum_to function:")
    test_cases = [1, 2, 3, 4, 5, 10, 100]
    for n in test_cases:
        result = sum_to(store, n)
        expected = sum_to_py(n)
        print(f"sum_to({n}) = {result}")
        assert result == expected, f"Expected {expected}, got {result}"
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    main() 