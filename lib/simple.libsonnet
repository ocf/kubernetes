{
  deployment(options)::
    assert std.isString(options.name);
    assert std.isString(options.image);
    assert std.isString(options.mem);
    assert std.isString(options.cpu);
    assert std.isNumber(options.port);
    {
      apiVersion: 'apps/v1',
      kind: 'Deployment',
      metadata: {
        name: options.name,
        labels: {
          app: options.name,
        },
      },
      spec: {
        replicas: 1,
        selector: {
          matchLabels: {
            app: options.name,
          },
        },
        template: {
          metadata: {
            labels: {
              app: options.name,
            },
          },
          spec: {
            containers: [
              {
                name: options.name,
                image: options.image,
                resources: {
                  limits: {
                    memory: options.mem,
                    cpu: options.cpu,
                  },
                },
                ports: [
                  {
                    containerPort: options.port,
                  },
                ],
              },
            ],
            securityContext: {
              runAsNonRoot: if 'nonRoot' in options then assert std.isBoolean(options.nonRoot); options.nonRoot else true,
            },
          },
        },
      },
    },

  service(options)::
    assert std.isString(options.name);
    assert std.isNumber(options.port);
    {
      apiVersion: 'v1',
      kind: 'Service',
      metadata: {
        name: options.name,
      },
      spec: {
        selector: {
          app: options.name,
        },
        ports: [
          {
            port: options.port,
            targetPort: options.port,
          },
        ],
      },
    },

  ingress(options)::
    assert std.isString(options.name);
    assert std.isString(options.domain);
    assert std.isNumber(options.port);
    {
      // Deprecated: Move to networking by v1.22 (upgrade blocked by ArgoCD).
      apiVersion: 'extensions/v1beta1',
      kind: 'Ingress',
      metadata: {
        name: options.name,
        annotations: {
          'cert-manager.io/cluster-issuer': 'letsencrypt',
          'ingress.kubernetes.io/force-ssl-redirect': 'true',
          'kubernetes.io/tls-acme': 'true',
        },
      },
      spec: {
        rules: [
          {
            host: options.domain,
            http: {
              paths: [
                {
                  backend: {
                    serviceName: options.name,
                    servicePort: options.port,
                  },
                  pathType: 'ImplementationSpecific',
                },
              ],
            },
          },
        ],
        tls: [
          {
            hosts: [
              options.domain,
            ],
            secretName: options.name + '-tls',
          },
        ],
      },
    },
}
