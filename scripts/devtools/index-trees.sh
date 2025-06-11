#!/usr/bin/env bash

# Brief: Generate index trees for the main project and each major subdirectory

ORIGINAL_PWD=$(pwd)
SCRIPT_PATH="$ORIGINAL_PWD/scripts/devtools/generate-index-tree.sh"

# Check if the generate-index-tree.sh script exists
if [[ ! -f "$SCRIPT_PATH" ]]; then
    echo "Error: generate-index-tree.sh not found at $SCRIPT_PATH" >&2
    exit 1
fi

# Generate main project tree (level 1 only)
{
    echo "# Project Index Tree" 
    echo ""
    echo "Generated on: $(date)"
    echo ""
    echo "\`\`\`"
    if command -v tree >/dev/null 2>&1; then
        tree -L 1
    else
        echo "."
        ls -1 | sed 's/^/├── /'
    fi
    echo "\`\`\`"
} > INDEX_TREE.md

echo "Generated main INDEX_TREE.md"

# Generate trees for each subdirectory
for dir in cdk backend frontend overlays; do
    if [[ -d "$dir" ]]; then
        echo "Generating tree for $dir..."
        cd "$dir"
        
        # Run the script from the correct location
        "$SCRIPT_PATH"
        
        cd "$ORIGINAL_PWD"  # Return to original directory
        echo "Generated $dir/INDEX_TREE.md"
    else
        echo "Warning: Directory $dir does not exist, skipping..."
    fi
done

echo "All index trees generated successfully!"