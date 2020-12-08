local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='olm',
  namespace='olm',
  directory='core/olm',
  extraArgs={},
)
