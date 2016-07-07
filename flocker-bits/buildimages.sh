#!/bin/sh
set -e
export FLOCKER_TAG=1.13.0
docker build -t cedbossneo/flocker-core:$FLOCKER_TAG flocker-core
docker build -t cedbossneo/flocker-container-agent:$FLOCKER_TAG container-agent
docker build -t cedbossneo/flocker-control-service:$FLOCKER_TAG control-agent
docker build -t cedbossneo/flocker-dataset-agent:$FLOCKER_TAG dataset-agent
docker push cedbossneo/flocker-core
docker push cedbossneo/flocker-container-agent
docker push cedbossneo/flocker-control-service
docker push cedbossneo/flocker-dataset-agent
