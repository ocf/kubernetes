{
  apiVersion: 'argoproj.io/v1alpha1',
  kind: 'Application',
  metadata: {
    name: 'argo-cd',
  },
  spec: {
    destination: {
      namespace: 'argocd',
      server: 'https://kubernetes.default.svc',
    },
    project: 'default',
    source: {
      path: 'core/argocd',
      repoURL: 'https://github.com/ocf/kubernetes',
      targetRevision: 'HEAD',
    },
  },
}
