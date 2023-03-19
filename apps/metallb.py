from transpire import helm
from transpire.utils import get_versions

name = "metallb"

pool = {
    "apiVersion": "metallb.io/v1beta1",
    "kind": "IPAddressPool",
    "metadata": {"name": "pool-1"},
    "spec": {
        "addresses": [
            "169.229.226.81-169.229.226.89",
            "2607:f140:8801::1:81",
            "2607:f140:8801::1:82",
            "2607:f140:8801::1:83",
            "2607:f140:8801::1:84",
            "2607:f140:8801::1:85",
            "2607:f140:8801::1:86",
            "2607:f140:8801::1:87",
            "2607:f140:8801::1:88",
            "2607:f140:8801::1:89",
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
        values={"controller": {"metrics": {"enabled": True}}},
    )

    yield pool
    yield method
