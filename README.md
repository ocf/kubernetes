# Kubernetes

This is the git repository for the [Open Computing Facility](https://ocf.berkeley.edu/)'s [Kubernetes](https://k8s.io/) cluster.

## Deploying Software

1. Create a new folder in `apps` or `core` and put your configuration in it. See the other folders for examples. You can pick from Helm Charts (recommended), JSONnet Files (recommended for software the OCF wrote), or Kustomize (only recommended if necessary).
    a. If you need to build your own container image, do so in another git repository. Instructions coming soon (TM).
2. Add a JSONnet file to `deployment/applications` defining how to deploy the folder you made.
3. (Root Required) Go to [ArgoCD](https://argo.ocf.berkeley.edu/) and run a sync. Before you click sync, look at the diff to sanity check what will change. We do not automatically sync configuration for safety reasons.

## Folder Structure

```
- apps
    - templates
    - notes
    - ... (stakeholder-facing applications)
- core
    - cilium
    - argocd
    - ... (cluster resources and configuration)
- deployment
    - {apps, core}
        - *.jsonnet (ArgoCD application CRDs)
    - projects
        - *.jsonnet (Argocd project CRDs)
- lib
    - *.libsonnet (JSONnet helper libraries)
```

## Bootstrapping

A bootstrap script is provided to help bring up new clusters when needed. It installs the bare minimum required to run ArgoCD, provided Kubernetes is already running without a CNI, and `KUBECONFIG` is pointed at the right place.

```bash
./bootstrap.sh
```

## Contributing

The [Open Computing Facility](https://ocf.berkeley.edu/) (OCF) is an all-volunteer student organization dedicated to free computing for all University of California, Berkeley students, faculty, and staff. Students from all backgrounds are encouraged to [join as staff](https://ocf.io/getinvolved)! If you're not a student, or just want to make a one time contribution, please use the standard GitHub pull request workflow. Thanks for helping out :)
