from transpire import helm

from apps.versions import versions

name = "keda"


def objects():
    yield from helm.build_chart_from_versions(
        name=name,
        versions=versions,
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
