{
  apiVersion: 'argoproj.io/v1alpha1',
  kind: 'Application',
  metadata: {
    name: 'rook',
  },
  spec: {
    destination: {
      namespace: 'rook-ceph',
      server: 'https://kubernetes.default.svc',
    },
    project: 'default',
    source: {
      path: 'core/rook',
      repoURL: 'https://github.com/ocf/kubernetes',
      targetRevision: 'HEAD',
      helm: {
        valueFiles: [
          'values.yaml',
        ],
        version: 'v3',
      },
    },
  },
}
