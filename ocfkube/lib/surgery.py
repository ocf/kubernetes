from typing import Dict, Tuple, List, Union, Callable, Optional, Iterable, Any, cast
from ocfkube.utils.json import shelve

RESOURCE_APIS = {
    "Deployment": "apps/v1",
    "Secret": "v1",
    "Service": "v1",
    "ConfigMap": "v1",
}


def edit_manifests(
    edits: Dict[
        Union[Tuple[str, str], Tuple[Tuple[str, str], str]], Callable[[dict], dict]
    ],
    manifests: Iterable[dict],
) -> List[dict]:
    resolved_edits: Dict[Tuple[Optional[str], str, str], Callable[[dict], dict]] = {
        (
            k[0][0]
            if isinstance(k[0], tuple)
            else RESOURCE_APIS.get(k[0], cast(str, None)),
            k[0] if isinstance(k[0], str) else k[0][1],
            k[1],
        ): v
        for k, v in edits.items()
    }
    unseen = set(resolved_edits.keys())

    def mapper(m: dict) -> dict:
        key1: Tuple[Optional[str], str, str] = (
            m["apiVersion"],
            m["kind"],
            m["metadata"]["name"],
        )
        key2 = (None, *key1[1:])
        func = resolved_edits.get(key1, resolved_edits.get(key2, None))
        if func is not None:
            try:
                unseen.remove(key1)
            except KeyError:
                unseen.remove(key2)
            return func(m)
        return m

    result = list(map(mapper, manifests))
    if unseen:
        raise RuntimeError(f"Some edits were not applied: {repr(unseen)}")
    return result


def make_edit_manifest(
    edits: Dict[Iterable[str], Any], *, create_parents: bool = False
) -> Callable[[dict], dict]:
    def edit(m):
        for path, val in edits.items():
            shelve(m, path, val, create_parents=create_parents)
        return m

    return edit
