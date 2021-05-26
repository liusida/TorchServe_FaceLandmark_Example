#!/bin/sh
set -x

# customized port numbers
BASE_SERVE_PORT=9001
BASE_MANAGE_PORT=10001

# create log folder
mkdir -p logs/face_lm_3d

# Run the container
docker run -it --rm --name=torchserve-face_lm_3d \
    --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
    -p$(expr $BASE_SERVE_PORT + 2):8080 \
    -p$(expr $BASE_MANAGE_PORT + 2):8081 \
    --mount type=bind,source=$PWD/logs/face_lm_3d,target=/home/model-server/logs \
    --mount type=bind,source=$PWD/model_store/face_lm_3d,target=/tmp/models \
    --mount type=bind,source=$PWD/debug,target=/tmp/debug \
    face_lm_3d:latest \
    torchserve --model-store=/tmp/models --ts-config=/tmp/models/torchserve.cfg

# remove log folder if needed
# rm logs/face_lm_3d -rf