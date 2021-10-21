from typing import Iterable, Optional, Any


__all__ = ["delve"]


def delve(obj: dict, path: Iterable[str]) -> Optional[Any]:
    """
    Get the element of the nested dict at the path provided, returning None if
    any keys along the way do not exist
    """
    curr = obj
    for key in path:
        try:
            curr = curr[key]
        except KeyError:
            return None
    return curr
