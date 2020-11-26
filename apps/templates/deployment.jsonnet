local name = 'templates';

{
  apiVersion: 'apps/v1',
  kind: 'Deployment',
  metadata: {
    name: 'templates-deployment',
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
            image: 'docker.ocf.berkeley.edu/templates:<%= version %>',
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
