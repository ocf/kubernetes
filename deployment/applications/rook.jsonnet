local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='rook',
  namespace='rook-ceph',
  directory='core/rook',
  extraArgs=lib.default_helm_args,
)
