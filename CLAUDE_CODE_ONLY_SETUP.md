# Claude Code Only Setup - No ANTHROPIC_API_KEY Required

## Summary

The ADW (AI Developer Workflow) project has been updated to work **exclusively with Claude Code CLI** without requiring an ANTHROPIC_API_KEY. Claude Code CLI handles authentication automatically, so no API key is needed.

## Changes Made

### 1. **adw_plan.py** - Removed API Key Check
- Updated `check_env_vars()` function to not require ANTHROPIC_API_KEY
- Claude Code CLI handles all authentication automatically

### 2. **adw_build.py** - Removed API Key Check
- Updated `check_env_vars()` function to not require ANTHROPIC_API_KEY
- Claude Code CLI handles all authentication automatically

### 3. **adw_modules/agent.py** - Updated Environment Handling
- **`get_claude_env()` function**: Changed from restrictive environment to inheriting parent environment
  - Claude Code CLI needs access to its own credentials and authentication tokens
  - Removed requirement for ANTHROPIC_API_KEY
  - Now properly inherits PATH and system variables needed for Claude Code CLI
  - Still supports optional GITHUB_PAT for GitHub operations

- **UTF-8 Encoding**: Added proper UTF-8 encoding for all file operations
  - `parse_jsonl_output()`: Now uses UTF-8 encoding
  - `convert_jsonl_to_json()`: Now uses UTF-8 with `ensure_ascii=False`

### 4. **.env.sample** - Updated Documentation
- Clearly marked ANTHROPIC_API_KEY as NOT REQUIRED
- Explains that Claude Code CLI handles authentication automatically
- Kept other optional configurations (GITHUB_PAT, CLAUDE_CODE_PATH, etc.)

## How It Works

### Before
```
ANTHROPIC_API_KEY=sk-ant-xxx  (REQUIRED)
CLAUDE_CODE_PATH=claude       (Optional)
```

### After
```
# ANTHROPIC_API_KEY not needed!
CLAUDE_CODE_PATH=claude       (Optional - defaults to 'claude')
GITHUB_PAT=ghp-xxx            (Optional - for GitHub operations)
```

## Running the Project

### Prerequisites
- Claude Code CLI installed and authenticated: `claude --version`
- GitHub CLI installed and authenticated: `gh auth login`
- Git installed
- Python 3.11+
- uv package manager

### Quick Start
```bash
# No need to set ANTHROPIC_API_KEY!
cd adws
uv run adw_plan_build.py 13
```

### What Happens
1. Claude Code CLI invokes the `claude` command (automatically authenticated)
2. Claude Code handles API authentication internally
3. GitHub operations use `gh` CLI (authenticated via `gh auth login`)
4. No ANTHROPIC_API_KEY needed anywhere

## Technical Details

### Why This Works
- **Claude Code CLI**: When you run `uv run`, it invokes the `claude` command which is already authenticated
- **Subprocess Environment**: By inheriting the parent environment (`os.environ.copy()`), subprocess calls can access:
  - User's PATH to find the `claude` CLI
  - Claude Code's internal authentication (stored in `~/.config/claude`)
  - System environment variables

### Why Restricting Environment Was Problematic
- Creating an empty or minimal environment (`env={}`) breaks:
  - PATH lookups for `claude` command
  - Claude Code's ability to find its own credentials
  - System commands like `git`, `gh`, etc.

## Files Modified

1. `adws/adw_plan.py` - Removed ANTHROPIC_API_KEY requirement
2. `adws/adw_build.py` - Removed ANTHROPIC_API_KEY requirement
3. `adws/adw_modules/agent.py` - Fixed environment handling & UTF-8 encoding
4. `.env.sample` - Updated documentation
5. `adws/__init__.py` - Created to make adws a proper Python package

## Testing

Run the following to verify the setup works:

```bash
cd adws
uv run adw_plan_build.py 13
```

Expected output:
- No "Missing required environment variables" error
- Script proceeds to plan generation and implementation phases
- Only Unicode encoding warnings from Windows console (these are harmless)

## Notes

- Unicode/emoji logging errors on Windows console are cosmetic and don't affect functionality
- All file I/O uses UTF-8 encoding to handle special characters properly
- GitHub operations still work via `gh` CLI (no additional config needed)
- Claude Code CLI authentication is cached in `~/.config/claude/`
