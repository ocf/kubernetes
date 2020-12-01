local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='contour',
  namespace='contour',
  directory='core/contour',
  extraArgs=lib.default_helm_args,
)
