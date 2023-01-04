from typing import Generator

from transpire import helm

from apps.versions import versions

name = "istio"
namespace = "istio-system"


def objects() -> Generator[dict, None, None]:
    yield from helm.build_chart_from_versions(
        name="istio-base",
        versions=versions,
        values={},
    )

    yield from helm.build_chart_from_versions(
        name="istio-istiod",
        versions=versions,
        values={},
    )


