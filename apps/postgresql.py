from transpire.dsl import helm
from apps.versions import versions

from transpire.dsl import emit

values = {
    "postgresql": {"existingSecret": "postgresql-pw", "replicaCount": 1},
    "pgpool": {"existingSecret": "pgpool-pw"},
}

secret = [
    {
        "apiVersion": "ricoberger.de/v1alpha1",
        "kind": "VaultSecret",
        "metadata": {"name": "pgpool-pw"},
        "spec": {
            "keys": ["admin_password"],
            "templates": {"admin-password": "{% .Secrets.admin_password %}"},
            "path": "kvv2/postgresql",
            "type": "Opaque",
        },
    },
    {
        "apiVersion": "ricoberger.de/v1alpha1",
        "kind": "VaultSecret",
        "metadata": {"name": "postgresql-pw"},
        "spec": {
            "keys": ["postgresql_password", "repmgr_password"],
            "templates": {
                "postgresql-password": "{% .Secrets.postgresql_password %}",
                "repmgr-password": "{% .Secrets.repmgr_password %}",
            },
            "path": "kvv2/postgresql",
            "type": "Opaque",
        },
    },
]


def build() -> None:
    emit(
        helm.build_chart_from_versions(
            name="postgresql",
            versions=versions,
            values=values,
        )
        + secret
    )
