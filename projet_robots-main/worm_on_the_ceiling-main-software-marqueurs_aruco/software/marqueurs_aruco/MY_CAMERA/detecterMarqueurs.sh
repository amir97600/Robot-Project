#!/bin/bash

printf " (1) detecter les marqueurs  (2) Afficher les coordonnées "
read choix

if (( $choix == 1 ))
then
../build/detect_aruco_markers -d=0 --ci=0 -l=0.02 -c=camera_calibration.yaml
else
python3  ../scripts/detect_markers_and_camera_inside_a_given_map.py --ci 0 -c camera_calibration.yaml -m Mymap.yaml
fi
