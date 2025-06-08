#!/usr/bin/env bash
# filepath: /home/arthur/src/bedrock-chat/scripts/devtools/clean-cdk.sh

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
CDK_DIR="cdk"
SCRIPT_NAME="$(basename "$0")"

# Colors for output (if terminal supports it)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    RED='' GREEN='' YELLOW='' BLUE='' NC=''
fi

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# Validate CDK directory exists
if [[ ! -d "$CDK_DIR" ]]; then
    log_error "CDK directory '$CDK_DIR' not found"
    log_info "Run this script from the project root containing the '$CDK_DIR' directory"
    exit 1
fi

log_info "Starting CDK cleanup in directory: $CDK_DIR"

# Change to CDK directory
cd "$CDK_DIR" || {
    log_error "Failed to change to CDK directory"
    exit 1
}

# Find files to delete (excluding node_modules and specific exceptions)
mapfile -t files_to_delete < <(
    find . \
        -type f \
        \( -name "*.js" -o -name "*.d.ts" \) \
        -not -path "./node_modules/*" \
        -not -path "./cdk.out/*" \
        -not -name "jest.config.js" \
        -not -name "*.min.js" \
        2>/dev/null
)

# Check if any files were found
if [[ ${#files_to_delete[@]} -eq 0 ]]; then
    log_info "No TypeScript compilation artifacts found to delete"
    exit 0
fi

# Display files that will be deleted
log_info "Found ${#files_to_delete[@]} file(s) to delete:"
printf '%s\n' "${files_to_delete[@]}" | sed 's/^/  - /'

# Confirm deletion (optional - remove if you want silent operation)
read -p "Proceed with deletion? [Y/n] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]?$ ]]; then
    log_warning "Deletion cancelled"
    exit 0
fi

# Delete files and track results
deleted_count=0
failed_count=0
failed_files=()

for file in "${files_to_delete[@]}"; do
    if rm -f "$file" 2>/dev/null; then
        log_success "Deleted: $file"
        ((deleted_count++))
    else
        log_error "Failed to delete: $file"
        failed_files+=("$file")
        ((failed_count++))
    fi
done

# Summary
echo
log_info "Cleanup completed:"
log_success "Successfully deleted: $deleted_count file(s)"

if [[ $failed_count -gt 0 ]]; then
    log_error "Failed to delete: $failed_count file(s)"
    printf '%s\n' "${failed_files[@]}" | sed 's/^/  - /'
    exit 1
fi

log_success "CDK cleanup completed successfully"