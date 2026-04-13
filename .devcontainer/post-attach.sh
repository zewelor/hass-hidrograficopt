#!/usr/bin/env bash

set -e

# Run user post-attach hook if present.
_hook_file="$(cd "$(dirname "$0")" && pwd)/hooks/post-attach.post.sh"
if [[ -f "$_hook_file" ]]; then
    echo "ℹ Running hook: .devcontainer/hooks/post-attach.post.sh"
    # shellcheck source=/dev/null
    source "$_hook_file"
fi
unset _hook_file
