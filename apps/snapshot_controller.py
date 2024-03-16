from transpire import kustomize
from transpire.utils import get_versions

name = "snapshot-controller"
namespace = "kube-system"

def objects():
    yield from kustomize.build_kustomization_from_versions(
        name="snapshot-controller-crds",
        versions=get_versions(__file__),
    )

    yield from kustomize.build_kustomization_from_versions(
        name="snapshot-controller",
        versions=get_versions(__file__),
    )
