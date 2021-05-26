#!/bin/sh
# use docker container to build the archive. (Because machines with small memory might have trouble installing pytorch at all.)

echo "Starting the container..."
docker run -d --rm --name=torchserve-model-archiver-face_lm_3d \
    --mount type=bind,source=$PWD,target=/home/model-server/host_folder \
    face_lm_3d:latest \
    bash

docker exec -t torchserve-model-archiver-face_lm_3d \
    python host_folder/dummy_pth.py --path host_folder/model_store/face_lm_3d/models/dummy.pth

docker exec -t torchserve-model-archiver-face_lm_3d \
    torch-model-archiver --model-name face_lm_3d --version 1.0 \
        --serialized-file host_folder/model_store/face_lm_3d/models/dummy.pth \
        --export-path host_folder/model_store/face_lm_3d/ \
        --force \
        --handler host_folder/handler.py

echo "Stopping the container..."
docker stop torchserve-model-archiver-face_lm_3d
