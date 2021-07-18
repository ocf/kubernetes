from ocfkube.utils import helm
from ocfkube.utils import versions

values = {
    "serviceAccount": {"create": True},
    # TODO: This is a hardcoded variable from the kubelet configuration.
    # Consider automatically grabbing this value.
    "service": {
        "clusterIP": "10.32.0.10",
    },
}


def build() -> object:
    return helm.build_chart_from_versions(
        name="coredns",
        versions=versions,
        values=values,
    )
