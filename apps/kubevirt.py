from typing import Generator

import requests
import yaml
from transpire.utils import get_versions

name = "kubevirt"


def objects() -> Generator[dict, None, None]:
    version = get_versions(__file__)[name]["version"]
    yield from yaml.safe_load_all(
        requests.get(
            f"https://github.com/kubevirt/kubevirt/releases/download/{version}/kubevirt-operator.yaml"
        ).text
    )

    yield {
        "apiVersion": "kubevirt.io/v1",
        "kind": "KubeVirt",
        "metadata": {"name": "kubevirt", "namespace": "kubevirt"},
        "spec": {
            "certificateRotateStrategy": {},
            "configuration": {"developerConfiguration": {"featureGates": []}},
            "customizeComponents": {},
            "imagePullPolicy": "IfNotPresent",
            "workloadUpdateStrategy": {},
        },
    }
