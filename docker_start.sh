#!/bin/bash
xhost +local:docker
nvidia-docker run -d -e DISPLAY=$DISPLAY --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix/X0:/tmp/.X11-unix/X0 -v /home/ubuntu/data/:/data -it garyfeng/docker-openpose:latest  \
./build/examples/openpose/openpose.bin --camera 0 --write_images /data/fastai/cached_images_folder/ > ./docker_start.pid

# Helpful commands
# ./build/examples/openpose/openpose.bin --video /data/output/gangnam.mp4 --write_images /data/output/images/rendered/ --write_keypoint_json /data/output/json --process_real_time --disable_blending
#./build/examples/openpose/openpose.bin --video /data/otherway.MOV --write_images /data/fastai/cached_images_folder/  --process_real_time --output_resolution 400x400
#./build/examples/openpose/openpose.bin --camera 0 --write_images /data/fastai/cached_images_folder/
