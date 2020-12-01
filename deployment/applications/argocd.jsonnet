local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='argo-cd',
  namespace='argocd',
  directory='core/argocd',
  extraArgs={},
)
