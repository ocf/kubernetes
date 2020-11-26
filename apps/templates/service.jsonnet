local name = 'templates';

{
  apiVersion: 'v1',
  kind: 'Service',
  metadata: {
    name: name,
  },
  spec: {
    selector: {
      app: name,
    },
    ports: [
      {
        port: 80,
        targetPort: 8000,
      },
    ],
  },
}
