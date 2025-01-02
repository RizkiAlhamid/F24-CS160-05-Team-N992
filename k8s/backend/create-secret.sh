#!/bin/bash

kubectl apply -f <(
  kubectl create secret generic mongo-uri \
    --from-env-file=.env \
    --dry-run=client -o yaml
)

echo "Secret updated."
