# Modern Python Type Annotations

**ALWAYS use modern Python type annotation syntax instead of importing from the typing module.**

## ❌ WRONG - Don't do this:
```python
from typing import List, Dict, Set, Optional, Union

def process_items(items: List[str]) -> Optional[Dict[str, str]]:
    unique_items: Set[str] = set(items)
    return {"count": len(unique_items)} if unique_items else None

# Old union syntax
def handle_data(data: Union[str, bytes]) -> str:
    return str(data)

# Old optional syntax
def get_value(key: str) -> Optional[str]:
    return None
```

## ✅ CORRECT - Always do this:
```python
def process_items(items: list[str]) -> dict[str, str] | None:
    unique_items: set[str] = set(items)
    return {"count": len(unique_items)} if unique_items else None

# Modern union syntax
def handle_data(data: str | bytes) -> str:
    return str(data)

# Modern optional syntax
def get_value(key: str) -> str | None:
    return None
```

## Type Annotation Mapping

| Old Syntax | New Syntax | Example |
|------------|------------|---------|
| `List[T]` | `list[T]` | `list[str]` |
| `Dict[K, V]` | `dict[K, V]` | `dict[str, int]` |
| `Set[T]` | `set[T]` | `set[int]` |
| `Tuple[T, ...]` | `tuple[T, ...]` | `tuple[int, str]` |
| `Optional[T]` | `T | None` | `str | None` |
| `Union[T1, T2]` | `T1 | T2` | `str | bytes` |

## When to Still Import from typing

**Only import from typing for types that don't have built-in alternatives:**

```python
from typing import Protocol, TypeVar, Callable

# Protocols (structural typing)
class Readable(Protocol):
    def read(self) -> str: ...

# Type variables for generics
T = TypeVar('T')
def identity(item: T) -> T:
    return item

# Complex callable types
def apply_func(func: Callable[[int], str], value: int) -> str:
    return func(value)
```

## Benefits

1. **Cleaner Code**: More readable and concise
2. **Better Performance**: No runtime overhead from typing imports
3. **Modern Python**: Uses Python 3.9+ built-in generics
4. **Consistency**: All type annotations follow the same pattern
5. **Maintainability**: Easier to read and understand
