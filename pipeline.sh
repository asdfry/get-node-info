#!/bin/bash

docker build -t asdfry/get-node-info:20230625 .
docker push asdfry/get-node-info:20230625
yes | docker system prune -a
docker system df
