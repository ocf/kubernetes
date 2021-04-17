local name = "postgres-operator";

{
  apiVersion: 'argoproj.io/v1alpha1',
  kind: 'Sensor',
  metadata: {
    name: name,
  },
  spec: {
    template: {
      container: {
        volumeMounts: [
          {
            mountPath: '/git/ocf',
            name: 'argoproj',
          },
          {
            mountPath: '/secret',
            name: 'sshkey',
          },
          {
            mountPath: '/etc/ssh',
            name: 'known-hosts',
          },
        ],
      },
      volumes: [
        {
          name: 'argoproj',
          emptyDir: {},
        },
        {
          name: 'sshkey',
          secret: {
            secretName: 'git-ssh',
          },
        },
        {
          name: 'known-hosts',
          secret: {
            secretName: 'git-known-hosts',
          },
        },
      ],
      serviceAccountName: 'operate-workflow-sa',
    },
    dependencies: [
      {
        name: 'push-dep',
        eventSourceName: 'github-postgres-operator',
        eventName: 'push',
      },
    ],
    triggers: [
      {
        template: {
          name: 'webhook-workflow-trigger',
          k8s: {
            group: 'argoproj.io',
            version: 'v1alpha1',
            resource: 'workflows',
            operation: 'create',
            source: {
              resource: {
                apiVersion: 'argoproj.io/v1alpha1',
                kind: 'Workflow',
                metadata: {
                  generateName: 'webhook-',
                },
                spec: {
                  entrypoint: 'build',
                  serviceAccountName: 'argo',
                  volumes: [
                    {
                      name: 'workflow-account',
                      secret: {
                        secretName: 'workflow-account',
                      },
                    },
                  ],
                  templates: [
                    {
                      name: 'build',
                      inputs: {
                        artifacts: [
                          {
                            name: 'source',
                            path: '/src',
                            git: {
                              repo: 'https://github.com/ocf/templates',
                              revision: 'master',
                            },
                          },
                        ],
                      },
                      container: {
                        image: 'gcr.io/kaniko-project/executor',
                        env: [
                          {
                            name: 'AWS_S3_USE_ARN_REGION',
                            value: 'false',
                          },
                        ],
                        args: [
                          '--context=/src',
                          '--destination=harbor.ocf.berkeley.edu/library/' + name + ':master',
                        ],
                        volumeMounts: [
                          {
                            name: 'workflow-account',
                            mountPath: '/kaniko/.docker/',
                            readOnly: true,
                          },
                        ],
                      },
                    },
                  ],
                },
              },
            },
            parameters: [
              {
                src: {
                  dependencyName: 'test-dep',
                },
                dest: 'spec.arguments.parameters.0.value',
              },
            ],
          },
        },
      },
    ],
  },
}
