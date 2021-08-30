values = {
    "configInline": {
        "address-pools": [
            {
                "name": "default",
                "protocol": "layer2",
                "addresses": [
                    "169.229.226.81-169.229.226.89",
                    "2607:f140:8801::1:81-2607:f140:8801::1:89",
                ],
            }
        ]
    }
}


def build() -> object:
    return helm.build_chart_from_versions(
        name="metallb",
        versions=versions,
        values=values,
    )


def ci() -> object:
    return 
