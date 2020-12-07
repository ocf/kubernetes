local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='argo-events',
  namespace='argo-events',
  directory='core/argo-events',
  extraArgs={},
)
