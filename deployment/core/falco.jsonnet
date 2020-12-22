local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='falco',
  namespace='falco',
  directory='core/falco',
  extraArgs=lib.default_helm_args,
)
