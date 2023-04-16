#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]; then
    if [[ $(uname -m) == 'arm64' ]]; then
        echo "darwin-arm64"
    else
        echo "darwin-amd64"
    fi
    # Do something under Mac OS X platform
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "linux-amd64"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    echo "windows-amd64"
fi