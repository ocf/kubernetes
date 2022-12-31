from typing import Generator
import requests
import hashlib
import base64
import yaml

from transpire import helm

from apps.versions import versions

name = "knative"


def objects() -> Generator[dict, None, None]:
    version = versions[name]["version"]
    checksum = versions[name]["checksum"]
    yaml_str = requests.get(
        f"https://github.com/knative/operator/releases/download/knative-v{version}/operator.yaml"
    ).text

    # Make sure the input hasn't changed...
    yaml_checksum = base64.b64encode(
        hashlib.sha256(bytes(yaml_str, "utf-8")).digest()
    ).decode("utf-8")
    if yaml_checksum != checksum:
        raise ValueError(
            f"Received bad YAML from github? Got SHA256:{yaml_checksum} but expected SHA256:{checksum}."
        )

    # Deploy operator
    yield from yaml.safe_load_all(yaml_str)
