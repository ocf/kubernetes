import yaml

from ocfkube.utils import helm
from ocfkube.utils import versions

values = {
    "kubeProxyReplacement": "strict",
    "k8sServiceHost": "127.0.0.1",
    "k8sServicePort": "6443",
    "nativeRoutingCIDR": "10.0.0.0/8",
    "containerRuntime": {
        "integration": "containerd",
        "socketPath": "/run/containerd/containerd.sock",
    },
    "hubble": {"tls": {"auto": {"method": "cronJob"}}},
}


def build() -> object:
    return helm.build_chart_from_versions(
        name="cilium",
        versions=versions,
        values=values,
    )
