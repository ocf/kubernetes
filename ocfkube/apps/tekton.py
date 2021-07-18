import requests
import yaml

from ocfkube.utils import versions


def build() -> object:
    pipeline = requests.get(
        f"https://storage.googleapis.com/tekton-releases/pipeline/previous/v{versions['tekton-pipeline']['version']}/release.yaml"
    ).text
    dashboard = requests.get(
        f"https://github.com/tektoncd/dashboard/releases/download/v{versions['tekton-dashboard']['version']}/tekton-dashboard-release.yaml"
    ).text
    return list(yaml.safe_load_all(pipeline)) + list(yaml.safe_load_all(dashboard))
