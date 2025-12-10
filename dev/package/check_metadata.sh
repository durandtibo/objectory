#!/usr/bin/env bash

set -euo pipefail

METADATA=$(uv pip show objectory)

echo "$METADATA"

echo "$METADATA" | grep -zq "Name: objectory\n"
echo "$METADATA" | grep -zq "Requires:\n"
