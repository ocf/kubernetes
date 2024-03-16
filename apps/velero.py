from transpire import helm
from transpire.utils import get_versions

name = "velero"

values = {
    # At least one plugin provider image is required.
    "initContainers": [
        {
            "name": "velero-plugin-for-csi",
            "image": "velero/velero-plugin-for-csi:v0.7.0",
            "imagePullPolicy": "IfNotPresent",
            "volumeMounts": [
                {
                    "mountPath": "/target",
                    "name": "plugins",
                },
            ],
        },
        {
            "name": "velero-plugin-for-aws",
            # for S3-compatible API
            "image": "velero/velero-plugin-for-aws:v1.9.0",
            "imagePullPolicy": "IfNotPresent",
            "volumeMounts": [
                {
                    "mountPath": "/target",
                    "name": "plugins",
                },
            ],
        },
    ],
    "deployNodeAgent": "true",
    "configuration": {
        "backupStorageLocation": [
            {
                "name": "default",
                "provider": "velero.io/aws",
                "bucket": "velero",
                "credential": {"key": "aws-config", "name": "minio-credentials"},
                "config": {
                    "region": "minio",
                    "s3ForcePathStyle": "true",
                    "s3Url": "http://hal.ocf.berkeley.edu:9000",
                },
            }
        ],
        "volumeSnapshotLocation": [],
    },
}


def objects():
    yield {
        "apiVersion": "ricoberger.de/v1alpha1",
        "kind": "VaultSecret",
        "metadata": {"name": "minio-credentials"},
        "spec": {
            "keys": ["aws-config"],
            "path": f"kvv2/{name}/minio-credentials",
            "type": "Opaque",
        },
    }

    yield from helm.build_chart_from_versions(
        name="velero",
        versions=get_versions(__file__),
        values=values,
    )

