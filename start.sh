#!/bin/sh

service ssh start

cd /home/pi/SCS-Docker-pi/SCS/APP
/usr/local/bin/python3 main.py