import os
import shutil
import tempfile
import yaml
from subprocess import run, PIPE

# TODO: This is hardcoded, but we can grab it from the k8s API instead.
capabilities = [
    "acme.cert-manager.io/v1",
    "acme.cert-manager.io/v1alpha2",
    "acme.cert-manager.io/v1alpha3",
    "acme.cert-manager.io/v1beta1",
    "admissionregistration.k8s.io/v1",
    "admissionregistration.k8s.io/v1beta1",
    "apiextensions.k8s.io/v1",
    "apiextensions.k8s.io/v1beta1",
    "apiregistration.k8s.io/v1",
    "apiregistration.k8s.io/v1beta1",
    "apps/v1",
    "argoproj.io/v1alpha1",
    "authentication.k8s.io/v1",
    "authentication.k8s.io/v1beta1",
    "authorization.k8s.io/v1",
    "authorization.k8s.io/v1beta1",
    "autoscaling/v1",
    "autoscaling/v2beta1",
    "autoscaling/v2beta2",
    "batch/v1",
    "batch/v1beta1",
    "ceph.rook.io/v1",
    "cert-manager.io/v1",
    "cert-manager.io/v1alpha2",
    "cert-manager.io/v1alpha3",
    "cert-manager.io/v1beta1",
    "certificates.k8s.io/v1",
    "certificates.k8s.io/v1beta1",
    "cilium.io/v2",
    "coordination.k8s.io/v1",
    "coordination.k8s.io/v1beta1",
    "discovery.k8s.io/v1beta1",
    "events.k8s.io/v1",
    "events.k8s.io/v1beta1",
    "extensions/v1beta1",
    "fission.io/v1",
    "keycloak.org/v1alpha1",
    "networking.k8s.io/v1",
    "networking.k8s.io/v1beta1",
    "node.k8s.io/v1beta1",
    "objectbucket.io/v1alpha1",
    "ocf.io/v1",
    "policy/v1beta1",
    "projectcontour.io/v1",
    "projectcontour.io/v1alpha1",
    "rbac.authorization.k8s.io/v1",
    "rbac.authorization.k8s.io/v1beta1",
    "ricoberger.de/v1alpha1",
    "rook.io/v1alpha2",
    "scheduling.k8s.io/v1",
    "scheduling.k8s.io/v1beta1",
    "storage.k8s.io/v1",
    "storage.k8s.io/v1beta1",
    "v1",
]


def build_chart_from_versions(
    name: str,
    versions: object,
    values: dict,
):
    return build_chart(
        repo_url=versions[name]["helm"],
        chart_name=versions[name].get("chart", name),
        namespace=name,
        version=versions[name]["version"],
        values=values,
    )


def build_chart(
    repo_url: str,
    chart_name: str,
    namespace: str,
    version: str,
    values: dict,
) -> list:
    if shutil.which("helm") is None:
        raise RuntimeError("You must install Helm to use this script.")

    values_file, values_file_name = tempfile.mkstemp(suffix=".yml")
    with open(values_file_name, "w") as f:
        f.write(yaml.dump(values))

    tpl_args = [
        "helm",
        "template",
        "-n",
        namespace,
        "--repo",
        repo_url,
        "--version",
        version,
        "--values",
        values_file_name,
        "--include-crds",
        "--name-template",
        # the helm release name
        # sometimes used in resource names
        f"ocf-{namespace}",
        "--api-versions",
        ", ".join(capabilities),
        chart_name,
    ]
    r = run(
        tpl_args,
        check=True,
        stdout=PIPE,
    ).stdout

    os.close(values_file)
    return list(yaml.safe_load_all(r))
