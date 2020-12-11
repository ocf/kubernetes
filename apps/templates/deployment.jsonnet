local name = 'templates';

{
  apiVersion: 'apps/v1',
  kind: 'Deployment',
  metadata: {
    name: name,
    labels: {
      app: name,
    },
  },
  spec: {
    replicas: 1,
    selector: {
      matchLabels: {
        app: name,
      },
    },
    template: {
      metadata: {
        labels: {
          app: name,
        },
      },
      spec: {
        containers: [
          {
            name: name,
            image: 'harbor.ocf.berkeley.edu/library/templates:latest',
            resources: {
              limits: {
                memory: '128Mi',
                cpu: '50m',
              },
            },
            ports: [
              {
                containerPort: 8000,
              },
            ],
          },
        ],
      },
    },
  },
}
