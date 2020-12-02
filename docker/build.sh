#!/bin/bash

MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

IMG=gha2/gha2minio:latest

cd "$MYDIR/.." || exit 1

docker build . -f docker/Dockerfile -t $IMG
docker push $IMG
