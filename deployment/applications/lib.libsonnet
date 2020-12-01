{
  default_helm_args: {
    helm: {
      valueFiles: [
        'values.yaml',
      ],
      version: 'v3',
    },
  },

  make_deployment(name, namespace, directory, extraArgs):: {
    apiVersion: 'argoproj.io/v1alpha1',
    kind: 'Application',
    metadata: {
      name: name,
    },
    spec: {
      destination: {
        namespace: namespace,
        server: 'https://kubernetes.default.svc',
      },
      project: 'default',
      source: {
        path: directory,
        repoURL: 'https://github.com/ocf/kubernetes',
        targetRevision: 'HEAD',
      } + extraArgs,
    },
  },
}
