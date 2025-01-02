#!/bin/bash

# Function to apply the Kubernetes resources
apply_k8s_resources() {
    local path=$1
    echo "Deploying resources from $path"
    kubectl apply -f "$path"
}

# Deploy backend resources
./backend/create-secret.sh
apply_k8s_resources "backend/service.yaml"
apply_k8s_resources "backend/deployment.yaml"

# Deploy frontend resources
#apply_k8s_resources "frontend/service.yaml"
#apply_k8s_resources "frontend/deployment.yaml"

# Deploy webscraper resources
#apply_k8s_resources "webscraper/service.yaml"
#apply_k8s_resources "webscraper/deployment.yaml"

echo "Deployment complete."
