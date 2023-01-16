from transpire import helm
from transpire.utils import get_versions

name = "keda"


def objects():
    yield from helm.build_chart_from_versions(
        name=name,
        versions=get_versions(__file__),
        values={
            "prometheus": {
                "metricServer": {
                    "enabled": True,
                    "podMonitor": {"enabled": True},
                },
                "operator": {
                    "enabled": True,
                    "podMonitor": {"enabled": True},
                },
            },
        },
    )
