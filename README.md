# Kubernetes

This is the git repository for the [Open Computing Facility](https://ocf.berkeley.edu/)'s [Kubernetes](https://k8s.io/) cluster.

## Deploying Software

1. Create a new folder in the format of the other folders in this repository. You can pick from Helm Charts (recommended), our custom Python script plugin (recommended), JSONnet Files (eh), or Kustomize (not recommended).
2. Add a YAML file to `ocf/applications` defining how to deploy the folder you made.
3. Edit `ocf/kustomization.yml` to add the name of the YAML file you made.
4. (Root Required) Go to [ArgoCD](https://argocd.ocf.berkeley.edu/) and manually run the first sync, if it hasn't automatically.

## Bootstrapping

A bootstrap script is provided to help bring up new clusters when needed. It installs the bare minimum required to run ArgoCD.

```bash
./bootstrap.sh
```

## Contributing

The [Open Computing Facility](https://ocf.berkeley.edu/) (OCF) is an all-volunteer student organization dedicated to free computing for all University of California, Berkeley students, faculty, and staff. Students from all backgrounds are encouraged to [join as staff](https://ocf.io/getinvolved)! If you're not a student, or just want to make a one time contribution, please use the standard GitHub pull request workflow. Thanks for helping out :)
