#!/bin/bash
cd /home/pi/agromeans/tools/bird-iot-deployment-starlight
python3 main.py -server $1 -repo $2

# start build&run container
cd /home/pi
bash $2.sh
rm -f $2.sh