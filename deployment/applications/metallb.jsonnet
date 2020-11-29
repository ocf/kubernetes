{
  apiVersion: 'argoproj.io/v1alpha1',
  kind: 'Application',
  metadata: {
    name: 'metallb',
  },
  spec: {
    destination: {
      namespace: 'metallb',
      server: 'https://kubernetes.default.svc',
    },
    project: 'default',
    source: {
      path: 'core/metallb',
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
