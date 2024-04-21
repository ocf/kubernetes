from transpire import helm
from transpire.utils import get_versions

name = "odoo"


def objects():
    yield {
        "apiVersion": "acid.zalan.do/v1",
        "kind": "postgresql",
        "metadata": {"name": "ocf-odoo-db"},
        "spec": {
            "teamId": "ocf",
            "volume": {
                "size": "128Gi",
                "storageClass": "rbd-nvme",
            },
            "numberOfInstances": 1,
            "users": {"odoo": ["superuser", "createdb"]},
            "databases": {"odoo": "odoo"},
            "postgresql": {"version": "15"},
        },
    }

    yield from helm.build_chart_from_versions(
        name=name,
        versions=get_versions(__file__),
        values={
            # Database
            "postgresql": {
                "enabled": False,
            },
            "externalDatabase": {
                "host": "ocf-odoo-db",
                "port": 5432,
                "user": "odoo",
                "database": "odoo",
                "existingSecret": "odoo.ocf-odoo-db.credentials.postgresql.acid.zalan.do",
                "existingSecretPasswordKey": "password",
            },
            # Mail
            "smtpHost": "smtp.ocf.berkeley.edu",
            # Ingress
            "ingress": {
                "enabled": True,
                "ingressClassName": "contour",
                "annotations": {
                    "cert-manager.io/cluster-issuer": "letsencrypt",
                    "ingress.kubernetes.io/force-ssl-redirect": "true",
                    "kubernetes.io/tls-acme": "true",
                },
                "hostname": "odoo.ocf.berkeley.edu",
                "tls": True,
            },
        },
    )
