local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='harbor',
  namespace='harbor',
  directory='core/harbor',
  extraArgs=lib.default_helm_args,
)
