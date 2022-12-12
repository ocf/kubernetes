from typing import Generator

from transpire import helm

from apps.versions import versions

name = "argo-workflows"


def objects() -> Generator[dict, None, None]:
    # TODO: Create argo-events namespace.

    yield from helm.build_chart_from_versions(
        name="argo-workflows",
        versions=versions,
    )
