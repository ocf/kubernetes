from ocfkube.utils import helm
from ocfkube.utils import versions

values = {
    "envoy": {
        "service": {
            "loadBalancerIP": "169.229.226.81",
        }
    }
}


def build() -> object:
    return helm.build_chart_from_versions(
        name="nextcloud",
        versions=versions,
        values=values,
    )
