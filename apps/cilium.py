from transpire import helm
from transpire.utils import get_versions

name = "cilium"


def objects():
    yield from helm.build_chart_from_versions(
        name="cilium",
        versions=get_versions(__file__),
        values={
            "kubeProxyReplacement": "strict",
            "k8sServiceHost": "dna.ocf.io",
            "k8sServicePort": "6443",
            "hubble": {
                "tls": {"auto": {"method": "cronJob"}},
                "listenAddress": ":4244",
            },
            "ipam": {
                "mode": "cluster-pool",
                "operator": {
                    "clusterPoolIPv4PodCIDRList": ["10.244.0.0/16"],
                    "clusterPoolIPv6PodCIDRList": ["2607:f140:8801:1::/112"],
                },
            },
            # "bpf": {
            #     "masquerade": True,
            # },
            # needed for bpf masquerade
            # "enableIPv6Masquerade": False,
            "tunnel": "disabled",
            "autoDirectNodeRoutes": True,
            "endpointRoutes": {
                "enabled": True,
            },
            "ipv4NativeRoutingCIDR": "10.244.0.0/16",
            "ipv6NativeRoutingCIDR": "2607:f140:8801:1::/112",
            "ipv6": {
                "enabled": True,
            },
            "ipv4": {
                "enabled": True,
            },
            "k8s": {
                "requireIPv6PodCIDR": True,
                "requireIPv4PodCIDR": True,
            },
        },
    )
