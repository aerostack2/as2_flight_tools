#!/bin/bash
# usage

if [ -z $1 ]; then
    echo "Usage: $0 <hostname> without .local" 
    exit 1
fi

SSH_HOST=$1.local
CMD="systemctl restart NetworkManager.service"
TMUX_CMD="tmux new-session -d -s wifi_reset bash -c \"$CMD\""
ssh root@$SSH_HOST "${TMUX_CMD}"

