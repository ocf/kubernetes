local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='argo-workflows',
  namespace='argo',
  directory='core/argo-workflows',
  extraArgs={},
)
