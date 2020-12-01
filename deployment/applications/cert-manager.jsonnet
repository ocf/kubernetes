local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='cert-manager',
  namespace='cert-manager',
  directory='core/cert-manager',
  extraArgs=lib.default_helm_args,
)
