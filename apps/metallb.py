from transpire import helm

from apps.versions import versions

name = "metallb"

pool = {
    "apiVersion": "metallb.io/v1beta1",
    "kind": "IPAddressPool",
    "metadata": {"name": "pool-1"},
    "spec": {
        "addresses": [
            "169.229.226.81-169.229.226.89",
            "2607:f140:8801::1:81-2607:f140:8801::1:89",
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
        versions=versions,
        values={},
    )

    yield pool
    yield method

