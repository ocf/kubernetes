local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='prometheus-stack',
  namespace='prometheus',
  directory='core/prometheus',
  extraArgs=lib.default_helm_args,
)
