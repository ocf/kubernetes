local name = 'templates';

{
  apiVersion: 'extensions/v1beta1',
  kind: 'Ingress',
  metadata: {
    name: name,
    annotations: {
      'cert-manager.io/cluster-issuer': 'letsencrypt',
      'ingress.kubernetes.io/force-ssl-redirect': 'true',
      'kubernetes.io/tls-acme': 'true',
    },
  },
  spec: {
    rules: [
      {
        host: 'templates.ocf.berkeley.edu',
        http: {
          paths: [
            {
              backend: {
                serviceName: name,
                servicePort: 80,
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
          'templates.ocf.berkeley.edu',
        ],
        secretName: 'templates-tls',
      },
    ],
  },
}
