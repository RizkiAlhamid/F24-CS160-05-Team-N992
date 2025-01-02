# Kubernetes Setup (IN PROGRESS)

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- .env file with the following variables
```bash
MONGO_URI='your_mongo_uri'
```

## Steps
1. Start minikube
```bash
minikube start
```

2. Use the up.sh script to create the deployments and services
```bash
./up.sh
```
