from typing import Generator

from transpire import helm
from transpire.utils import get_versions

name = "argo-events"


def objects() -> Generator[dict, None, None]:
    yield from helm.build_chart_from_versions(
        name="argo-events",
        versions=get_versions(__file__),
        values={
            "controller": {
                "metrics": {
                    "enabled": True, 
                    "serviceMonitor": {"enabled": True}
                },
            },
        }, 
    )
