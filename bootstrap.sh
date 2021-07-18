#!/usr/bin/env bash
set -euo pipefail

echo "OCF Kubernetes Bootstrap Script"
echo "This script will install the bare minimum needed to run ArgoCD onto your currently configured kubernetes cluster."
echo It has been $((($(date +%s)-$(date +%s --date "2021-07-18"))/(3600*24))) days since this script was last updated. Knowing the OCF, this is probably a lot of days. Consider modernizing this script before you run it.

# TODO: Automatically detect when services are healthy and it's ok to move on.

echo
read -p "Continue? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Check dependencies...
    command -v helm >/dev/null 2>&1 || { echo >&2 "Please install helm before running this script."; exit 1; }
    command -v kubectl >/dev/null 2>&1 || { echo >&2 "Please install kubectl before running this script."; exit 1; }

    echo "Installing Cilium..."
    kubectl create namespace cilium --dry-run=client -o yaml | kubectl apply -f -
    python3 -m ocfkube cilium | kubectl apply -n cilium -f -
    read -p "Now wait for Cilium to come up, press enter once it's healthy... " -n 1 -r
    
    echo "Installing CoreDNS..."
    kubectl create namespace coredns --dry-run=client -o yaml | kubectl apply -f -
    python3 -m ocfkube coredns | kubectl apply -n coredns -f -
    read -p "Now wait for CoreDNS to come up, press enter once it's healthy... " -n 1 -r
    
    echo "Installing ArgoCD..."
    kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
    python3 -m ocfkube argocd | kubectl apply -n argocd -f -
    read -p "Now wait for ArgoCD to come up, press enter once it's healthy... " -n 1 -r
    
    echo "USERNAME: admin, PASSWORD: the name of the argocd-server pod"
    kubectl -n argocd get pods

    echo "To finish bootstrapping the cluster, visit http://localhost:8000, log in, and press sync. When you're done, Ctrl+C this script. ArgoCD should now redeploy itself, cilium, and everything else in this repo."
    kubectl -n argocd port-forward service/argocd-server 8000:80
fi
