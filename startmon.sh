#!/bin/bash

startcommand="python3 monitorscreen.py"

if pgrep -f "$startcommand" > /dev/null
then
    echo "System monitor already running"
else
    echo "Starting system monitor"
    cd ~/pgms/python/spidisplay
    $startcommand 2>/dev/null &
fi
