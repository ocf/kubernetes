name = "gvisor"


def objects():
    yield {
        "apiVersion": "node.k8s.io/v1",
        "kind": "RuntimeClass",
        "metadata": {"name": "gvisor"},
        "handler": "runsc",
    }

    # Test pod
    yield {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": "nginx-gvisor"},
        "spec": {
            "runtimeClassName": "gvisor",
            "containers": [{"name": "nginx", "image": "docker.io/nginx"}],
        },
    }
