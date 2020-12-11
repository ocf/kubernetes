local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='templates',
  namespace='templates',
  directory='apps/templates',
  extraArgs={
    directory: { // "Just parse this directory into YAML" mode
      recurse: true,
    },
  },
)
