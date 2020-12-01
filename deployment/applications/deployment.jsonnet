local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='deployment',
  namespace='argocd',
  directory='deployment',
  extraArgs={
    directory: { // "Just parse this directory into YAML" mode
      recurse: true,
    },
  },
)
