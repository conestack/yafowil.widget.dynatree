#!/bin/bash
#
# Watch source directory for changes and run rollup.sh. 
#
# Install dependencies:
#     sudo apt-install inotify-tools

while res=$(inotifywait -e create -e modify -e delete -e move ./js/src); do
    echo "changed: $res, run rollup"
    ./scripts/rollup.sh --configDebug
done
