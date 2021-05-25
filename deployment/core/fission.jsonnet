local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='fission',
  namespace='fission',
  directory='core/fission',
  extraArgs=lib.default_helm_args,
)
