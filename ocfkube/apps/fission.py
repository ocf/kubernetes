from ocfkube.utils import helm
from ocfkube.utils import versions

values = {
    # TODO: Enable prometheus here...
    # "prometheus": {"serviceEndpoint": "xx"}
    "serviceType": "ClusterIP",
    "routerServiceType": "ClusterIP",
    "analytics": False,
    "canaryDeployment": {"enabled": True},
}


def build() -> object:
    return helm.build_chart_from_versions(
        name="fission",
        versions=versions,
        values=values,
    )
