from transpire import helm
from transpire.utils import get_versions

name = "metallb"

pool = {
    "apiVersion": "metallb.io/v1beta1",
    "kind": "IPAddressPool",
    "metadata": {"name": "pool-1"},
    "spec": {
        "addresses": [
            "169.229.226.105-169.229.226.107",
            "2607:f140:8801::1:105-2607:f140:8801::1:107",
        ]
    },
}

method = {
    "apiVersion": "metallb.io/v1beta1",
    "kind": "L2Advertisement",
    "metadata": {"name": "pool-1"},
    "spec": {"ipAddressPools": ["pool-1"]},
}


def objects():
    yield from helm.build_chart_from_versions(
        name="metallb",
        versions=get_versions(__file__),
        values={
            "controller": {
                "metrics": {"enabled": True, "serviceMonitor": {"enabled": True}}
            }
        },
    )

    yield pool
    yield method
