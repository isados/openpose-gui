#!/bin/bash
# sudo docker run -it ubuntu bash &
firefox &
PRO_PID=$!
echo $! > pid.pid
#kill -9 $!
