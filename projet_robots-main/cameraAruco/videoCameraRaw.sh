#!/bin/bash

echo camera 1
ffplay -f v4l2 -input_format yuyv422 -video_size 1920x1080 -i /dev/video0

echo camera 2
ffplay -f v4l2 -input_format yuyv422 -video_size 1920x1080 -i /dev/video2 
