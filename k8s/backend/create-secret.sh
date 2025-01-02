#!/bin/bash

kubectl apply -f <(
  kubectl create secret generic my-secret \
    --from-env-file=.env \
    --dry-run=client -o yaml
)

echo "Secret updated."
