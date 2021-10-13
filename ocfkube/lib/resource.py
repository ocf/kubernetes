from __future__ import annotations

from collections import UserDict
from typing import Any

import yaml


class Resource(UserDict):
    name: str
    namespace: str

    def __init__(self, obj: dict[str, Any], check_namespace: bool = True):
        super().__init__(obj)
        try:
            self.name = obj["metadata"]["name"]
        except KeyError:
            raise ValueError(f"Expected a name for Resource {obj}")

        if check_namespace:
            try:
                self.namespace = obj["metadata"]["namespace"]
            except KeyError:
                raise ValueError(f"Expected a namespace for Resource {obj}")

        if "apiVersion" not in obj.keys():
            raise ValueError(f"Expected an apiVersion for Resource {obj}")

        if "kind" not in obj.keys():
            raise ValueError(f"Expected a kind for Resource {obj}")

    def to_yaml(self) -> str:
        return yaml.dump(self)
