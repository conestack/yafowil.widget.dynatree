#!/bin/bash
#
# Create JS bundles.

node_modules/rollup/dist/bin/rollup --config rollup.conf.js "$@"
