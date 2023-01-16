from transpire import helm
from transpire.utils import get_versions

values = {
    "serviceAccount": {"create": True},
    # TODO: This is a hardcoded variable from the kubelet configuration.
    # Consider automatically grabbing this value.
    "service": {
        "clusterIP": "10.96.0.10",
    },
}

name = "coredns"
namespace = "kube-system"


def objects():
    yield from helm.build_chart_from_versions(
        name="coredns",
        versions=get_versions(__file__),
        values=values,
    )
