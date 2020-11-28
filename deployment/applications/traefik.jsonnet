{
  apiVersion: 'argoproj.io/v1alpha1',
  kind: 'Application',
  metadata: {
    name: 'traefik',
  },
  spec: {
    destination: {
      namespace: 'traefik',
      server: 'https://kubernetes.default.svc',
    },
    project: 'default',
    source: {
      path: 'core/traefik',
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
