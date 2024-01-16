#!/bin/bash

# Define SSH server information
SSH_SERVER="nx1-cvar.local"
SSH_PORT="22"
SSH_USER="cvar"
SSH_TIMEOUT=10  # Adjust the timeout as needed

# Check the SSH server
if nc -w $SSH_TIMEOUT -z $SSH_SERVER $SSH_PORT; then
    # SSH server is reachable
    START_TIME=$(date +%s.%N)
    if ssh -q -o BatchMode=yes -o ConnectTimeout=$SSH_TIMEOUT $SSH_USER@$SSH_SERVER exit; then
        END_TIME=$(date +%s.%N)
        LATENCY=$(echo "$END_TIME - $START_TIME" | bc)
        echo "$(date) - SSH server $SSH_SERVER is reachable with latency: $LATENCY seconds"
    else
        echo "$(date) - SSH server $SSH_SERVER is reachable, but connection failed"
    fi
else
    # SSH server is not reachable
    echo "$(date) - SSH server $SSH_SERVER is not reachable"
fi
