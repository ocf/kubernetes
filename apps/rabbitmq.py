from typing import Generator

from transpire import helm

from apps.versions import versions

name = "rabbitmq"


def objects() -> Generator[dict, None, None]:
    # <https://github.com/bitnami/charts/tree/main/bitnami/rabbitmq-cluster-operator>
    values = {
        "clusterOperator": {
            "metrics": {
                "enabled": True,
                "serviceMonitor": {
                    "enabled": True,
                },
            },
        },
        "msgTopologyOperator": {
            "metrics": {
                "enabled": True,
                "serviceMonitor": {
                    "enabled": True,
                },
            },
        },
        "useCertManager": True,
    }
    yield from helm.build_chart_from_versions(
        name=name,
        versions=versions,
        values=values,
    )

    # <https://www.rabbitmq.com/kubernetes/operator/using-operator.html>
    yield {
        "apiVersion": "rabbitmq.com/v1beta1",
        "kind": "RabbitmqCluster",
        "metadata": {"name": "rabbitmq"},
        "spec": {
            # <https://www.rabbitmq.com/kubernetes/operator/using-operator.html#vault-default-user>
            "secretBackend": {
                "vault": {
                    "role": "rabbitmq",
                    "annotations": {
                        "vault.hashicorp.com/template-static-secret-render-interval": "60s",
                        "vault.hashicorp.com/service": "https://vault.ocf.berkeley.edu/",
                    },
                    "defaultUserPath": "kvv2/data/rabbitmq/rabbitmq-admin-userpass",
                    "tls": {
                        "pkiIssuerPath": "pki/issue/rabbitmq",
                    },
                },
            },
        },
    }
