from typing import Any, Iterable, Iterator
import json


def json_stream(data: Iterable[Any], count: int) -> Iterator[str]:
    """
    Streams a list JSON objects to the client.
    """
    yield "["
    for i, x in enumerate(data):
        s = json.dumps(x, separators=(",", ":"))  # no whitespaces
        if i < count - 1:
            s += ","
        yield s
    yield "]"
