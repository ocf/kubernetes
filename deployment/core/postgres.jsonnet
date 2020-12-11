local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='postgresql',
  namespace='postgresql',
  directory='core/postgresql',
  extraArgs=lib.default_helm_args,
)
