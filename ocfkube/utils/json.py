from typing import Iterable, Optional, Any


__all__ = ["delve", "shelve"]


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


def shelve(
    obj: dict, path: Iterable[str], val: Any, *, create_parents: bool = False
) -> dict:
    """
    Set the element of the nested dict at the path provided, returning the
    (in-place modified) object, throwing KeyError if any keys along the way do
    not exist
    """
    curr: Optional[dict] = obj
    prev: Optional[dict] = None
    prev_key = None
    for key in path:
        if curr is None:
            if create_parents:
                curr = dict()
                assert prev is not None
                prev[prev_key] = curr
            else:
                raise KeyError(prev_key)
        prev, prev_key = curr, key
        try:
            curr = curr[key]
        except KeyError:
            curr = None
    if prev is None:
        return val
    prev[prev_key] = val
    return obj
