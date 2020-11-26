{
  apiVersion: 'argoproj.io/v1alpha1',
  kind: 'Application',
  metadata: {
    name: 'cilium',
  },
  spec: {
    destination: {
      namespace: 'cilium',
      server: 'https://kubernetes.default.svc',
    },
    project: 'default',
    source: {
      path: 'core/cilium',
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
