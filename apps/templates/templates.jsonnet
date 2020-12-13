local simple = import '../../lib/simple.libsonnet';

local options = {
  name: 'templates',
  image: 'harbor.ocf.berkeley.edu/library/templates:latest',
  mem: '128Mi',
  cpu: '50m',
  port: 8000,
  domain: 'templates.ocf.berkeley.edu',
};

[simple.deployment(options), simple.service(options), simple.ingress(options)]
