from pkgutil import iter_modules
from transpire.dsl import emit


def application_for_name(app_name: str) -> dict:
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
                "path": f"manifests/{app_name}",
            },
            "syncPolicy": {
                "syncOptions": [
                    "CreateNamespace=true",
                ],
            },
        },
    }


def build() -> None:
    for module in iter_modules(__import__("apps").__path__):
        if module.name != "bootstrap":
            emit(application_for_name(module.name))
