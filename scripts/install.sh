#!/bin/bash
#
# Install development environment.

set -e

./scripts/clean.sh

if ! which npm &> /dev/null; then
    sudo apt-get install npm
fi

npm --save-dev install \
    qunit \
    karma \
    karma-qunit \
    karma-coverage \
    karma-chrome-launcher \
    karma-module-resolver-preprocessor \
    rollup \
    rollup-plugin-cleanup \
    rollup-plugin-terser

npm --no-save install https://github.com/jquery/jquery#main

python3 -m venv .
./bin/pip install wheel
./bin/pip install -e .[test]
