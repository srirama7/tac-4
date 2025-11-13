# Quick Start - ADW with Claude Code CLI Only

## Prerequisites
You only need:
1. ✅ Claude Code CLI installed & authenticated
   ```bash
   claude --version
   ```
2. ✅ GitHub CLI installed & authenticated
   ```bash
   gh auth login
   ```
3. ✅ Git installed
4. ✅ Python 3.11+ with uv installed

## NO ANTHROPIC_API_KEY NEEDED! 🎉

Claude Code CLI handles authentication automatically.

## Setup

```bash
# 1. Navigate to project
cd adws

# 2. Run the workflow (that's it!)
uv run adw_plan_build.py 13
```

Replace `13` with your GitHub issue number.

## What Happens

1. **Plan Phase**: AI analyzes the issue and creates an implementation plan
2. **Build Phase**: AI implements the solution based on the plan
3. **Git Operations**: Creates branches, commits, and can create PRs

## Optional Configuration

Create a `.env` file (copy from `.env.sample`) for optional settings:

```env
# GitHub - use different account than 'gh auth login'
GITHUB_PAT=ghp_xxxxxxxxxxxxx

# Only if 'claude' command is not in PATH
CLAUDE_CODE_PATH=/usr/local/bin/claude

# These are rarely needed
E2B_API_KEY=e2b_xxxxx
CLOUDFLARED_TUNNEL_TOKEN=xxxxx
```

## Verify Setup

```bash
# Check Claude Code is working
claude --version

# Check GitHub is authenticated
gh auth status

# Test the workflow
cd adws
uv run adw_plan_build.py 13
```

## Troubleshooting

### Claude Code CLI not found
```bash
which claude  # Find where it's installed
# Add to .env file:
CLAUDE_CODE_PATH=/path/to/claude
```

### GitHub authentication issues
```bash
gh auth login
gh auth status
```

### Python/uv issues
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python via uv
uv python install
```

## Logs & Output

Workflow logs are stored in:
```
agents/{adw_id}/adw_plan/execution.log
agents/{adw_id}/adw_build/execution.log
```

Implementation plans are saved in:
```
specs/issue-{issue_number}-adw-{adw_id}-*.md
```

## Need Help?

See `CLAUDE_CODE_ONLY_SETUP.md` for detailed technical information about how this works.
