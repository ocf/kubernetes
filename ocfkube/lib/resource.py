from typing import Any


class Resource:
    def __init__(self, obj: object) -> "Resource":
        def to_resource(o: object):
            if isinstance(o, int):
                return o
            elif isinstance(o, bool):
                return o
            elif isinstance(o, list):
                return [to_resource(x) for x in o]
            elif isinstance(o, dict):
                result = {}
                for key, value in o.items():
                    result[key] = to_resource(value)
                return result
            else:
                raise ValueError(f"Unexpected type {type(o)} of {o} in Resource")

        # check for the existence of a apiVersion, kind, a metadata.name, and a metadata.namespace
        self._obj: dict = to_resource(obj)
        try:
            self.name = self._obj["metadata"]["name"]
        except ValueError:
            raise ValueError(f"Expected a name for Resource {o}")

        try:
            self.namespace = self._obj["metadata"]["namespace"]
        except ValueError:
            raise ValueError(f"Expected a namespace for Resource {o}")

        if "apiVersion" not in self.obj_.keys():
            raise ValueError(f"Expected an apiVersion for Resource {o}")

        if "kind" not in self.obj_.keys():
            raise ValueError(f"Expected a kind for Resource {o}")

    def __getitem__(self, name: str) -> Any:
        if isinstance(self, dict):
            return Resource(self)
        return getattr(self._obj, name)
