from ocfkube.utils import helm
from ocfkube.utils import versions

values = {
    "alertmanager": {
        "enabled": True,
        "ingress": {
            "enabled": True,
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "ingress.kubernetes.io/force-ssl-redirect": "true",
                "kubernetes.io/tls-acme": "true",
            },
            "hosts": ["alerts.ocf.berkeley.edu"],
            "tls": [{"hosts": ["alerts.ocf.berkeley.edu"], "secretName": "alerts-tls"}],
        },
    },
    "nodeExporter": {"enabled": False},
    "prometheus": {
        "ingress": {
            "enabled": True,
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "ingress.kubernetes.io/force-ssl-redirect": "true",
                "kubernetes.io/tls-acme": "true",
            },
            "hosts": ["prom.ocf.berkeley.edu"],
            "tls": [{"hosts": ["prom.ocf.berkeley.edu"], "secretName": "prom-tls"}],
        }
    },
    "grafana": {
        "ingress": {
            "enabled": True,
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "ingress.kubernetes.io/force-ssl-redirect": "true",
                "kubernetes.io/tls-acme": "true",
            },
            "hosts": ["graf.ocf.berkeley.edu"],
            "tls": [{"hosts": ["graf.ocf.berkeley.edu"], "secretName": "graf-tls"}],
        }
    },
}


def build() -> object:
    return helm.build_chart_from_versions(
        name="prometheus",
        versions=versions,
        values=values,
    )
