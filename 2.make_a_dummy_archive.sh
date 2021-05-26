#!/bin/sh

python dummy_pth.py --path model_store/face_lm_3d/models/dummy.pth

# pip install torch-model-archiver
# torch-model-archiver==0.4.0
torch-model-archiver --model-name face_lm_3d --version 1.0 \
    --serialized-file model_store/face_lm_3d/models/dummy.pth \
    --export-path model_store/face_lm_3d/ \
    --force \
    --handler handler.py
