from transpire import helm

from apps.versions import versions

values = {
    "kubeProxyReplacement": "strict",
    "k8sServiceHost": "k8s0.ocf.io",
    "k8sServicePort": "6443",
    "nativeRoutingCIDR": "10.0.0.0/8",
    "containerRuntime": {
        "integration": "crio",
    },
    "hubble": {
        "tls": {"auto": {"method": "cronJob"}},
        "listenAddress": ":4244",
        "relay": {"enabled": True},
        "ui": {"enabled": True},
    },
    "bpf": {
        "masquerade": True,
    },
}

name = "cilium"

def objects():
    yield from helm.build_chart_from_versions(
        name="cilium",
        versions=versions,
        values=values,
    )
