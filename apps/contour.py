from transpire import helm
from transpire.utils import get_versions

name = "contour"


def objects():
    yield from helm.build_chart_from_versions(
        name=name,
        versions=get_versions(__file__),
        values={
            "envoy": {
                "service": {
                    "annotations": {
                        "metallb.universe.tf/loadBalancerIPs": "169.229.226.81,2607:f140:8801::1:81",
                    },
                    "ipFamilyPolicy": "PreferDualStack",
                },
                "resourcesPreset": "large", # otherwise it OOMs
            },
            "metrics": {
                "serviceMonitor": {
                    "enabled": True,
                }
            },
        },
    )
