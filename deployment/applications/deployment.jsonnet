{
  apiVersion: 'argoproj.io/v1alpha1',
  kind: 'Application',
  metadata: {
    name: 'deployment',
  },
  spec: {
    destination: {
      namespace: 'argocd',
      server: 'https://kubernetes.default.svc',
    },
    project: 'default',
    source: {
      path: 'deployment',
      repoURL: 'https://github.com/ocf/kubernetes',
      targetRevision: 'HEAD',
      directory: {
        recurse: true,
      },
    },
  },
}
