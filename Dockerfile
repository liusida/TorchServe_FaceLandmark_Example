FROM pytorch/torchserve:latest-cpu

# Install face_alignment, the core algorithm
# https://github.com/1adrianb/face-alignment
RUN pip install -U pip
RUN pip install face_alignment

# Additional dependencies
# https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo
USER root
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Copy the cached models into docker, to avoid download at runtime.
USER model-server
COPY --chown=model-server:model-server ./model_store/face_lm_3d/downloaded/* /home/model-server/.cache/torch/hub/checkpoints/
