import unittest
from src.core.compiler import LumaCompiler
from src.utils.logger import Logger

class TestLumaCompiler(unittest.TestCase):
    def setUp(self):
        self.compiler = LumaCompiler()
        self.logger = Logger(__name__)

    def test_basic_function(self):
        """Test compilation of a basic function"""
        source = """
        func add(a: i32, b: i32) -> i32 {
            return a + b;
        }
        """
        
        # Compile
        wasm_binary = self.compiler.compile(source)
        
        # Basic validation
        self.assertIsNotNone(wasm_binary)
        self.assertTrue(len(wasm_binary) > 0)
        
        # Verify WASM magic number
        self.assertEqual(wasm_binary[:4], b"\x00asm")
        
        # Save for inspection
        with open("test_output.wasm", "wb") as f:
            f.write(wasm_binary)
            
        self.logger.info("Test WASM binary saved to test_output.wasm")

if __name__ == '__main__':
    unittest.main() 