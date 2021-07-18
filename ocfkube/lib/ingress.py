from .resource import Resource
from .service import Service


class Ingress(Resource):
    def from_service(service: Service, domain: str):
        if len(service["spec"]["ports"] != 1):
            raise ValueError("Can only create an ingress for a service with one port")

        port_number = service["spec"]["ports"][0]["port"]

        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": service.name + "-ingress",
                "namespace": service.namespace,
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
                                        "serviceName": "argocd-server",
                                        "servicePort": port_number,
                                    },
                                    "pathType": "ImplementationSpecific",
                                }
                            ]
                        },
                    }
                ],
                "tls": [
                    {"hosts": [domain], "secretName": service.name + "-ingress-tls"}
                ],
            },
        }
