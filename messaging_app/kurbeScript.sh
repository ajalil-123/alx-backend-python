#!/usr/bin/env bash
# kurbeScript - Set up and verify a local Kubernetes cluster with Minikube

set -e  # exit on error

# Step 1: Check if minikube is installed
if ! command -v minikube &> /dev/null
then
    echo "Minikube not found. Please install Minikube first."
    exit 1
fi

# Step 2: Check if kubectl is installed
if ! command -v kubectl &> /dev/null
then
    echo "kubectl not found. Please install kubectl first."
    exit 1
fi

# Step 3: Start minikube cluster
echo "Starting Minikube cluster..."
minikube start

# Step 4: Verify cluster info
echo "Verifying cluster status..."
kubectl cluster-info

# Step 5: List pods in kube-system namespace
echo "Retrieving pods..."
kubectl get pods -A
