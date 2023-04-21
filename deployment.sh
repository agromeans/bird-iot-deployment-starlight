#!/bin/bash
# bash /home/pi/agromeans/tools/bird-iot-deployment-starlight/deployment.sh
base=/home/pi/agromeans/tools/bird-iot-deployment-starlight/start.sh
server=bird.agromeans.com:3360
bash $base $server bird-iot-microservice
bash $base $server bird-iot-ai-starlight
bash $base $server bird-iot-scheduler-starlight