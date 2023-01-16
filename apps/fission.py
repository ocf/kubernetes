from transpire import helm
from transpire.resources import Secret
from transpire.surgery import edit_manifests, make_edit_manifest
from transpire.utils import get_versions

name = "fission"


def objects():
    # TODO: The helm chart doesn't come with CRDs.
    # kubectl create -k "github.com/fission/fission/crds/v1?ref=v1.17.0"

    s3_secret = "storage-s3-key"
    yield Secret.simple(
        name=s3_secret,
        string_data={
            "STORAGE_S3_ACCESS_KEY_ID": "",
            "STORAGE_S3_SECRET_ACCESS_KEY": "",
        },
    )

    def inject_secrets(storagesvc: dict) -> dict:
        envs = storagesvc["spec"]["template"]["spec"]["containers"][0]["env"]
        storagesvc["spec"]["template"]["spec"]["containers"][0]["env"] = list(
            filter(
                lambda x: not (
                    x["name"] == "STORAGE_S3_ACCESS_KEY_ID"
                    or x["name"] == "STORAGE_S3_SECRET_ACCESS_KEY"
                ),
                envs,
            )
        )
        storagesvc["spec"]["template"]["spec"]["containers"][0]["env"].extend(
            [
                {
                    "name": "STORAGE_S3_ACCESS_KEY_ID",
                    "valueFrom": {
                        "secretKeyRef": {
                            "name": s3_secret,
                            "key": "STORAGE_S3_ACCESS_KEY_ID",
                        }
                    },
                },
                {
                    "name": "STORAGE_S3_SECRET_ACCESS_KEY",
                    "valueFrom": {
                        "secretKeyRef": {
                            "name": s3_secret,
                            "key": "STORAGE_S3_SECRET_ACCESS_KEY",
                        }
                    },
                },
            ]
        )
        return storagesvc

    yield from edit_manifests(
        manifests=helm.build_chart_from_versions(
            name=name,
            versions=get_versions(__file__),
            values={
                "routerServiceType": "ClusterIP",
                "persistence": {
                    "enabled": True,
                    "storageType": "s3",
                    "s3": {
                        "bucketName": "ocf-fission",
                        # These get injected into the Deployment directly, do not use!
                        # "accessKeyId": "replaced-in-vault",
                        # "secretAccessKey": "replaced-in-vault",
                        "endPoint": "https://o3.ocf.berkeley.edu",
                    },
                },
                # TODO: Configure OpenTelemetry...
                # "openTelemetry": {},
                "serviceMonitor": {"enabled": True},
                "podMonitor": {"enabled": True},
                # RabbitMQ Connector
                "mqt_keda": {"enabled": True},
                # I have no idea how this works, but neat.
                "grafana": {
                    "namespace": "prometheus",
                    "dashboards": {"enable": True},
                },
            },
        ),
        edits={
            ("Deployment", "storagesvc"): inject_secrets,
        },
    )
