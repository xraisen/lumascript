"""
Test script for max.ls example program
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

def main():
    # Compile max.ls to WASM
    wasm_bytes = compile_file('examples/max.ls')
    
    # Save WASM binary for inspection
    with open('examples/max.wasm', 'wb') as f:
        f.write(wasm_bytes)
    
    # Create WASM runtime
    store = wasmtime.Store()
    module = wasmtime.Module(store.engine, wasm_bytes)
    instance = wasmtime.Instance(store, module, [])
    
    # Get exported functions
    max_func = instance.exports(store)["max"]
    is_positive = instance.exports(store)["is_positive"]
    abs_func = instance.exports(store)["abs"]
    
    # Test max function
    print("Testing max function:")
    test_cases = [(5, 3), (2, 7), (4, 4)]
    for a, b in test_cases:
        result = max_func(store, a, b)
        print(f"max({a}, {b}) = {result}")
        assert result == max(a, b)
    
    # Test is_positive function
    print("\nTesting is_positive function:")
    test_cases = [5, 0, -3]
    for x in test_cases:
        result = is_positive(store, x)
        print(f"is_positive({x}) = {result}")
        assert result == (1 if x > 0 else 0)
    
    # Test abs function
    print("\nTesting abs function:")
    test_cases = [5, 0, -3]
    for x in test_cases:
        result = abs_func(store, x)
        print(f"abs({x}) = {result}")
        assert result == abs(x)
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    main() 