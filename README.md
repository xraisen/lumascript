# LumaScript

A simple, efficient programming language that compiles to WebAssembly.

## Features

- **Type Safety**: Static typing with clear type annotations
- **WebAssembly Output**: Direct compilation to WASM
- **Control Flow**: If statements and while loops
- **Local Variables**: Variable declarations and assignments
- **Arithmetic Operations**: Basic math and comparison operators
- **Function Support**: Multiple function definitions with parameters

## Language Syntax

### Function Definitions
```lua
func add(a: i32, b: i32) -> i32 {
    return a + b;
}
```

### Variables
```lua
let x: i32 = 42;
x = x + 1;
x += 1;  // Compound assignment
```

### Control Flow
```lua
// If statements
if (x > 0) {
    return x;
} else {
    return -x;
}

// While loops
while (i < n) {
    sum += i;
    i += 1;
}
```

### Types
- `i32`: 32-bit integer
- `i64`: 64-bit integer
- `f32`: 32-bit float
- `f64`: 64-bit float

## Examples

### Fibonacci Sequence
```lua
func fibonacci(n: i32) -> i32 {
    let a: i32 = 0;
    let b: i32 = 1;
    let i: i32 = 0;
    
    while (i < n) {
        let temp: i32 = a + b;
        a = b;
        b = temp;
        i += 1;
    }
    
    return a;
}
```

### Sum to N
```lua
func sum_to(n: i32) -> i32 {
    let sum: i32 = 0;
    let i: i32 = 1;
    
    while (i <= n) {
        sum += i;
        i += 1;
    }
    
    return sum;
}
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lumascript.git
cd lumascript
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Write your LumaScript code in a `.ls` file:
```lua
func main() -> i32 {
    return 42;
}
```

2. Compile to WASM:
```bash
python -m lumascript compile input.ls -o output.wasm
```

3. Run the tests:
```bash
python -m pytest tests/
```

## Development Status

Current version: 0.3.0

### Implemented Features
- [x] Basic arithmetic operations
- [x] Function definitions
- [x] If statements and conditions
- [x] While loops
- [x] Local variables
- [x] Compound assignments
- [x] Type checking

### Planned Features
- [ ] Arrays and memory management
- [ ] String support
- [ ] Standard library
- [ ] Module system
- [ ] Error handling
- [ ] Optimizations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.