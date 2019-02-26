#!/bin/bash
# sudo docker run -it ubuntu bash &
qbittorrent &
PRO_PID=$!
echo $! > pid.pid
#kill -9 $!
