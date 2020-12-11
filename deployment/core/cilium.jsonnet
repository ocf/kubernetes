local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='cilium',
  namespace='cilium',
  directory='core/cilium',
  extraArgs=lib.default_helm_args,
)
