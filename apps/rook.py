from transpire import helm

from apps.versions import versions

values = {
    "image": {
        "tag": "v1.10.6",
    },
    # <https://rook.io/docs/rook/v1.10/CRDs/Cluster/ceph-cluster-crd/?h=stack#network-configuration-settings>
    "network": {
        "dualStack": True,
    },
    # <https://rook.io/docs/rook/v1.10/Storage-Configuration/Monitoring/ceph-dashboard/?h=dashboard#enable-the-ceph-dashboard>
    "dashboard": {
        "enabled": True,
    },
    # <https://rook.io/docs/rook/v1.10/Getting-Started/Prerequisites/prerequisites/?h=nixos#nixos>
    # <https://github.com/rook/rook/blob/v1.10.6/deploy/charts/rook-ceph/values.yaml#L141>
    "csi": {
        "csiRBDPluginVolume": [
            {
                "name": "lib-modules",
                "hostPath": {"path": "/run/booted-system/kernel-modules/lib/modules/"},
            },
            {"name": "host-nix", "hostPath": {"path": "/nix"}},
        ],
        "csiRBDPluginVolumeMount": [
            {"name": "host-nix", "mountPath": "/nix", "readOnly": True}
        ],
        "csiCephFSPluginVolume": [
            {
                "name": "lib-modules",
                "hostPath": {"path": "/run/booted-system/kernel-modules/lib/modules/"},
            },
            {"name": "host-nix", "hostPath": {"path": "/nix"}},
        ],
        "csiCephFSPluginVolumeMount": [
            {"name": "host-nix", "mountPath": "/nix", "readOnly": True}
        ],
    },
}

name = "rook"

nucleusDevices = (
    [
        {
            "config": {"deviceClass": "nvme"},
            "name": "/dev/disk/by-path/pci-0000:02:00.0-nvme-1",
        },
        {
            "config": {"deviceClass": "nvme"},
            "name": "/dev/disk/by-path/pci-0000:41:00.0-nvme-1",
        },
    ],
)

ceph_cluster = {
    "apiVersion": "ceph.rook.io/v1",
    "kind": "CephCluster",
    "metadata": {
        "name": "ceph",
        "namespace": "rook",
        "annotations": {"argocd.argoproj.io/compare-options": "IgnoreExtraneous"},
    },
    "spec": {
        "cephVersion": {"image": "quay.io/ceph/ceph:v17.2.5"},
        "dataDirHostPath": "/var/lib/rook",
        "mon": {"count": 3, "allowMultiplePerNode": False},
        "dashboard": {
            "enabled": True,
        },
        "storage": {
            "nodes": [
                {
                    "devices": nucleusDevices,
                    "name": "adenine",
                },
                {
                    "devices": nucleusDevices,
                    "name": "guanine",
                },
                {
                    "devices": nucleusDevices,
                    "name": "cytosine",
                },
                {"name": "thymine"},
            ],
            "useAllDevices": False,
            "useAllNodes": False,
        },
    },
}

storageclass_yaml = [
    {
        "apiVersion": "ceph.rook.io/v1",
        "kind": "CephBlockPool",
        "metadata": {"name": "replicapool", "namespace": "rook"},
        "spec": {
            "failureDomain": "host",
            "replicated": {"size": 2, "requireSafeReplicaSize": True},
            "deviceClass": "ssd",
        },
    },
    {
        "apiVersion": "storage.k8s.io/v1",
        "kind": "StorageClass",
        "metadata": {
            "name": "rook-ceph-block",
            "annotations": {"storageclass.kubernetes.io/is-default-class": "true"},
        },
        "provisioner": "rook.rbd.csi.ceph.com",
        "parameters": {
            "clusterID": "rook",
            "pool": "replicapool",
            "imageFormat": "2",
            "csi.storage.k8s.io/provisioner-secret-name": "rook-csi-rbd-provisioner",
            "csi.storage.k8s.io/provisioner-secret-namespace": "rook",
            "csi.storage.k8s.io/controller-expand-secret-name": "rook-csi-rbd-provisioner",
            "csi.storage.k8s.io/controller-expand-secret-namespace": "rook",
            "csi.storage.k8s.io/node-stage-secret-name": "rook-csi-rbd-node",
            "csi.storage.k8s.io/node-stage-secret-namespace": "rook",
            "csi.storage.k8s.io/fstype": "ext4",
            # <https://rook.io/docs/rook/v1.10/Getting-Started/Prerequisites/prerequisites/#rbd>
            "imageFeatures": "layering,fast-diff,object-map,deep-flatten,exclusive-lock",
        },
        "allowVolumeExpansion": True,
        "reclaimPolicy": "Delete",
    },
]


def objects():
    yield from helm.build_chart_from_versions(
        name="rook",
        versions=versions,
        values=values,
    )

    yield ceph_cluster
    yield from storageclass_yaml
