from typing import Any
import yaml


class Resource:
    _obj: dict

    def __init__(self, obj: object) -> "Resource":
        self._obj = obj
        try:
            self.name = self._obj["metadata"]["name"]
        except ValueError:
            raise ValueError(f"Expected a name for Resource {obj}")

        try:
            self.namespace = self._obj["metadata"]["namespace"]
        except ValueError:
            raise ValueError(f"Expected a namespace for Resource {obj}")

        if "apiVersion" not in self.obj_.keys():
            raise ValueError(f"Expected an apiVersion for Resource {obj}")

        if "kind" not in self.obj_.keys():
            raise ValueError(f"Expected a kind for Resource {obj}")

    def __getitem__(self, name: str) -> Any:
        if isinstance(self, dict):
            return Resource(self)
        return getattr(self._obj, name)

    def to_yaml(self) -> str:
        return yaml.dump(self._obj)
