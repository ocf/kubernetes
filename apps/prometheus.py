from transpire import helm
from transpire.utils import get_versions

name = "prometheus"
values = {
    "defaultRules": {
        "rules": {
            # We don't run kube-proxy, Cilium handles that.
            "kubeProxy": False,
        },
    },
    "nodeExporter": {"enabled": True},
    # TODO: Setup alertmanager.
    "alertmanager": {
        "enabled": False,
        "ingress": {
            "enabled": False,
            "ingressClassName": "contour",
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "ingress.kubernetes.io/force-ssl-redirect": "true",
                "kubernetes.io/tls-acme": "true",
            },
            "hosts": ["alerts.ocf.berkeley.edu"],
            "tls": [{"hosts": ["alerts.ocf.berkeley.edu"], "secretName": "alerts-tls"}],
        },
    },
    "prometheus": {
        "ingress": {
            "enabled": True,
            "ingressClassName": "contour",
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "ingress.kubernetes.io/force-ssl-redirect": "true",
                "kubernetes.io/tls-acme": "true",
            },
            "hosts": ["prom.ocf.berkeley.edu"],
            "tls": [{"hosts": ["prom.ocf.berkeley.edu"], "secretName": "prom-tls"}],
        },
        "prometheusSpec": {"serviceMonitorSelectorNilUsesHelmValues": False},
    },
    "grafana": {
        "ingress": {
            "enabled": True,
            "ingressClassName": "contour",
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "ingress.kubernetes.io/force-ssl-redirect": "true",
                "kubernetes.io/tls-acme": "true",
            },
            "hosts": ["graf.ocf.berkeley.edu"],
            "tls": [{"hosts": ["graf.ocf.berkeley.edu"], "secretName": "graf-tls"}],
        },
    },
}


def objects():
    yield from helm.build_chart_from_versions(
        name="prometheus", versions=get_versions(__file__), values=values,
    )
