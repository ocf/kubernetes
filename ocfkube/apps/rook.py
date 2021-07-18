from ocfkube.utils import helm
from ocfkube.utils import versions

values = {"image": {"tag": "v1.5.1"}}

ceph_yaml = {
    "apiVersion": "ceph.rook.io/v1",
    "kind": "CephCluster",
    "metadata": {
        "name": "ceph",
        "namespace": "rook-ceph",
        "annotations": {"argocd.argoproj.io/compare-options": "IgnoreExtraneous"},
    },
    "spec": {
        "cephVersion": {"image": "ceph/ceph:v15.2.6"},
        "dataDirHostPath": "/var/lib/rook",
        "mon": {"count": 3, "allowMultiplePerNode": False},
        "storage": {
            "useAllNodes": False,
            "useAllDevices": False,
            "nodes": [
                {
                    "name": "jaws",
                    "devices": [
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K932843P"
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K933151M"
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K934154M"
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K934284J"
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K934288X"
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K937582P"
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K943700W"
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K944017K"
                        },
                    ],
                }
            ],
        },
    },
}
storageclass_yaml = [
    {
        "apiVersion": "ceph.rook.io/v1",
        "kind": "CephBlockPool",
        "metadata": {"name": "replicapool", "namespace": "rook-ceph"},
        "spec": {
            "failureDomain": "host",
            "replicated": {"size": 2, "requireSafeReplicaSize": True},
        },
    },
    {
        "apiVersion": "storage.k8s.io/v1",
        "kind": "StorageClass",
        "metadata": {
            "name": "rook-ceph-block",
            "annotations": {"storageclass.kubernetes.io/is-default-class": "true"},
        },
        "provisioner": "rook-ceph.rbd.csi.ceph.com",
        "parameters": {
            "clusterID": "rook-ceph",
            "pool": "replicapool",
            "imageFormat": "2",
            "imageFeatures": "layering",
            "csi.storage.k8s.io/provisioner-secret-name": "rook-csi-rbd-provisioner",
            "csi.storage.k8s.io/provisioner-secret-namespace": "rook-ceph",
            "csi.storage.k8s.io/controller-expand-secret-name": "rook-csi-rbd-provisioner",
            "csi.storage.k8s.io/controller-expand-secret-namespace": "rook-ceph",
            "csi.storage.k8s.io/node-stage-secret-name": "rook-csi-rbd-node",
            "csi.storage.k8s.io/node-stage-secret-namespace": "rook-ceph",
            "csi.storage.k8s.io/fstype": "ext4",
        },
        "allowVolumeExpansion": True,
        "reclaimPolicy": "Delete",
    },
]


def build() -> object:
    return (
        helm.build_chart_from_versions(
            name="rook",
            versions=versions,
            values=values,
        )
        + [ceph_yaml]
        + storageclass_yaml
    )
