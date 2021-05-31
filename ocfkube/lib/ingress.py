def ingress_for_service_with_tls(
    name: str,
    service_name: str,
    service_port: int,
    domain: str,
) -> object:
    return {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": "argocd-server-http-ingress",
            "namespace": "argocd",
            "annotations": {
                "cert-manager.io/cluster-issuer": "letsencrypt",
                "ingress.kubernetes.io/force-ssl-redirect": "true",
                "kubernetes.io/tls-acme": "true",
            },
        },
        "spec": {
            "rules": [
                {
                    "host": "argo.ocf.berkeley.edu",
                    "http": {
                        "paths": [
                            {
                                "backend": {
                                    "serviceName": "argocd-server",
                                    "servicePort": 80,
                                },
                                "pathType": "ImplementationSpecific",
                            }
                        ]
                    },
                }
            ],
            "tls": [{"hosts": ["argo.ocf.berkeley.edu"], "secretName": "argocd-tls"}],
        },
    }
