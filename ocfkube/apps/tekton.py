import requests
import yaml

from ocfkube.utils import versions


helpers = [
    {
        "apiVersion": "v1",
        "kind": "ServiceAccount",
        "metadata": {"name": "registry"},
        "secrets": [{"name": "registry-creds"}],
    },
    {
        "apiVersion": "tekton.dev/v1alpha1",
        "kind": "PipelineResource",
        "metadata": {"name": "templates-git"},
        "spec": {
            "type": "git",
            "params": [
                {"name": "revision", "value": "main"},
                {
                    "name": "url",
                    "value": "https://github.com/ocf/templates",
                },
            ],
        },
    },
    {
        "apiVersion": "tekton.dev/v1alpha1",
        "kind": "PipelineResource",
        "metadata": {"name": "sinatra-hello-world-tekton-demo-image"},
        "spec": {
            "type": "image",
            "params": [
                {
                    "name": "url",
                    "value": "<DOCKER_USERNAME>/sinatra-hello-world-tekton-demo",
                },
            ],
        },
    },
    {
        "apiVersion": "tekton.dev/v1beta1",
        "kind": "Task",
        "metadata": {"name": "build-docker-image-from-git-source"},
        "spec": {
            "params": [
                {
                    "name": "pathToDockerFile",
                    "type": "string",
                    "description": "The path to the dockerfile to build",
                    "default": "$(resources.inputs.docker-source.path)/Dockerfile",
                },
                {
                    "name": "pathToContext",
                    "type": "string",
                    "description": "The build context used by Kaniko\n(https://github.com/GoogleContainerTools/kaniko#kaniko-build-contexts)\n",
                    "default": "$(resources.inputs.docker-source.path)",
                },
            ],
            "resources": {
                "inputs": [{"name": "docker-source", "type": "git"}],
                "outputs": [{"name": "builtImage", "type": "image"}],
            },
            "steps": [
                {
                    "name": "build-and-push",
                    "image": "gcr.io/kaniko-project/executor:v0.17.1",
                    "env": [
                        {"name": "DOCKER_CONFIG", "value": "/tekton/home/.docker/"},
                    ],
                    "command": ["/kaniko/executor"],
                    "args": [
                        "--dockerfile=$(params.pathToDockerFile)",
                        "--destination=$(resources.outputs.builtImage.url)",
                        "--context=$(params.pathToContext)",
                    ],
                },
            ],
        },
    },
    {
        "apiVersion": "tekton.dev/v1beta1",
        "kind": "TaskRun",
        "metadata": {"name": "build-docker-image-from-git-source-task-run"},
        "spec": {
            "serviceAccountName": "dockerhub-service",
            "taskRef": {"name": "build-docker-image-from-git-source"},
            "params": [{"name": "pathToDockerFile", "value": "Dockerfile"}],
            "resources": {
                "inputs": [
                    {
                        "name": "docker-source",
                        "resourceRef": {"name": "sinatra-hello-world-git"},
                    },
                ],
                "outputs": [
                    {
                        "name": "builtImage",
                        "resourceRef": {
                            "name": "sinatra-hello-world-tekton-demo-image",
                        },
                    },
                ],
            },
        },
    },
]

cfg = {
    "apiVersion": "operator.tekton.dev/v1alpha1",
    "kind": "TektonConfig",
    "metadata": {"name": "config", "namespace": "tekton-operator"},
    "spec": {
        # installs Tekton into 
        "profile": "all",
        "targetNamespace": "tekton-operator",
        "pruner": {
            "resources": ["pipelinerun", "taskrun"],
            "keep": 100,
            "schedule": "0 8 * * *",
        },
    },
}


def build() -> object:
    operator = requests.get(
        f"https://storage.googleapis.com/tekton-releases/operator/previous/v{versions['tekton']['version']}/release.yaml",
    ).text
    return [x for x in list(yaml.safe_load_all(operator)) if x is not None] + [cfg]
