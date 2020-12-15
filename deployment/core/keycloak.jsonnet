local lib = import 'lib.libsonnet';

lib.make_deployment(
  name='keycloak',
  namespace='keycloak',
  directory='core/keycloak',
  extraArgs=lib.default_helm_args,
)
