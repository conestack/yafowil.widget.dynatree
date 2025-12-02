#!/bin/bash
#
# Clean development environment.

set -e

to_remove=(
    bin build bundle dist include karma lib lib64 node_modules
    package-lock.json pyvenv.cfg share
)

for item in "${to_remove[@]}"; do
    if [ -e "$item" ]; then
        rm -r "$item"
    fi
done
