from ocfkube.utils import helm
from ocfkube.utils import versions

values = {
    "kubeProxyReplacement": "strict",
    "k8sServiceHost": "127.0.0.1",
    "k8sServicePort": "6443",
    "nativeRoutingCIDR": "10.0.0.0/8",
    "containerRuntime": {
        "integration": "crio",
    },
    "autoDirectNodeRoutes": True,
    "tunnel": "disabled",
    "loadBalancer": {
        "algorithm": "maglev",
        # TODO: Look into switching to full DSR...
        "mode": "hybrid",
        "acceleration": "native",
    },
    "config": {
        "sessionAffinity": True,
    },
    "hubble": {
        "tls": {"auto": {"method": "cronJob"}},
        "listenAddress": ":4244",
        "relay": {"enabled": True},
        "ui": {"enabled": True},
    },
}


def build() -> object:
    return helm.build_chart_from_versions(
        name="cilium",
        versions=versions,
        values=values,
    )
