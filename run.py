import unittest
import sys
from examples.simple import main as run_simple_example
from examples.wasm_example import main as run_wasm_example
from tests.test_compiler import TestLumaCompiler

def run_tests():
    """Run all tests"""
    print("\nRunning tests...")
    unittest.main(verbosity=2)

def run_examples():
    """Run example programs"""
    print("\nRunning simple example...")
    run_simple_example()
    
    print("\nRunning WASM example...")
    run_wasm_example()

def main():
    """Main entry point"""
    print("LumaScript Compiler")
    print("==================")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            run_tests()
        elif sys.argv[1] == "--wasm":
            run_wasm_example()
        else:
            print("Usage: python run.py [--test|--wasm]")
            sys.exit(1)
    else:
        run_examples()

if __name__ == "__main__":
    main()