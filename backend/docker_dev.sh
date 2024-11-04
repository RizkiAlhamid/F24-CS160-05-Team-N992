#!/bin/bash

# Pull and run the Docker container
docker run -d --env-file .env -p 8080:8080 --name backend rizkialhamid/cs160-project-backend:latest
