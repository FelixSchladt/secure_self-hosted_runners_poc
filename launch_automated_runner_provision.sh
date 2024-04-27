#!/bin/bash

# Check args
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <GITHUB_OWNER> <GITHUB_REPO> <GITHUB_PAT>"
    exit 1
fi

# Set env vars
export GITHUB_OWNER="$1"
export GITHUB_REPO="$2"
export GITHUB_PAT="$3"

# Launch server
echo "Starting FastAPI server..."
python3 automated_runner_provision.py

