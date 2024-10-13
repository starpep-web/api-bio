import json
from typing import Callable, TypeVar, Any, Dict, List, Union, Optional


_T = TypeVar('_T')
JsonObject = Dict[str, Any]
JsonObjectArray = List[JsonObject]
Json = Union[JsonObject, JsonObjectArray]


def safe_attribute_chain(f: Callable[[], _T], default: _T = None) -> _T:
    try:
        return f()
    except (AttributeError, IndexError, KeyError):
        return default


def safe_json_parse(data: Optional[str], default: _T = None) -> Union[Optional[Json], _T]:
    if not data:
        return default

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return default


def safe_float(value: Optional[str]) -> Optional[float]:
    if value:
        try:
            return float(value)
        except Exception:
            return None

    return None


def safe_int(value: Optional[str]) -> Optional[int]:
    if value:
        try:
            return int(value)
        except Exception:
            return None

    return None
