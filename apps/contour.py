from transpire.dsl import helm
from transpire.dsl import emit
from apps.versions import versions

values = {
    "envoy": {
        "service": {
            "loadBalancerIP": "169.229.226.81",
        },
    },
}


def build() -> None:
    emit(
        helm.build_chart_from_versions(
            name="contour",
            versions=versions,
            values=values,
        )
    )
