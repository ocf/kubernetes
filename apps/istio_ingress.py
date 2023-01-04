from typing import Generator

from transpire import helm

from apps.versions import versions

name = "istio-ingress"
namespace = "istio-ingress"


def objects() -> Generator[dict, None, None]:
    # Manually create the namespace so injection is enabled.
    # <https://istio.io/latest/docs/setup/install/helm/#installation-steps>
    yield {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {
            "labels": {"istio-injection": "enabled"},
            "name": namespace,
        },
    }

    yield from helm.build_chart_from_versions(
        name=name,
        versions=versions,
        values={
            "service": {
                "annotations": {
                    "metallb.universe.tf/loadBalancerIPs": "169.229.226.84,2607:f140:8801::1:84",
                },
            },
        },
    )
