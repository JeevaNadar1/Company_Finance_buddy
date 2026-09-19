#!/usr/bin/env bash
# Package the skill source tree into an installable .skill bundle.
#
# A .skill file is a zip whose single top-level directory is the skill name.
# The build is deterministic: fixed timestamps and sorted entries, so an
# unchanged source tree always produces a byte-identical bundle and the
# artifact diff in a PR means something.
#
# Usage: scripts/build.sh [skill_dir] [output_file]

set -euo pipefail

SKILL_DIR="${1:-company-finance-buddy}"
OUTPUT="${2:-${SKILL_DIR}.skill}"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

if [[ ! -d "$SKILL_DIR" ]]; then
  echo "build: skill directory '$SKILL_DIR' not found" >&2
  exit 1
fi

echo "==> validating"
python3 scripts/validate.py "$SKILL_DIR"

echo "==> staging"
# Copy only what belongs in the bundle. Anything else in the source tree
# (notes, scratch files, real client data) must not ship.
mkdir -p "$STAGE/$SKILL_DIR"
(cd "$SKILL_DIR" && find . -type f -name '*.md' -print0) \
  | while IFS= read -r -d '' f; do
      mkdir -p "$STAGE/$SKILL_DIR/$(dirname "$f")"
      cp "$SKILL_DIR/$f" "$STAGE/$SKILL_DIR/$f"
    done

# Deterministic timestamps.
find "$STAGE" -exec touch -t 198001010000 {} +

echo "==> packaging"
rm -f "$OUTPUT"
ABS_OUTPUT="$(cd "$(dirname "$OUTPUT")" && pwd)/$(basename "$OUTPUT")"
(cd "$STAGE" && find . -print0 | LC_ALL=C sort -z \
  | xargs -0 zip -X -q -0 "$ABS_OUTPUT")

SIZE=$(wc -c < "$OUTPUT" | tr -d ' ')
COUNT=$(unzip -l "$OUTPUT" | tail -1 | awk '{print $2}')
echo "==> built $OUTPUT  ${SIZE} bytes  ${COUNT} entries"
