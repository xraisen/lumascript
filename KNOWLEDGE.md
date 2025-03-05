# LumaScript Knowledge Base

## Core Principles

### MOTO (Make One Thing Outstanding)
- **Focus**: Pure Python + WASM communication
- **Excellence**: Best-in-class WASM caching and execution
- **Simplicity**: One clear purpose, executed perfectly
- **Mastery**: Deep understanding of WASM binary format

### ZERO (Zero External Dependencies, Zero Complexity)
- **Dependencies**: Only Python standard library + WASM
- **Complexity**: Minimal code paths, clear flow
- **Learning Curve**: Easy to understand, hard to misuse
- **Maintenance**: Self-contained, easily debuggable

## Technical Knowledge Base

### 1. WASM Core Concepts

#### Binary Format
```
Magic Number: 0x6d736100
Version: 0x01000000
Sections:
- Type (1)
- Function (3)
- Memory (5)
- Export (7)
- Code (10)
```

#### Basic Types
```
i32: 32-bit integer
i64: 64-bit integer
f32: 32-bit float
f64: 64-bit float
```

### 2. Caching System

#### Cache Key Generation
```python
def _get_cache_key(source_path: Path) -> str:
    """Generate cache key based on file content and modification time"""
    content = read_file(source_path)
    mtime = get_mtime(source_path)
    return sha256(f"{content}{mtime}")
```

#### Cache Structure
```
.wasm_cache/
├── metadata.pkl      # Cache metadata
└── [hash].wasm      # Cached WASM modules
```

### 3. Core Operations

#### Compilation Pipeline
```
Source Code → WASM Binary → Cache → Execute
```

#### Function Mapping
```python
# Python/C Function
def add(a: int, b: int) -> int:
    return a + b

# WASM Equivalent
(func $add 
  (param $a i32) 
  (param $b i32) 
  (result i32)
  local.get $a
  local.get $b
  i32.add)
```

### 4. Best Practices

#### Code Organization
```
src/
├── wasm/           # WASM core functionality
│   ├── cache.py    # Caching system
│   └── decoder.py  # WASM binary handling
├── utils/          # Utilities
└── main.py         # Entry point
```

#### Performance Optimization
1. Cache frequently used modules
2. Minimize binary size
3. Use native WASM types
4. Batch operations when possible

#### Error Handling
```python
try:
    instance = cache.get_instance(source_file)
    if not instance:
        raise RuntimeError("Failed to get WASM instance")
except Exception as e:
    log_error(f"WASM error: {e}")
```

### 5. Testing Strategy

#### Unit Tests
- Test cache operations
- Verify WASM compilation
- Check error handling

#### Integration Tests
- End-to-end compilation
- Cache persistence
- Memory management

### 6. Development Workflow

1. Write minimal code
2. Ensure zero dependencies
3. Test thoroughly
4. Cache effectively
5. Document clearly

### 7. Future Considerations

#### Planned Features
- SIMD support
- Multi-threading
- Memory optimization
- Performance profiling

#### Non-Goals
- Complex language features
- External dependencies
- Unnecessary abstractions

## Conclusion

This knowledge base represents our commitment to:
1. Making WASM communication outstanding
2. Maintaining zero external dependencies
3. Keeping complexity at a minimum
4. Focusing on performance and reliability

Remember: "Make it work, make it right, make it fast, make it simple." 

Glory to God!