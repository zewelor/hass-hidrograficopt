---
applyTo: "script/**, .devcontainer/*.sh"
---

# Shell Script Instructions

**Applies to:** Shell scripts in `script/` and `**/.devcontainer/*.sh`

## Key Conventions

- Source `script/.lib/output.sh` for colored output and helpers
- Use `activate_venv` instead of open-coded activation logic
- Use `run_hook` for pre/post script extension points when applicable
- Quote variables and prefer `[[ ]]`
