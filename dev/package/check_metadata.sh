#!/usr/bin/env bash

set -euo pipefail

METADATA=$(uv pip show objectory)

echo "$METADATA"

echo "$METADATA" | grep -q "Name: objectory"
echo "$METADATA" | grep -q "Requires: tornado"
