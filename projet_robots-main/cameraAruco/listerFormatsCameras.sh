#!/bin/bash

echo camera2
ffmpeg -f v4l2 -list_formats all -i /dev/video2

echo camera1
ffmpeg -f v4l2 -list_formats all -i /dev/video0
