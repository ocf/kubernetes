from transpire import helm
from transpire.utils import get_versions

name = "postgres-operator"


def objects():
    yield from helm.build_chart_from_versions(
        name=name,
        versions=get_versions(__file__),
    )

    yield {
        "apiVersion": "acid.zalan.do/v1",
        "kind": "postgresql",
        # name must be in {TEAM}-{NAME} format
        "metadata": {"name": "ocf-postgres-nvme"},
        "spec": {
            "teamId": "ocf",
            "volume": {
                "size": "512Gi",
                "storageClass": "rbd-nvme",
            },
            "numberOfInstances": 1,
            "postgresql": {"version": "14"},
        },
    }
