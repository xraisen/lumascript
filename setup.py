from setuptools import setup, find_packages

setup(
    name="lumascript",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "wasmtime==14.0.0",
    ],
    extras_require={
        "test": ["pytest==7.4.3"],
    },
    python_requires=">=3.8",
    description="A lightweight WASM compiler and runtime cache",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="LumaScript Team",
    license="MIT",
) 