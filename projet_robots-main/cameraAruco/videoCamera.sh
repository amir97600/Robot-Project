#!/bin/bash

echo no framerate

ffplay -f v4l2 -input_format mjpeg -video_size 1920x1080 -i /dev/video2

echo framerate 30

ffplay -f v4l2 -input_format mjpeg -video_size 1920x1080 -i /dev/video2 -framerate 30 -pix_fmt mjpeg

echo framerate 60

ffplay -f v4l2 -input_format mjpeg -video_size 1920x1080 -i /dev/video2 -framerate 60 -pix_fmt mjpeg
