from transpire import helm

from apps.versions import versions

values = {
    "kubeProxyReplacement": "strict",
    "k8sServiceHost": "dna.ocf.io",
    "k8sServicePort": "6443",
    "hubble": {
        "tls": {"auto": {"method": "cronJob"}},
        "listenAddress": ":4244",
        "relay": {"enabled": True},
        "ui": {"enabled": True},
    },
    "ipam": {
        "mode": "cluster-pool",
        "operator": {
            "clusterPoolIPv4PodCIDRList": ["10.244.0.0/16"],
            "clusterPoolIPv6PodCIDRList": ["2607:f140:8801:1::/112"],
        },
    },
    "bpf": {
      "masquerade": True,
    },
    # needed for bpf masquerade
    "enableIPv6Masquerade": False,
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
    "ingressController": {
        "enabled": True,
        "loadbalancerMode": "shared",
        "enforceHttps": True,
        "service": {
            # Hardcode the shared loadbalancer IP, since lots of external DNS points to it and it should not change easily.
            "annotations": { "metallb.universe.tf/loadBalancerIPs": "169.229.226.81,2607:f140:8801::1:81" },
        },
        # first two are default values, we aren't using them as of 2022
        "ingressLBAnnotationPrefixes": ['service.beta.kubernetes.io', 'service.kubernetes.io', 'metallb.universe.tf'],
    },
}

name = "cilium"

def objects():
    yield from helm.build_chart_from_versions(
        name="cilium",
        versions=versions,
        values=values,
    )
