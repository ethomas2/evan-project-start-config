import collections
import contextlib
import functools
import hashlib
import inspect
import logging
import pathlib
import sys
import time
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterable,
    Callable,
    Generator,
    Iterable,
    Mapping,
    Optional,
    Sequence,
    TextIO,
    Type,
    get_args,
    get_origin,
    overload,
)

logger = logging.getLogger(__name__)


def find_git_root(
    start_path: pathlib.Path | str | None = None,
) -> pathlib.Path:  # TODO: rename to find_app_root()
    """
    Find the root directory of the git repository by searching upwards
    from the given path or the current working directory.
    """

    current_path = pathlib.Path(start_path) if start_path is not None else pathlib.Path.cwd()
    if not current_path.is_dir():
        current_path = current_path.parent

    while not (current_path / ".git").is_dir():
        current_path = current_path.parent
        is_root = current_path.parent == current_path
        if is_root:
            raise ValueError("Could not find git root")
    return current_path


def md5_hash(content: str | bytes) -> str:
    match content:
        case str():
            return hashlib.md5(content.encode("utf-8")).hexdigest()
        # I don't understand why i have to do this if content is typed as
        # bytes. Pyright makes me do this
        case bytes() | bytearray() | memoryview():
            return hashlib.md5(content).hexdigest()


def timeit(func):
    """Poor man's metrics before we have real metrics in gcp/datadog"""

    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end_time = time.time()
                elapsed_time = end_time - start_time
                logger.info(
                    "Timeit: async function label=%s took seconds=%.4f to complete",
                    func.__name__,
                    elapsed_time,
                )

        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(
                "Timeit: sync function label=%s took seconds=%.4f seconds to complete",
                func.__name__,
                elapsed_time,
            )

    return sync_wrapper


@contextlib.contextmanager
def timeit_contextmanager(label: str):
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info("Timeit: label=%s took seconds=%.4f to complete", label, elapsed_time)


def groupby[K, V](iterable: Iterable[V], keyfunc: Callable[[V], K]) -> dict[K, list[V]]:
    """
    Given an iterable and a key function, return a dictionary where the keys are
    the result of applying the key function to each element of the iterable and
    the values are lists of elements that map to that key.
    """
    result = {}
    for item in iterable:
        key = keyfunc(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result


def all_same[T](iterable: Iterable[T]) -> bool:
    try:
        first_item = next(iter(iterable))
    except StopIteration:
        return True
    return all(first_item == item for item in iterable)


def check(condition: bool, message: str):
    """Like assert, but can't be disabled by python -O"""
    if not condition:
        raise AssertionError(message)


class InvariantError(Exception):
    """
    Indicates that some invariant that is expected to be
    enforced by application code has been broken
    """


def hist[T](iterable: Iterable[T]) -> dict[T, int]:
    """
    Return a histogram of the elements in the iterable.

    >>> hist(['A', 'B', 'A', 'C', 'B', 'A'])
    >>> {'A': 3, 'B': 2, 'C': 1}
    """
    d = collections.defaultdict(int)
    for item in iterable:
        d[item] += 1
    return d


@overload
def chunks[T](iterable: Iterable[T], n: int) -> Generator[list[T], None, None]: ...


@overload
def chunks[T](iterable: AsyncIterable[T], n: int) -> AsyncGenerator[list[T], None]: ...


def _chunks_sync[T](iterable: Iterable[T], n: int) -> Generator[list[T], None, None]:
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == n:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


async def _chunks_async[T](iterable: AsyncIterable[T], n: int) -> AsyncGenerator[list[T], None]:
    chunk = []
    async for item in iterable:
        chunk.append(item)
        if len(chunk) == n:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def chunks[T](iterable: Iterable[T] | AsyncIterable[T], n: int):
    """
    Given an iterable or async iterable of values (x1, x2, x3, ...), return batches of size n.

    >>> list(chunks([1, 2, 3, 4, 5, 6, 7, 8, 9], 3))
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    Async Usage:
    >>> async def main():
    >>>     async for chunk in chunks(some_async_iterable, 3):
    >>>         print(chunk)
    """
    if isinstance(iterable, AsyncIterable):
        return _chunks_async(iterable, n)
    return _chunks_sync(iterable, n)


def assert_not_none[T](  # pylint: disable=keyword-arg-before-vararg
    value: T | None,
    msg: str | None = None,
    *args: Any,
) -> T:
    """
    Assert that `value` is not None. Raise an error if it is.
    """
    if value is None:
        errmsg = None
        match (msg, len(args)):
            case (None, _):
                errmsg = f"Expected {value} to not be None"
            case (_, 0):
                errmsg = msg
            case (_, _):
                errmsg = msg % args
        raise AssertionError(errmsg)
    return value


def assert_type[T](  # pylint: disable=keyword-arg-before-vararg
    value: Any,
    type_: Type[T],
    msg: Optional[str] = None,
    *args: Any,
) -> T:
    """
    Runtime assertion that `value` isinstance of `type_`. Useful for when the
    type of a value is expected to be T, but the type cannot be known until
    runtime (e.g. when reading a value off the wire)

    For parameterized types (e.g. list[int]), recursively checks that:
    1. The value is an instance of the container type (e.g. list)
    2. Each item in the value is an instance of the contained type (e.g. int)
    """

    def get_error_message(
        value: Any,
        expected_type: Type[Any],
        msg: Optional[str],
        args: tuple[Any, ...],
    ) -> str:
        """Helper function to generate error messages for type assertions"""
        if msg is None:
            return f"Expected {value} to be an instance of {expected_type}"
        if not args:
            return msg
        return msg % args

    container_type = get_origin(type_)
    if container_type is not None:  # This is a parameterized type
        # First check that value is an instance of the container type
        if not isinstance(value, container_type):
            raise AssertionError(get_error_message(value, container_type, msg, args))

        # Then check each item in the value against the contained type
        contained_type = get_args(type_)[0]
        for item in value:
            try:
                assert_type(item, contained_type, msg, *args)
            except AssertionError as e:
                raise AssertionError(
                    get_error_message(
                        value,
                        contained_type,
                        (
                            f"Expected all items in {value} to be instances of {contained_type}, "
                            f"but found {item}"
                        ),
                        args,
                    )
                ) from e
    else:
        # Non-parameterized type, use regular isinstance check
        if not isinstance(value, type_):
            raise AssertionError(get_error_message(value, type_, msg, args))
    return value


def print_green(message: str, file: TextIO | None = None):
    file = file or sys.stdout
    print(f"\033[0;32m{message}\033[0m", flush=True, file=file)


def print_red(message: str, file: TextIO | None = None):
    file = file or sys.stderr
    print(f"\033[0;31m{message}\033[0m", flush=True, file=file)


def flatten[T](xss: list[list[T]]) -> list[T]:
    return [x for xs in xss for x in xs]


def exactly_one[T](iter_: Iterable[T], msg: str | None = None) -> T:
    """Assert that the list has exactly one element and return that element."""
    it = iter(iter_)
    try:
        item = next(it)
    except StopIteration:
        raise ValueError(  # pylint: disable=raise-missing-from
            msg or "Expected exactly one element, got 0"
        )
    try:
        next(it)
    except StopIteration:
        pass
    else:
        raise ValueError(msg or "Expected exactly one element, got more than 1")
    return item


def table(arr: list[list[str]]):
    """
    Given a list of lists, return a justified string representation of the table
    """
    arr = [list(map(str, row)) for row in arr]
    cols = zip(*arr)
    col_widths = [max(map(len, col)) for col in cols]

    padded_tbl = [
        [item + " " * (col_width - len(item)) for item, col_width in zip(row, col_widths)]
        for row in arr
    ]

    return "\n".join("| " + " | ".join(row) + " |" for row in padded_tbl)


JSONType = str | int | float | bool | None | Mapping[str, "JSONType"] | Sequence["JSONType"]


def to_jsonable(obj: Any) -> JSONType:
    """Convert an object to a JSON-serializable format."""
    return jsonable_encoder(obj)
