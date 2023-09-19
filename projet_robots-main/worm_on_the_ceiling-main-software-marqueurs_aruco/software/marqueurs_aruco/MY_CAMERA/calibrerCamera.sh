#!/bin/bash

printf " (1) Faire des video  (2) Concatener les videos (3) Utiliser la video pour calibrer \n"
read choix

if (( $choix == 1 ))
then
printf " Combien de videos \n "
read nbVideo
fi
	if (( $nbVideo == 1 ))
	then
	../build/capture_video -d=0 -w=5 -h=7 --sl=0.0333 --ml=0.02 --ci=0 video_1.avi
	else
	for  (( c=1; c<=$nbVideo; c++ ))
	do
	../build/capture_video -d=0 -w=5 -h=7 --sl=0.0333 --ml=0.02 --ci=0 video_$c.avi
	done
	fi
if (( $choix == 2 ))
then
	printf " Concatene 3 videos "
	../build/concatenate_videos video_1.avi video_2.avi video_3.avi video_for_calibration.avi
fi
if (( $choix == 3 ))
then 
	../build/calibrate_camera_charuco -d=0 -w=5 -h=7 --sl=0.0333 --ml=0.02 video_for_calibration.avi camera_calibration.yaml
fi
