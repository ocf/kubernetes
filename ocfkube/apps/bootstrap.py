from pkgutil import iter_modules


def application_for_name(app_name: str) -> object:
    new_app_name = app_name.replace("_", "-")

    return {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Application",
        "metadata": {"name": new_app_name, "namespace": "argocd"},
        "spec": {
            "project": "default",
            "destination": {
                "server": "https://kubernetes.default.svc",
                "namespace": new_app_name,
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
