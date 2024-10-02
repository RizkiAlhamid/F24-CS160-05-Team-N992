#!/bin/bash

# Check if we are already inside a poetry shell
if [[ "$VIRTUAL_ENV" != "" ]]; then
  echo "Already in poetry shell. Running the app..."
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
else
  echo "Not in poetry shell. Activate it by running 'poetry shell' and then re-run the script."
fi

