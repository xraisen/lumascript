# Changelog

All notable changes to the LumaScript compiler will be documented in this file.

## [0.3.0] - 2024-03-XX

### Added
- Local variable declarations with `let` keyword
- While loops with condition and body
- Variable assignments (=, +=, -=, *=, /=)
- Additional comparison operators (<=, >=)
- Example program (fibonacci.ls) demonstrating loops and variables
- Test suite for local variables and loops
- Compound assignment operators

### Changed
- Enhanced WASM generator to handle local variables
- Updated parser to support new statement types
- Improved lexer with new operators and keywords

### Fixed
- Local variable scope handling
- Loop control flow in WASM generation

## [0.2.0] - 2024-03-XX

### Added
- If statements with else blocks
- Comparison operators (<, >, ==)
- Basic arithmetic operations (+, -, *, /)
- WASM code generation for control flow
- Example program (max.ls) demonstrating conditionals
- Test suite for parser and generator
- Integration with wasmtime for runtime testing

### Changed
- Enhanced parser to handle control flow
- Updated WASM generator to support conditionals
- Improved error messages for syntax errors

### Fixed
- Parser error handling for missing semicolons
- WASM generation for nested expressions

## [0.1.0] - 2024-03-XX

### Added
- Basic lexer with token recognition
- Simple parser for function definitions
- Initial WASM generator
- Support for i32 type
- Function parameters and return types
- Basic expression parsing
- Core compiler infrastructure 