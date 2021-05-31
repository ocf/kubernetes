from pkgutil import iter_modules


def application_for_name(app_name: str) -> object:
    return {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Application",
        "metadata": {"name": app_name, "namespace": "argocd"},
        "spec": {
            "project": "default",
            "destination": {
                "server": "https://kubernetes.default.svc",
                "namespace": app_name,
            },
            "source": {
                "repoURL": "https://github.com/ocf/kubernetes",
                "path": ".",
                "plugin": {"name": "python"},
            },
            "syncPolicy": {
                "syncOptions": [
                    "CreateNamespace=true",
                ],
            },
        },
    }


def build() -> object:

    return [
        application_for_name(module.name)
        for module in iter_modules(__import__("ocfkube").apps.__path__)
        if module.name != "bootstrap"
    ]
