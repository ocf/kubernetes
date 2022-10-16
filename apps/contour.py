from transpire import emit, helm

from apps.versions import versions

values = {
    "envoy": {
        "service": {
            "loadBalancerIP": "169.229.226.81",
        },
    },
}

name = "contour"

def objects() -> None:
    emit(
        helm.build_chart_from_versions(
            name="contour",
            versions=versions,
            values=values,
        )
    )
