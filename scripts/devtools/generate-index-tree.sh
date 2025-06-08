#!/usr/bin/env bash

# Brief: Generate a tree view of the project, skipping files/folders in .gitignore, and output to INDEX_TREE.md

# Check for required dependencies
if ! command -v git &>/dev/null; then
  echo "Error: git is required but not installed." >&2
  exit 1
fi

# Use git ls-files to list tracked and untracked (but not ignored) files, then build a tree
TMP_FILE=$(mktemp)
git ls-files --others --cached --exclude-standard > "$TMP_FILE"

# Function to build tree from file list
function build_tree {
  awk -F/ '
  {
    path = ""
    for (i = 1; i < NF; i++) {
      path = (path ? path "/" : "") $i
      if (!(path in seen)) {
        indent = ""
        for (j = 1; j < i; j++) indent = indent "  "
        print indent "├── " $i
        seen[path] = 1
      }
    }
    indent = ""
    for (j = 1; j < NF; j++) indent = indent "  "
    print indent "├── " $NF
  }' "$TMP_FILE" | sort | uniq
}

# Write header and tree to INDEX_TREE.md
{
  echo "# Project Index Tree"
  echo ""
  echo "\`\`\`"
  build_tree
  echo "\`\`\`"
} > INDEX_TREE.md

rm "$TMP_FILE"

echo "Project tree written to INDEX_TREE.md"