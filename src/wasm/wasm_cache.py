import os
import hashlib
import pickle
from pathlib import Path
from typing import Dict, Optional, Any
from wasmtime import Store, Module, Instance
from datetime import datetime, timedelta

class WASMCache:
    def __init__(self, cache_dir: str = ".wasm_cache"):
        """Initialize WASM cache with specified directory"""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.binary_cache: Dict[str, bytes] = {}
        self.module_cache: Dict[str, Module] = {}
        self.instance_cache: Dict[str, Instance] = {}
        self.metadata: Dict[str, Any] = {}
        self._load_cache()

    def _get_cache_key(self, source_path: Path) -> str:
        """Generate cache key based on file content and modification time"""
        with open(source_path, 'rb') as f:
            content = f.read()
        mtime = os.path.getmtime(source_path)
        return hashlib.sha256(f"{content}{mtime}".encode()).hexdigest()

    def _load_cache(self) -> None:
        """Load cached data from disk"""
        try:
            metadata_file = self.cache_dir / "metadata.pkl"
            if metadata_file.exists():
                with open(metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)

            # Load cached binaries
            for cache_file in self.cache_dir.glob("*.wasm"):
                key = cache_file.stem
                if self._is_cache_valid(key):
                    with open(cache_file, 'rb') as f:
                        self.binary_cache[key] = f.read()
                else:
                    # Clean up invalid cache
                    cache_file.unlink()
                    if key in self.metadata:
                        del self.metadata[key]

        except Exception as e:
            print(f"Error loading cache: {e}")
            self._clear_cache()

    def _save_cache(self, key: str, wasm_binary: bytes) -> None:
        """Save WASM binary and metadata to cache"""
        try:
            # Save binary
            with open(self.cache_dir / f"{key}.wasm", 'wb') as f:
                f.write(wasm_binary)

            # Update metadata
            self.metadata[key] = {
                'created': datetime.now(),
                'expires': datetime.now() + timedelta(days=7)  # Cache for 7 days
            }

            # Save metadata
            with open(self.cache_dir / "metadata.pkl", 'wb') as f:
                pickle.dump(self.metadata, f)

        except Exception as e:
            print(f"Error saving to cache: {e}")

    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached item is still valid"""
        if key not in self.metadata:
            return False
        return datetime.now() < self.metadata[key]['expires']

    def _clear_cache(self) -> None:
        """Clear all cache data"""
        try:
            for file in self.cache_dir.glob("*"):
                file.unlink()
            self.binary_cache.clear()
            self.module_cache.clear()
            self.instance_cache.clear()
            self.metadata.clear()
        except Exception as e:
            print(f"Error clearing cache: {e}")

    def get_instance(self, source_path: Path) -> Optional[Instance]:
        """Get cached WASM instance or create new one"""
        try:
            key = self._get_cache_key(source_path)
            
            # Check if we have a cached instance
            if key in self.instance_cache and self._is_cache_valid(key):
                return self.instance_cache[key]

            # Get or load WASM binary
            if key not in self.binary_cache:
                wasm_file = source_path.with_suffix('.wasm')
                if not wasm_file.exists():
                    return None
                    
                with open(wasm_file, 'rb') as f:
                    wasm_binary = f.read()
                self.binary_cache[key] = wasm_binary
                self._save_cache(key, wasm_binary)

            # Create and cache module
            if key not in self.module_cache:
                store = Store()
                self.module_cache[key] = Module(store.engine, self.binary_cache[key])

            # Create and cache instance
            store = Store()
            instance = Instance(store, self.module_cache[key], [])
            self.instance_cache[key] = instance

            return instance

        except Exception as e:
            print(f"Error getting WASM instance: {e}")
            return None

    def invalidate(self, source_path: Path) -> None:
        """Invalidate cache for specific source file"""
        key = self._get_cache_key(source_path)
        if key in self.binary_cache:
            del self.binary_cache[key]
        if key in self.module_cache:
            del self.module_cache[key]
        if key in self.instance_cache:
            del self.instance_cache[key]
        if key in self.metadata:
            del self.metadata[key]
        
        cache_file = self.cache_dir / f"{key}.wasm"
        if cache_file.exists():
            cache_file.unlink() 