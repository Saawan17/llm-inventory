# Python

## Overview
Python is a high-level, dynamically typed programming language known for readable syntax and a broad ecosystem. It is widely used for automation, web services, data processing, machine learning, and AI applications.

## Basic example
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Saawan"))
```
Type hints document expected types and can be checked by static analysis tools, but Python does not enforce them automatically at runtime.

## Core concepts
- **Indentation:** Indentation defines code blocks.
- **Variables:** Names refer to objects; types are associated with objects rather than declared in variable declarations.
- **Built-in collections:** `list` is an ordered mutable sequence, `tuple` is an ordered immutable sequence, `dict` maps keys to values, and `set` stores unique elements.
- **Control flow:** `if`, `for`, `while`, `break`, and `continue`.
- **Functions:** Use `def`; return values with `return`.
- **Exceptions:** Use `try`, `except`, `else`, and `finally` to handle errors.
- **Comprehensions:** Concise syntax for constructing collections.

## Modules and environments
A module is a Python file that can be imported. A package groups modules. Use a virtual environment to isolate project dependencies:
```bash
python -m venv .venv
```
Activate the environment using the command appropriate for your operating system, then install dependencies with `python -m pip install package-name`. A `requirements.txt` file or a modern project configuration can record dependencies.

## File handling
Use a context manager so files are closed reliably:
```python
from pathlib import Path

path = Path("notes.txt")
path.write_text("RAG notes", encoding="utf-8")
text = path.read_text(encoding="utf-8")
```
For JSON data, use the standard library's `json` module.

## Classes and data models
Classes bundle data and behavior. Use `dataclasses` for straightforward data containers:
```python
from dataclasses import dataclass

@dataclass
class Product:
    product_id: str
    name: str
    price: float
```
For application input validation, a validation library may be useful, but validate business rules explicitly as well.

## Iterators and generators
An iterator yields values one at a time. A generator function uses `yield`, which can reduce memory use when processing large sequences because it need not build the entire result in memory.

## Async programming
`async` and `await` support asynchronous I/O. Async code is useful when tasks spend time waiting on network or other asynchronous operations. It does not automatically make CPU-bound work faster. Use suitable process-based or specialized approaches for CPU-heavy workloads.

## Python for AI and RAG
Common building blocks include:
- An embedding model that converts text into vectors.
- A vector index or vector database for similarity search.
- A document loader and chunking strategy.
- A retrieval step that selects passages relevant to a query.
- A language model that generates an answer grounded in retrieved passages.

Keep API keys in environment variables or a secrets manager, not in source code. Set request timeouts, handle rate limits, and avoid logging secrets or private document contents.

## Error handling and testing
Use specific exception types and preserve useful context. Avoid broad `except Exception` blocks unless they are part of a deliberate boundary that logs and handles unexpected failures. Use `pytest` or `unittest` to test normal cases, invalid inputs, and failure paths.

## Good practices
- Follow PEP 8 style conventions.
- Prefer clear, descriptive names.
- Keep functions focused and avoid unnecessary global state.
- Use `pathlib` for filesystem paths.
- Use logging instead of `print` for application diagnostics.
- Pin or constrain dependencies for reproducible deployments.
- Validate external input and treat retrieved content as untrusted.
