# Kubernetes

This is the git repository for the [Open Computing Facility](https://ocf.berkeley.edu/)'s [Kubernetes](https://k8s.io/) cluster.

## Deploying Software

1. Create a new python file in `ocfkube/apps` with a function `build()` that returns a list of Kubernetes objects (as dicts). See the other python files in that folder for examples. Helper functions are provided for Helm charts, although not all software will use helm charts.
    a. If you need to build your own container image, do so in another git repository. Instructions coming soon (TM).
2. (Root Required) Go to [ArgoCD](https://argo.ocf.berkeley.edu/) and run a sync. Before you click sync, look at the diff to sanity check what will change. We do not automatically sync configuration for safety reasons.

### Code-Test Loop

First, install dependencies and start a poetry shell...

```bash
poetry install
poetry shell
```

Then, make changes and run the following command to test your changes...

```bash
# inside poetry shell, might be python3 depending on your package manager
# e.x. python -m ocfkube cilium -> prints YAML to stdout for cilium
python -m ocfkube <appname>
```

## Folder Structure

Our deployment follows the folder structure of a typical poetry application.

```
- ocfkube
    - apps
        - cilium
        - notes
        - ... (any software)
        - versions.toml (all software versions)
    - utils
        - ... (helper functions)
    - lib
        - ... (common k8s object generators)
```

## Bootstrapping

A bootstrap script is provided to help bring up new clusters when needed. It installs the bare minimum required to run ArgoCD, provided Kubernetes is already running without a CNI, and `KUBECONFIG` is pointed at the right place.

```bash
./bootstrap.sh
```

## Contributing

The [Open Computing Facility](https://ocf.berkeley.edu/) (OCF) is an all-volunteer student organization dedicated to free computing for all University of California, Berkeley students, faculty, and staff. Students from all backgrounds are encouraged to [join as staff](https://ocf.io/getinvolved)! If you're not a student, or just want to make a one time contribution, please use the standard GitHub pull request workflow. Thanks for helping out :)
