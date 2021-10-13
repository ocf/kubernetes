from __future__ import annotations

from .resource import Resource
from .service import Service


class Ingress(Resource):
    @classmethod
    def from_service(_cls, service: Service, domain: str) -> Ingress:
        if len(service["spec"]["ports"] != 1):
            raise ValueError("Can only create an ingress for a service with one port")

        port = service["spec"]["ports"][0]["port"]

        return Ingress.from_service_name(service.name, port, domain)

    @classmethod
    def from_service_name(_cls, service_name: str, port: int, domain: str) -> Ingress:
        return Ingress(
            {
                "apiVersion": "networking.k8s.io/v1",
                "kind": "Ingress",
                "metadata": {
                    "name": service_name + "-ingress",
                    "annotations": {
                        "cert-manager.io/cluster-issuer": "letsencrypt",
                        "ingress.kubernetes.io/force-ssl-redirect": "true",
                        "kubernetes.io/tls-acme": "true",
                    },
                },
                "spec": {
                    "rules": [
                        {
                            "host": domain,
                            "http": {
                                "paths": [
                                    {
                                        "backend": {
                                            "service": {
                                                "name": service_name,
                                                "port": {
                                                    "number": port,
                                                },
                                            },
                                        },
                                        "pathType": "ImplementationSpecific",
                                    },
                                ],
                            },
                        },
                    ],
                    "tls": [
                        {
                            "hosts": [domain],
                            "secretName": service_name + "-ingress-tls",
                        },
                    ],
                },
            },
            check_namespace=False,
        )
