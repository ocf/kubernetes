from apps.versions import versions

name = "arcanum"

def objects():
    # NOTE: arcanum-secret is manually created, as it has a secret key that we need for bootstrap.
    manifests = [
            {
                "apiVersion": "v1",
                "kind": "ServiceAccount",
                "metadata": {"name": "arcanum-sa", "namespace": "arcanum"},
                "automountServiceAccountToken": True,
            },
            {
                "kind": "ClusterRole",
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "metadata": {"name": "arcanum-cr"},
                "rules": [
                    {
                        "apiGroups": ["arcanum.njha.dev"],
                        "resources": ["syncedsecrets", "syncedsecrets/status"],
                        "verbs": ["get", "watch", "list", "patch"],
                    },
                    {
                        "apiGroups": ["events.k8s.io"],
                        "resources": ["events"],
                        "verbs": ["create"],
                    },
                    {
                        "apiGroups": [""],
                        "resources": ["secrets"],
                        "verbs": ["create", "patch"],
                    },
                ],
            },
            {
                "kind": "ClusterRoleBinding",
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "metadata": {"name": "arcanum-binding"},
                "subjects": [
                    {
                        "kind": "ServiceAccount",
                        "namespace": "arcanum",
                        "name": "arcanum-sa",
                    }
                ],
                "roleRef": {
                    "kind": "ClusterRole",
                    "name": "arcanum-cr",
                    "apiGroup": "rbac.authorization.k8s.io",
                },
            },
            {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": "arcanum",
                    "namespace": "arcanum",
                    "labels": {"app": "arcanum"},
                },
                "spec": {
                    "ports": [
                        {
                            "port": 80,
                            "targetPort": 8080,
                            "protocol": "TCP",
                            "name": "http",
                        }
                    ],
                    "selector": {"app": "arcanum"},
                },
            },
            {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {
                    "name": "arcanum",
                    "namespace": "arcanum",
                    "labels": {"app": "arcanum"},
                },
                "spec": {
                    "replicas": 1,
                    "selector": {"matchLabels": {"app": "arcanum"}},
                    "template": {
                        "metadata": {
                            "labels": {"app": "arcanum"},
                            "annotations": {
                                "prometheus.io/scrape": "true",
                                "prometheus.io/port": "8080",
                            },
                        },
                        "spec": {
                            "serviceAccountName": "arcanum-sa",
                            "containers": [
                                {
                                    "name": "arcanum",
                                    "image": str(versions["arcanum"]["image"]),
                                    "env": [
                                        {
                                            "name": "ARCANUM_VLT_HOST",
                                            "valueFrom": {
                                                "secretKeyRef": {
                                                    "name": "arcanum-secret",
                                                    "key": "ARCANUM_VLT_HOST",
                                                }
                                            },
                                        },
                                        {
                                            "name": "ARCANUM_VLT_PATH",
                                            "valueFrom": {
                                                "secretKeyRef": {
                                                    "name": "arcanum-secret",
                                                    "key": "ARCANUM_VLT_PATH",
                                                }
                                            },
                                        },
                                        {
                                            "name": "ARCANUM_VLT_TOKEN",
                                            "valueFrom": {
                                                "secretKeyRef": {
                                                    "name": "arcanum-secret",
                                                    "key": "ARCANUM_VLT_TOKEN",
                                                }
                                            },
                                        },
                                        {
                                            "name": "ARCANUM_ENC_KEY",
                                            "valueFrom": {
                                                "secretKeyRef": {
                                                    "name": "arcanum-secret",
                                                    "key": "ARCANUM_ENC_KEY",
                                                }
                                            },
                                        },
                                    ],
                                    "imagePullPolicy": "IfNotPresent",
                                    "resources": {
                                        "limits": {"cpu": "200m", "memory": "256Mi"},
                                        "requests": {"cpu": "50m", "memory": "100Mi"},
                                    },
                                    "ports": [
                                        {
                                            "name": "http",
                                            "containerPort": 8080,
                                            "protocol": "TCP",
                                        }
                                    ],
                                    "readinessProbe": {
                                        "httpGet": {"path": "/health", "port": "http"},
                                        "initialDelaySeconds": 5,
                                        "periodSeconds": 5,
                                    },
                                }
                            ],
                        },
                    },
                },
            },
        ]
    
    for manifest in manifests:
        yield manifest

    manifests = [
            {
                "apiVersion": "apiextensions.k8s.io/v1",
                "kind": "CustomResourceDefinition",
                "metadata": {"name": "syncedsecrets.arcanum.njha.dev"},
                "spec": {
                    "group": "arcanum.njha.dev",
                    "names": {
                        "categories": [],
                        "kind": "SyncedSecret",
                        "plural": "syncedsecrets",
                        "shortNames": [],
                        "singular": "syncedsecret",
                    },
                    "scope": "Namespaced",
                    "versions": [
                        {
                            "additionalPrinterColumns": [],
                            "name": "v1",
                            "schema": {
                                "openAPIV3Schema": {
                                    "description": "Auto-generated derived type for SyncedSecretSpec via `CustomResource`",
                                    "properties": {
                                        "spec": {
                                            "description": "Our Foo custom resource spec",
                                            "properties": {
                                                "data": {
                                                    "additionalProperties": {
                                                        "type": "string"
                                                    },
                                                    "type": "object",
                                                },
                                                "pub_key": {"type": "string"},
                                            },
                                            "required": ["data", "pub_key"],
                                            "type": "object",
                                        },
                                        "status": {
                                            "nullable": True,
                                            "properties": {
                                                "last_updated": {
                                                    "format": "date-time",
                                                    "nullable": True,
                                                    "type": "string",
                                                },
                                                "reconciled": {
                                                    "nullable": True,
                                                    "type": "boolean",
                                                },
                                            },
                                            "type": "object",
                                        },
                                    },
                                    "required": ["spec"],
                                    "title": "SyncedSecret",
                                    "type": "object",
                                }
                            },
                            "served": True,
                            "storage": True,
                            "subresources": {"status": {}},
                        }
                    ],
                },
            }
        ]
    
    for manifest in manifests:
        yield manifest

