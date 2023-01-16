from typing import Generator

from transpire import helm
from transpire.utils import get_versions

name = "argo-workflows"


def objects() -> Generator[dict, None, None]:
    # TODO: Create argo-events namespace.

    yield from helm.build_chart_from_versions(
        name="argo-workflows",
        versions=get_versions(__file__),
    )
