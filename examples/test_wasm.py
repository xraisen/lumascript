from wasmtime import Store, Module, Instance
from src.utils.logger import Logger

def test_arithmetic(instance, store):
    """Test basic arithmetic operations"""
    logger = Logger(__name__)
    
    # Test addition
    add = instance.exports(store)["add"]
    result = add(store, 5, 3)
    logger.info(f"Addition: 5 + 3 = {result}")
    
    # Test subtraction
    sub = instance.exports(store)["sub"]
    result = sub(store, 10, 4)
    logger.info(f"Subtraction: 10 - 4 = {result}")
    
    # Test multiplication
    mul = instance.exports(store)["mul"]
    result = mul(store, 6, 7)
    logger.info(f"Multiplication: 6 * 7 = {result}")
    
    # Test division
    div = instance.exports(store)["div"]
    result = div(store, 15, 3)
    logger.info(f"Division: 15 / 3 = {result}")

def test_comparison(instance, store):
    """Test comparison operations"""
    logger = Logger(__name__)
    
    # Test equality
    eq = instance.exports(store)["eq"]
    result = eq(store, 5, 5)
    logger.info(f"Equality (5 == 5): {result}")
    result = eq(store, 5, 6)
    logger.info(f"Equality (5 == 6): {result}")
    
    # Test less than
    lt = instance.exports(store)["lt"]
    result = lt(store, 3, 5)
    logger.info(f"Less than (3 < 5): {result}")
    result = lt(store, 5, 3)
    logger.info(f"Less than (5 < 3): {result}")

def test_error_handling(instance, store):
    """Test error handling"""
    logger = Logger(__name__)
    
    try:
        # Test division by zero
        div = instance.exports(store)["div"]
        result = div(store, 10, 0)
    except Exception as e:
        logger.info(f"Division by zero caught: {e}")
    
    try:
        # Test invalid function call
        invalid = instance.exports(store)["invalid_func"]
        result = invalid(store)
    except Exception as e:
        logger.info(f"Invalid function call caught: {e}")

def main():
    logger = Logger(__name__)
    
    try:
        # Create a store
        store = Store()
        
        # Read the WASM binary
        with open("output.wasm", "rb") as f:
            wasm_bytes = f.read()
            
        # Create a module
        module = Module(store.engine, wasm_bytes)
        
        # Create an instance
        instance = Instance(store, module, [])
        
        # Run test suites
        logger.info("Running arithmetic tests...")
        test_arithmetic(instance, store)
        
        logger.info("Running comparison tests...")
        test_comparison(instance, store)
        
        logger.info("Running error handling tests...")
        test_error_handling(instance, store)
        
    except Exception as e:
        logger.error(f"Error running WASM: {e}")

if __name__ == "__main__":
    main() 