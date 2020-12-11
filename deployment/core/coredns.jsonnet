local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='coredns',
  namespace='kube-system',
  directory='core/coredns',
  extraArgs=lib.default_helm_args,
)
