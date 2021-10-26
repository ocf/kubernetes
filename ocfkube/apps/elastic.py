from ocfkube.utils import helm
from ocfkube.utils import versions

values = {}

license = [
    {
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {
            "labels": {"license.k8s.elastic.co/scope": "operator"},
            "name": "eck-license",
        },
        "type": "Opaque",
        "stringData": {"license": "this is a dummy value, *not* a real license"},
    }
]


def build() -> object:
    return helm.build_chart_from_versions(
        name="elastic", versions=versions, values=values, namespace="eck-operator"
    ) + license
