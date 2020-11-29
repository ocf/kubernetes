{
  apiVersion: 'argoproj.io/v1alpha1',
  kind: 'Application',
  metadata: {
    name: 'contour',
  },
  spec: {
    destination: {
      namespace: 'contour',
      server: 'https://kubernetes.default.svc',
    },
    project: 'default',
    source: {
      path: 'core/contour',
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
