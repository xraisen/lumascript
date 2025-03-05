import os
import subprocess
from pathlib import Path

def compile_wasm():
    """Compile C code to WASM using emcc"""
    try:
        # Get the directory of this script
        script_dir = Path(__file__).parent.absolute()
        
        # Input and output paths
        input_file = script_dir / "operations.c"
        output_file = script_dir / "operations.wasm"
        
        # Compile command
        cmd = [
            "emcc",
            str(input_file),
            "-o", str(output_file),
            "-s", "WASM=1",
            "-s", "EXPORTED_FUNCTIONS=['_add','_subtract','_multiply','_divide','_equals','_less_than']",
            "-s", "EXPORTED_RUNTIME_METHODS=['ccall','cwrap']"
        ]
        
        # Run compilation
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Compilation failed:")
            print(result.stderr)
            return False
            
        print("Successfully compiled to WASM")
        return True
        
    except Exception as e:
        print(f"Error compiling to WASM: {e}")
        return False

def test_wasm():
    """Test the compiled WASM module"""
    try:
        import wasmtime
        
        # Get the directory of this script
        script_dir = Path(__file__).parent.absolute()
        wasm_file = script_dir / "operations.wasm"
        
        # Load the WASM module
        store = wasmtime.Store()
        module = wasmtime.Module.from_file(store.engine, str(wasm_file))
        instance = wasmtime.Instance(store, module, [])
        
        # Test each operation
        tests = [
            ("add", 5, 3, 8),
            ("subtract", 10, 4, 6),
            ("multiply", 6, 7, 42),
            ("divide", 15, 3, 5),
            ("equals", 5, 5, 1),
            ("less_than", 3, 5, 1)
        ]
        
        for func_name, a, b, expected in tests:
            func = instance.exports(store)[func_name]
            result = func(store, a, b)
            print(f"{func_name}({a}, {b}) = {result} {'✓' if result == expected else '✗'}")
            
    except Exception as e:
        print(f"Error testing WASM: {e}")

if __name__ == "__main__":
    if compile_wasm():
        test_wasm() 