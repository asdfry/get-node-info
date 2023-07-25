#!/bin/bash

docker build -t asdfry/get-node-info:$1 .
docker push asdfry/get-node-info:$1
yes | docker system prune -a
