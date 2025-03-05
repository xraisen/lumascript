from pathlib import Path
from wasm_cache import WASMCache

def main():
    try:
        # Get the directory of this script
        script_dir = Path(__file__).parent.absolute()
        source_file = script_dir / "add.c"
        
        # Initialize cache
        cache = WASMCache()
        
        # Get WASM instance from cache
        instance = cache.get_instance(source_file)
        if not instance:
            print("Error: Could not get WASM instance")
            return
            
        # Get the add function
        store = instance.store
        add = instance.exports(store)["add"]
        
        # Test the function
        test_cases = [
            (5, 3),
            (10, 20),
            (-5, 7),
            (0, 0)
        ]
        
        print("Testing WASM add function:")
        for a, b in test_cases:
            result = add(store, a, b)
            print(f"{a} + {b} = {result}")
        
    except Exception as e:
        print(f"Error testing WASM: {e}")

if __name__ == "__main__":
    main() 