from transpire import helm

from apps.versions import versions

values = {
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
    # <https://github.com/cilium/cilium/issues/22949>
    "image": {
        "repository": "quay.io/cilium/cilium-ci",
        "tag": "0d91314f403cb906426bd6c13a1e5e0839be7df8",
        "digest": "sha256:f217be397d00865f0c61964ea9be944294b9e8baaf0126185ff940b1433bb510",
    },
    # <https://github.com/cilium/cilium/issues/22668>
    "operator": {
        "image": {
            "override": "quay.io/cilium/operator-generic-ci@sha256:a26bcd90fb3b665009aedb551d6efa14e543290441f7402444cad10595ae4a45",
        },
    },
}

name = "cilium"

def objects():
    yield from helm.build_chart_from_versions(
        name="cilium",
        versions=versions,
        values=values,
    )
