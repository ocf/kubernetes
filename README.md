# Kubernetes

This is the git repository for the [Open Computing Facility](https://ocf.berkeley.edu/)'s [Kubernetes](https://k8s.io/) cluster.

## Deploying Software

1. Create a new folder in `apps` or `core` and put your configuration in it. See the other folders for examples. You can pick from Helm Charts (recommended), JSONnet Files (recommended for software the OCF wrote), or Kustomize (only recommended if necessary).
2. Add a JSONNET file to `deployment/applications` defining how to deploy the folder you made.
3. (Root Required) Go to [ArgoCD](https://argocd.ocf.berkeley.edu/) and run a sync. We do not automatically sync configuration for safety reasons.

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
    - applications
        - *.jsonnet (ArgoCD application CRDs)
    - projects
        - *.jsonnet (Argocd project CRDs)
```

## Bootstrapping

A bootstrap script is provided to help bring up new clusters when needed. It installs the bare minimum required to run ArgoCD.

```bash
./bootstrap.sh
```

## Contributing

The [Open Computing Facility](https://ocf.berkeley.edu/) (OCF) is an all-volunteer student organization dedicated to free computing for all University of California, Berkeley students, faculty, and staff. Students from all backgrounds are encouraged to [join as staff](https://ocf.io/getinvolved)! If you're not a student, or just want to make a one time contribution, please use the standard GitHub pull request workflow. Thanks for helping out :)
