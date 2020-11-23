#!/usr/bin/env bash
set -euo pipefail

echo "OCF Kubernetes Bootstrap Script"
echo "This script will install the bare minimum needed to run ArgoCD onto your currently configured kubernetes cluster."
echo It has been $((($(date +%s)-$(date +%s --date "2020-11-22"))/(3600*24))) days since this script was last updated. Knowing the OCF, this is probably a lot of days. Consider modernizing this script before you run it.

echo
read -p "Continue? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Check dependencies...
    command -v helm >/dev/null 2>&1 || { echo >&2 "Please install helm before running this script."; exit 1; }
    command -v kubectl >/dev/null 2>&1 || { echo >&2 "Please install kubectl before running this script."; exit 1; }

    echo "Installing Cilium..."
    helm repo add cilium https://helm.cilium.io/
    kubectl create ns cilium
    read -p "Please input the IP of the Kubernetes apiserver: " -n 1 -r
    helm install cilium cilium/cilium --version 1.9.0 --namespace cilium \
    --set kubeProxyReplacement=strict \
    --set k8sServiceHost=$REPLY \
    --set k8sServicePort=6443

    echo "Installing ArgoCD..."
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

    echo "To finish bootstrapping the cluster, visit http://localhost:8000 and manually point ArgoCD at the ocf folder of this git repository, then press sync. When you're done, Ctrl+C this script. ArgoCD should now redeploy itself, cilium, and everything else in this repo."
    kubectl -n argocd port-forward service/argocd-server 8000:80
fi
