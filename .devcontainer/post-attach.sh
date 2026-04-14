#!/usr/bin/env bash
#
# .devcontainer/post-attach.sh - DevContainer Post-Attach Hook
#
# Runs automatically when attaching to an existing DevContainer.
# Detects fresh blueprint copies and triggers automatic initialization.
#

set -e

YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_color() {
    local color=$1
    shift
    echo -e "${color}$*${NC}" >&2
}

print_welcome_header() {
    local text="$1"
    local text_length=${#text}
    local padding_left=$(((78 - text_length) / 2))
    local padding_right=$((78 - text_length - padding_left))
    local left_spaces right_spaces
    left_spaces=$(printf "%${padding_left}s" "")
    right_spaces=$(printf "%${padding_right}s" "")

    echo ""
    print_color "$BLUE" "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
    print_color "$BLUE" "┃                                                                              ┃"
    print_color "$BLUE" "┃${left_spaces}${text}${right_spaces}┃"
    print_color "$BLUE" "┃                                                                              ┃"
    print_color "$BLUE" "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    echo ""
}

print_info() {
    print_color "$CYAN" "ℹ $1"
}

check_if_original_blueprint_repo() {
    if git rev-parse --git-dir >/dev/null 2>&1; then
        local remote_url
        remote_url=$(git remote get-url origin 2>/dev/null || echo "")
        if [[ "$remote_url" =~ jpawlowski.*(hacs\.)?integration[_.-]?blueprint ]]; then
            return 0
        fi
    fi
    return 1
}

check_if_needs_initialization() {
    if [[ ! -f "initialize.sh" ]]; then
        return 1
    fi

    if ! grep -q "ha_integration_domain" custom_components/*/manifest.json 2>/dev/null; then
        return 1
    fi

    if check_if_original_blueprint_repo; then
        return 1
    fi

    return 0
}

if check_if_needs_initialization; then
    print_welcome_header "🚀 Welcome to your new Home Assistant Integration!"
    print_info "This appears to be a fresh copy of the blueprint template."
    print_info "Starting automatic initialization process..."
    echo ""
    ./initialize.sh
elif check_if_original_blueprint_repo; then
    :
elif [[ ! -f "initialize.sh" ]]; then
    :
fi

if command -v npm >/dev/null 2>&1 && [[ -f package.json ]] && [[ -z "$(ls -A node_modules 2>/dev/null)" ]]; then
    print_color "$YELLOW" "⚠ node_modules is empty -- running npm ci to restore packages..."
    npm ci --silent
fi

_hook_file="$(cd "$(dirname "$0")" && pwd)/hooks/post-attach.post.sh"
if [[ -f "$_hook_file" ]]; then
    print_info "Running hook: .devcontainer/hooks/post-attach.post.sh"
    # shellcheck source=/dev/null
    source "$_hook_file"
fi
unset _hook_file
