local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='vault',
  namespace='vault',
  directory='core/vault',
  extraArgs=lib.default_helm_args,
)
