{
  apiVersion: 'argoproj.io/v1alpha1',
  kind: 'Application',
  metadata: {
    name: 'cert-manager',
  },
  spec: {
    destination: {
      namespace: 'cert-manager',
      server: 'https://kubernetes.default.svc',
    },
    project: 'default',
    source: {
      path: 'core/cert-manager',
      repoURL: 'https://github.com/ocf/kubernetes',
      targetRevision: 'HEAD',
    },
  },
}
