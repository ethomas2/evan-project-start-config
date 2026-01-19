# Always Use Fully Qualified Imports

**NEVER use `from` imports or import specific functions/classes directly.**

## ❌ WRONG - Don't do this:
```python
from openai import OpenAI
from config import config
from pathlib import Path
from collections import defaultdict
```

## ✅ CORRECT - Always do this:
```python
import openai
import config
import pathlib
import collections
```

### Usage Examples:

**Instead of:**
```python
client = OpenAI(api_key=config.OPENAI_API_KEY)
path = Path("some/path")
counts = defaultdict(int)
```

**Use:**
```python
client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
path = pathlib.Path("some/path")
counts = collections.defaultdict(int)
```

## Deep Module Imports

When importing from deeply nested modules, it's fine to shorten the import to
the *highest meaningful parent module*.

For example, if you need to access something like `a.b.foo`, don't write

```python
import a.b
a.b.foo()
```

Instead, prefer:

```python
from a import b
b.foo()
```

Or rename b to something clearer

```python
from a import b as renamed
renamed.foo()
```

## Why This Pattern?

1. **Explicit Dependencies**: It's immediately clear where each function/class comes from
2. **Avoids Name Collisions**: Prevents conflicts between imported names and local variables
3. **Better Code Navigation**: IDEs can easily trace where functions are defined
4. **Consistency**: All imports follow the same pattern throughout the codebase
5. **Maintainability**: Easier to refactor and understand code relationships

## Standard Library Imports

Always use fully qualified imports for standard library modules:
- `import os` (not `from os import path`)
- `import sys` (not `from sys import path`)
- `import pathlib` (not `from pathlib import Path`)
- `import json` (not `from json import loads`)
- `import time` (not `from time import time`)
- `import collections` (not `from collections import defaultdict`)

## Third-Party Library Imports

Always use fully qualified imports for third-party libraries:
- `import openai` (not `from openai import OpenAI`)
- `import requests` (not `from requests import get`)
- `import numpy` (not `from numpy import array`)

## Local Module Imports

Always use fully qualified imports for local modules:
- `import config` (not `from config import CONFIG`)
- `import utils` (not `from utils import helper_function`)

## Exception: Type Hints Only

You may use `from` imports ONLY for type hints that aren't built-in:
```python
from typing import Protocol, TypeVar, Callable

class Readable(Protocol):
    def read(self) -> str: ...
```

Note: For built-in type hints like `list`, `dict`, `str | None`, don't import anything - use the built-in syntax directly.
