"""
Tests for the WASM caching system.
Follows KISS principle with minimal, focused tests.
"""

import unittest
from pathlib import Path
from src.wasm.wasm_cache import WASMCache

class TestWASMCache(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.cache = WASMCache(cache_dir=".test_cache")
        self.test_dir = Path(__file__).parent / "test_files"
        self.test_dir.mkdir(exist_ok=True)
        
        # Create test C file
        self.source_file = self.test_dir / "test_add.c"
        with open(self.source_file, "w") as f:
            f.write("""
            int add(int a, int b) {
                return a + b;
            }
            """)
    
    def tearDown(self):
        """Clean up test environment"""
        # Remove test files
        if self.source_file.exists():
            self.source_file.unlink()
        if self.test_dir.exists():
            self.test_dir.rmdir()
            
        # Clear cache
        cache_dir = Path(".test_cache")
        if cache_dir.exists():
            for file in cache_dir.glob("*"):
                file.unlink()
            cache_dir.rmdir()
    
    def test_cache_initialization(self):
        """Test cache directory creation"""
        self.assertTrue(Path(".test_cache").exists())
        self.assertTrue(Path(".test_cache").is_dir())
    
    def test_get_instance(self):
        """Test getting WASM instance"""
        instance = self.cache.get_instance(self.source_file)
        self.assertIsNotNone(instance)
        
        # Test function execution
        store = instance.store
        add = instance.exports(store)["add"]
        result = add(store, 5, 3)
        self.assertEqual(result, 8)
    
    def test_cache_reuse(self):
        """Test that cache is reused for same file"""
        # First call should compile
        instance1 = self.cache.get_instance(self.source_file)
        
        # Second call should use cache
        instance2 = self.cache.get_instance(self.source_file)
        
        self.assertIsNotNone(instance1)
        self.assertIsNotNone(instance2)
        
        # Test both instances work
        store1 = instance1.store
        store2 = instance2.store
        add1 = instance1.exports(store1)["add"]
        add2 = instance2.exports(store2)["add"]
        
        self.assertEqual(add1(store1, 5, 3), 8)
        self.assertEqual(add2(store2, 5, 3), 8)
    
    def test_cache_invalidation(self):
        """Test cache invalidation when file changes"""
        # Get initial instance
        instance1 = self.cache.get_instance(self.source_file)
        
        # Modify source file
        with open(self.source_file, "w") as f:
            f.write("""
            int add(int a, int b) {
                return a + b + 1;  // Changed function
            }
            """)
        
        # Get new instance
        instance2 = self.cache.get_instance(self.source_file)
        
        store1 = instance1.store
        store2 = instance2.store
        add1 = instance1.exports(store1)["add"]
        add2 = instance2.exports(store2)["add"]
        
        # Original instance should return 8
        self.assertEqual(add1(store1, 5, 3), 8)
        # New instance should return 9
        self.assertEqual(add2(store2, 5, 3), 9)

if __name__ == "__main__":
    unittest.main() 