#!/usr/bin/env bash

set -euo pipefail

OUTPUT=$(uv pip tree --package objectory --show-version-specifiers)
echo "$OUTPUT"

# Define patterns for each line (in order).
# Add as many patterns as needed.
PATTERNS=(
  '^objectory v[0-9]+(\.[0-9]+)*[A-Za-z0-9]*$'
)

# --- Validator ---
i=1
while IFS= read -r line; do
    pattern="${PATTERNS[$((i-1))]-}"

    if [[ -z "${pattern}" ]]; then
        echo "❌ No pattern defined for line $i"
        exit 1
    fi

    if ! [[ "$line" =~ $pattern ]]; then
        echo "❌ Line $i does NOT match expected pattern"
        echo "   Line content:    '$line'"
        echo "   Expected pattern: $pattern"
        exit 1
    fi

    ((i++))
done <<< "$OUTPUT"

echo "✅ All $((i-1)) lines match."
