# LumaScript 🚀

> A unified, safe, and fast programming language for the future of software development.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://github.com/lumascript/lumascript/workflows/CI/badge.svg)](https://github.com/lumascript/lumascript/actions)
[![Discord](https://img.shields.io/discord/1234567890?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/lumascript)
[![Twitter](https://img.shields.io/twitter/follow/lumascript?style=social)](https://twitter.com/lumascript)

## Why LumaScript? 🤔

LumaScript is designed to revolutionize the way we build software by providing a single, powerful language that combines:

- �� **Speed**: Native/WebAssembly performance vs Python
- 🛡️ **Safety**: No null, no data races
- 🔄 **Unified Workflow**: From data cleaning to AI/ML deployment and web apps in one language, similar to Gatsby Static HTML Website.
- 📦 **Ecosystem**: Batteries included for math, AI/ML, and web

## Features ✨

- **Memory Safety**: No null pointers, no data races
- **WebAssembly Native**: Compile to WebAssembly for web and native targets
- **Tensor Operations**: Built-in support for AI/ML
- **Modern Syntax**: Python-like syntax with static typing
- **Rich Standard Library**: Everything you need, batteries included
- **GPU/TPU Support**: High-performance computing
- **Quantum Computing**: Simulator and IBMQ integration

## Quick Start 🚀

```bash
# Install LumaScript
curl -sSL https://install.lumascript.dev | sh

# Create a new project
lumascript new my-project
cd my-project

# Run your code
lumascript run main.ls
```

## Example Code 💡

```lua
// Hello World
func main() {
    print("Hello, LumaScript! 🚀");
}

// Tensor Operations
func tensor_example() {
    let x = Tensor::new([2, 2], Device::GPU);
    let y = x.matmul(x) + 5.0;
    print(y);
}

// Web Component
@web
struct Dashboard {
    data: DataFrame
}

impl Dashboard {
    func render() -> HTML {
        return html! {
            <div class="dashboard">
                <h1>{ self.data.title }</h1>
                <Plot data=self.data />
            </div>
        };
    }
}
```

## Roadmap 🗺️

- **MVP** (Q4 2024): Core language + Tensor support + WASM compiler
- **Ecosystem** (Q2 2025): Package manager + VS Code plugin
- **Auto-JIT** (Q4 2025): GPU/TPU support
- **Quantum** (2026): Simulator + IBMQ integration

## Contributing 🤝

We welcome contributions! Here's how you can help:

1. Star the repository ⭐
2. Fork the repository 🍴
3. Create a feature branch 🌿
4. Commit your changes 💾
5. Push to the branch 📤
6. Create a Pull Request 🔄

## Community 🌟

- [Discord](https://discord.gg/lumascript)
- [Twitter](https://twitter.com/lumascript)
- [GitHub Discussions](https://github.com/xraisen/lumascript/discussions)

## Documentation 📚

- [Getting Started](docs/getting-started.md)
- [Language Reference](docs/language-reference.md)
- [Standard Library](docs/stdlib.md)
- [Examples](examples/)

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Thanks to all our contributors
- Inspired by Python, Rust, and Julia
- Built with ❤️ by the LumaScript solo-team

---

<p align="center">Made with ❤️ by the LumaScript Solo-Team</p>