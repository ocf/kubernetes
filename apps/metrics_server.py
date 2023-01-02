from typing import Generator

from transpire import helm

from apps.versions import versions

name = "metrics-server"


def objects() -> Generator[dict, None, None]:
    # Default values seem fine for now, except no Prometheus scraping, but that seems okay?
    # We don't really use autoscaling (at least not yet), so we only need `kubectl top`.
    # <https://artifacthub.io/packages/helm/metrics-server/metrics-server>
    yield from helm.build_chart_from_versions(
        name=name,
        versions=versions,
    )
