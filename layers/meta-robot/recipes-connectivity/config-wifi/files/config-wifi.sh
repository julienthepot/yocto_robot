#!/bin/bash

# This script configures WiFi settings on a meta-robot device.

rfkill unblock wifi

if [ "$?" -ne 0 ]; then
    echo "Failed to unblock WiFi. Exiting."
    exit 1
fi

connmanctl enable wifi