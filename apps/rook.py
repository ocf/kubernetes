from transpire import helm
from transpire.utils import get_versions

name = "rook"
values = {
    "image": {
        "tag": "v1.15.9",
    },
    # <https://rook.io/docs/rook/v1.10/CRDs/Cluster/ceph-cluster-crd/?h=stack#network-configuration-settings>
    "network": {
        "dualStack": True,
    },
    # <https://rook.io/docs/rook/v1.10/Storage-Configuration/Monitoring/ceph-dashboard/?h=dashboard#enable-the-ceph-dashboard>
    "dashboard": {
        "enabled": True,
    },
    "enableDiscoveryDaemon": True,
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

nucleusDevices = [
    {
        "config": {"deviceClass": "nvme"},
        "name": "/dev/disk/by-path/pci-0000:02:00.0-nvme-1",
    },
    {
        "config": {"deviceClass": "nvme"},
        "name": "/dev/disk/by-path/pci-0000:41:00.0-nvme-1",
    },
    {
        "config": {"deviceClass": "hdd"},
        "name": "/dev/disk/by-path/pci-0000:84:00.0-ata-2",
    },
    {
        "config": {"deviceClass": "hdd"},
        "name": "/dev/disk/by-path/pci-0000:84:00.0-ata-3",
    },
]


def objects():
    yield from helm.build_chart_from_versions(
        name="rook",
        versions=get_versions(__file__),
        values=values,
    )

    yield {
        "apiVersion": "ceph.rook.io/v1",
        "kind": "CephCluster",
        "metadata": {
            "name": "ceph",
            "namespace": "rook",
            "annotations": {"argocd.argoproj.io/compare-options": "IgnoreExtraneous"},
        },
        "spec": {
            "cephVersion": {"image": "quay.io/ceph/ceph:v18.2.2"},
            "dataDirHostPath": "/var/lib/rook",
            "mon": {"count": 3, "allowMultiplePerNode": False},
            # Re-enable this when the issue that blocks it is merged and available in a released Ceph version.
            # <https://github.com/ceph/ceph/pull/48384>
            # This is needed to show physical devices in the Ceph dashboard.
            # "mgr": {'modules': [{'name': 'rook', 'enabled': True}]},
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
                    {
                        "devices": nucleusDevices,
                        "name": "thymine",
                    },
                ],
                "useAllDevices": False,
                "useAllNodes": False,
            },
        },
    }

    #################
    # Block Devices #
    #################
    yield {
        "apiVersion": "ceph.rook.io/v1",
        "kind": "CephBlockPool",
        "metadata": {"name": "rbd-nvme", "namespace": "rook"},
        "spec": {
            "failureDomain": "host",
            "replicated": {"size": 3, "requireSafeReplicaSize": True},
            "deviceClass": "nvme",
        },
    }

    yield {
        "apiVersion": "storage.k8s.io/v1",
        "kind": "StorageClass",
        "metadata": {
            "name": "rbd-nvme",
            "annotations": {"storageclass.kubernetes.io/is-default-class": "true"},
        },
        "provisioner": "rook.rbd.csi.ceph.com",
        "parameters": {
            "clusterID": "rook",
            "pool": "rbd-nvme",
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
    }

    yield {
        "apiVersion": "snapshot.storage.k8s.io/v1",
        "kind": "VolumeSnapshotClass",
        "metadata": {"name": "csi-rbdplugin-snapclass"},
        "driver": "rook.rbd.csi.ceph.com",
        "parameters": {
            "clusterID": "rook",
            "csi.storage.k8s.io/snapshotter-secret-name": "rook-csi-rbd-provisioner",
            "csi.storage.k8s.io/snapshotter-secret-namespace": "rook",
        },
        "deletionPolicy": "Delete",
    }

    ###############
    # Filesystems #
    ###############
    yield {
        "apiVersion": "ceph.rook.io/v1",
        "kind": "CephFilesystem",
        "metadata": {"name": "cephfs-hybrid"},
        "spec": {
            "metadataPool": {
                "failureDomain": "host",
                "replicated": {"size": 3},
                "deviceClass": "nvme",
            },
            "dataPools": [
                {
                    "name": "nvme",
                    "failureDomain": "host",
                    "replicated": {"size": 3},
                    "deviceClass": "nvme",
                },
                {
                    "name": "hdd",
                    "failureDomain": "host",
                    "replicated": {"size": 3},
                    "deviceClass": "hdd",
                },
            ],
            "preserveFilesystemOnDelete": True,
            "metadataServer": {"activeCount": 1, "activeStandby": True},
        },
    }

    yield {
        "apiVersion": "storage.k8s.io/v1",
        "kind": "StorageClass",
        "metadata": {"name": "cephfs-nvme"},
        "provisioner": "rook.cephfs.csi.ceph.com",
        "parameters": {
            "clusterID": "rook",
            "fsName": "cephfs-hybrid",
            "pool": "cephfs-hybrid-nvme",
            "csi.storage.k8s.io/provisioner-secret-name": "rook-csi-cephfs-provisioner",
            "csi.storage.k8s.io/provisioner-secret-namespace": "rook",
            "csi.storage.k8s.io/controller-expand-secret-name": "rook-csi-cephfs-provisioner",
            "csi.storage.k8s.io/controller-expand-secret-namespace": "rook",
            "csi.storage.k8s.io/node-stage-secret-name": "rook-csi-cephfs-node",
            "csi.storage.k8s.io/node-stage-secret-namespace": "rook",
        },
        "reclaimPolicy": "Delete",
    }

    yield {
        "apiVersion": "storage.k8s.io/v1",
        "kind": "StorageClass",
        "metadata": {"name": "cephfs-hdd"},
        "provisioner": "rook.cephfs.csi.ceph.com",
        "parameters": {
            "clusterID": "rook",
            "fsName": "cephfs-hybrid",
            "pool": "cephfs-hybrid-hdd",
            "csi.storage.k8s.io/provisioner-secret-name": "rook-csi-cephfs-provisioner",
            "csi.storage.k8s.io/provisioner-secret-namespace": "rook",
            "csi.storage.k8s.io/controller-expand-secret-name": "rook-csi-cephfs-provisioner",
            "csi.storage.k8s.io/controller-expand-secret-namespace": "rook",
            "csi.storage.k8s.io/node-stage-secret-name": "rook-csi-cephfs-node",
            "csi.storage.k8s.io/node-stage-secret-namespace": "rook",
        },
        "reclaimPolicy": "Delete",
    }

    yield {
        "apiVersion": "snapshot.storage.k8s.io/v1",
        "kind": "VolumeSnapshotClass",
        "metadata": {"name": "csi-cephfsplugin-snapclass"},
        "driver": "rook.cephfs.csi.ceph.com",
        "parameters": {
            "clusterID": "rook",
            "csi.storage.k8s.io/snapshotter-secret-name": "rook-csi-cephfs-provisioner",
            "csi.storage.k8s.io/snapshotter-secret-namespace": "rook",
        },
        "deletionPolicy": "Delete",
    }

    ##################
    # Object Storage #
    ##################
    crtname = "o3-ocf-crt"
    yield {
        "apiVersion": "cert-manager.io/v1",
        "kind": "Certificate",
        "metadata": {"name": crtname},
        "spec": {
            "secretName": crtname,
            "dnsNames": ["o3.ocf.io", "o3.ocf.berkeley.edu"],
            "issuerRef": {
                "name": "letsencrypt",
                "kind": "ClusterIssuer",
                "group": "cert-manager.io",
            },
        },
    }

    yield {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": "o3-ingress",
        },
        "spec": {
            "ingressClassName": "contour",
            "tls": [
                {
                    "hosts": ["o3.ocf.io", "o3.ocf.berkeley.edu"],
                    "secretName": crtname,
                },
            ],
            "rules": [
                {
                    "host": "o3.ocf.io",
                    "http": {
                        "paths": [
                            {
                                "path": "/",
                                "pathType": "Prefix",
                                "backend": {
                                    "service": {
                                        "name": "rook-ceph-rgw-rgw-hdd",
                                        "port": {"number": 80},
                                    }
                                },
                            }
                        ]
                    },
                },
                {
                    "host": "o3.ocf.berkeley.edu",
                    "http": {
                        "paths": [
                            {
                                "path": "/",
                                "pathType": "Prefix",
                                "backend": {
                                    "service": {
                                        "name": "rook-ceph-rgw-rgw-hdd",
                                        "port": {"number": 80},
                                    }
                                },
                            }
                        ]
                    },
                },
            ],
        },
    }

    yield {
        "apiVersion": "ceph.rook.io/v1",
        "kind": "CephObjectStore",
        "metadata": {"name": "rgw-hdd"},
        "spec": {
            "metadataPool": {
                "failureDomain": "host",
                "replicated": {"size": 3},
                "deviceClass": "nvme",
            },
            "dataPool": {
                "failureDomain": "host",
                "replicated": {"size": 3},
                "deviceClass": "hdd",
            },
            "preservePoolsOnDelete": True,
            "gateway": {
                "securePort": 443,
                "port": 80,
                "instances": 1,
            },
        },
    }

    yield {
        "apiVersion": "storage.k8s.io/v1",
        "kind": "StorageClass",
        "metadata": {"name": "rgw-hdd"},
        "provisioner": "rook.ceph.rook.io/bucket",
        "reclaimPolicy": "Delete",
        "parameters": {
            "objectStoreName": "rgw-hdd",
            "objectStoreNamespace": "rook-ceph",
        },
    }
