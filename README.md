# TorchServe_FaceLandmark_Example

In this repository, I am practicing how to deploy a face landmark application as a web service.

The face landmark application is from [https://github.com/1adrianb/face-alignment](https://github.com/1adrianb/face-alignment).

## Prerequisites

We'll need docker to run everything. Please [install docker](https://docs.docker.com/get-docker/) and [give non-root user access](https://docs.docker.com/engine/install/linux-postinstall/). If you don't want to give non-root user access to docker due to security concern, please change the corresponding scripts accordingly.

## Steps

0. download related models.
```bash
cd model_store/face_lm_3d/models
sh download_models.sh # this might be very slow, since the author's website is getting busy.
                      # if it is slow, please Ctrl+C and retry multiple times.
cd ../../..
```

1. build an image based on `pytorch/torchserve:latest-cpu`, install dependencies in the container, and copy the models .
```bash
sh 1.build_image.sh
```

2. start the docker container and make a dummy archive for TorchServe. (the real model will be invoked and used in the `handler.py`)
```bash
sh 2.make_a_dummy_archive.sh
```

3. start the service.
```bash
sh 3.docker-run.sh
```

4. try the service. the output image will be write in the `debug/` folder.
```bash
python try_remote.py
```

5. stop the service.
```bash
docker stop torchserve-face_lm_3d
```