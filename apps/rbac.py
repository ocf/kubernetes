name = "ocf-rbac"


def objects():
    yield {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRoleBinding",
        "metadata": {
            "name": "ocf-viewer",
        },
        "subjects": [
            {
                "apiGroup": "rbac.authorization.k8s.io",
                "kind": "Group",
                "name": "ocf:viewer",
            }
        ],
        "roleRef": {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "ClusterRole",
            "name": "view",
        },
    }
