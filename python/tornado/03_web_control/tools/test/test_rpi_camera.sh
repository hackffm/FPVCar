#!/bin/bash

echo camera still picture test
echo detecting
vcgencmd get_camera

if [ ! -d ~/temp/camera ]; then
    mkdir -p ~/temp/camera
fi

DATE=$(date +"%Y-%m-%d_%H%M")
raspistill -vf -hf -o ~/temp/camera/$DATE.jpg
echo "created ~/temp/camera/$DATE.jpeg"
