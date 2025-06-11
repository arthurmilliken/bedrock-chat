#!/usr/bin/env bash

TMP_FILE=$(mktemp)
git ls-files --others --cached --exclude-standard > "$TMP_FILE"

{
  echo "# Project Index Tree"
  echo ""
  echo "Generated on: $(date)"
  echo ""
  echo "\`\`\`"
  echo "."
  sort "$TMP_FILE" | sed 's|^|├── |'
  echo "\`\`\`"
  echo ""
  echo "Total files: $(wc -l < "$TMP_FILE")"
} > INDEX_TREE.md

rm "$TMP_FILE"
echo "Project tree written to $(pwd) INDEX_TREE.md"