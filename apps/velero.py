from transpire import helm
from transpire.utils import get_versions

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
    "configuration": {
        "backupStorageLocation": [],
        "volumeSnapshotLocation": [],
    },
}

name = "velero"


def objects():
    yield from helm.build_chart_from_versions(
        name="velero",
        versions=get_versions(__file__),
        values=values,
    )

