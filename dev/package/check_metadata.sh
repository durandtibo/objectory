#!/usr/bin/env bash

set -euo pipefail

METADATA=$(uv pip show objectory)

echo "$METADATA"

# Check if the package "objectory" is installed
if ! echo "$METADATA" | grep -q "Name: objectory"; then
    echo "Error: 'objectory' package is not installed or not found in pip metadata!" >&2
    exit 1
fi

# Check if the package has no dependencies
if ! echo "$METADATA" | grep -zq "Requires:\nRequired-by:"; then
    echo "Error: 'objectory' package has dependencies listed." >&2
    exit 1
fi
