"""
Simple example demonstrating LumaScript compiler functionality.
This example shows how to:
1. Compile C code to WASM
2. Cache the compiled module
3. Execute the WASM function
"""

from pathlib import Path
from src.wasm.wasm_cache import WASMCache

def main():
    # Get the directory containing this script
    script_dir = Path(__file__).parent.absolute()
    
    # C source code for a simple add function
    c_source = """
    int add(int a, int b) {
        return a + b;
    }
    """
    
    # Save C source to file
    source_file = script_dir / "add.c"
    with open(source_file, "w") as f:
        f.write(c_source)
    
    try:
        # Initialize WASM cache
        cache = WASMCache()
        
        # Compile and get WASM instance
        instance = cache.get_instance(source_file)
        if not instance:
            print("Error: Could not get WASM instance")
            return
        
        # Get the add function
        store = instance.store
        add = instance.exports(store)["add"]
        
        # Test cases
        test_cases = [
            (5, 3),      # Basic addition
            (10, 20),    # Larger numbers
            (-5, 7),     # Negative number
            (0, 0),      # Zero case
            (999, 1)     # Large number
        ]
        
        # Run tests
        print("\nTesting WASM add function:")
        print("-" * 30)
        for a, b in test_cases:
            result = add(store, a, b)
            print(f"{a:4d} + {b:4d} = {result:4d}")
        print("-" * 30)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up source file
        if source_file.exists():
            source_file.unlink()

if __name__ == "__main__":
    main() 