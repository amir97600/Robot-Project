#!/bin/bash

printf " (1) Configurer+Auto-focus (2) Sans Auto-focus "
read choix

if (( $choix == 1 ))
then
printf " \n\n Configuration de la camera avec Auto-focus \n "
python3 ../scripts/configure_camera.py -d /dev/video0 -c camera_configuration.yaml

else
printf " \n\n Reglage sans l'auto focus \n "
python3 ../scripts/configure_camera.py -d /dev/video0 -c camera_configuration.yaml -i
fi
