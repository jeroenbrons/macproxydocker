#!/bin/bash
if [ -z "$USER_AGENT" ]; then
    /usr/local/bin/python3 /usr/src/app/proxy.py $@
else
    echo "user-agent requested"
    /usr/local/bin/python3 /usr/src/app/proxy.py --user-agent $USER_AGENT $@
fi