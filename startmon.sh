#!/bin/bash

startcommand="python3 monitorscreen.py"
codelocation="/home/wdaher/pgms/python/spidisplay"

if pgrep -f "$startcommand" > /dev/null
then
    echo "System monitor already running"
else
    echo "Starting system monitor"
    cd "$codelocation"
    $startcommand 2>/dev/null &
fi
