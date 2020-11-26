local name = 'templates';

{
  apiVersion: 'extensions/v1beta1',
  kind: 'Ingress',
  metadata: {
    name: 'virtual-host-ingress',
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
            },
          ],
        },
      },
    ],
  },
}
