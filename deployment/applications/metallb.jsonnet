local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='metallb',
  namespace='metallb',
  directory='core/metallb',
  extraArgs=lib.default_helm_args,
)
