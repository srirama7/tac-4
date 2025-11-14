# Claude Code Migration for ADW

## Overview

The ADW (AI Developer Workflow) system has been migrated to use **Claude Code CLI** for planning and implementation, while **Gemini API** is now reserved exclusively for SQL operations and natural language query generation.

### Why This Change?

- **Claude Code CLI** is more powerful for agentic workflows (planning, implementation, testing)
- **Gemini API** remains optimal for SQL description generation and analytics
- Better separation of concerns and technology stack
- Reduces dependency on a single LLM provider

---

## Architecture

### ADW Workflow (Claude Code CLI)

```
GitHub Issue
    ↓
ADW Planning (Claude Code CLI)
    ↓
Implementation (Claude Code CLI)
    ↓
Testing (Claude Code CLI)
    ↓
PR Creation (Claude Code CLI)
```

**Used for:**
- Issue classification (/classify_issue)
- Implementation planning (/feature, /bug, /chore)
- Code implementation (/implement)
- Testing and validation (/test)
- Pull request creation (/pull_request)
- Branch naming and git operations

### SQL Operations (Gemini API)

```
Natural Language Query
    ↓
Gemini API (Claude Code is not available)
    ↓
SQL Query + Execution
    ↓
Results
```

**Used for:**
- Random SQL description generation
- Natural language to SQL conversion (when Claude Code isn't available)
- Column statistics and data insights

---

## Setup Instructions

### 1. Install Claude Code CLI

```bash
# Install Claude Code (if not already installed)
curl https://claude.com/install.sh | bash

# Or follow: https://docs.claude.com/en/docs/claude-code/setup
```

### 2. Configure Environment Variables

Create `.env` file in the project root:

```bash
# .env

# Gemini API Key - REQUIRED for SQL operations
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.5-flash

# GitHub Configuration (Optional)
GITHUB_PAT=your-github-token-here

# Claude Code is auto-detected and uses configured model
# No additional configuration needed here
```

### 3. Configure Claude Code Model (Optional)

Edit `.claude/settings.json` to specify your preferred Claude model:

```json
{
  "model": "claude-opus-4-1",  // or claude-sonnet, etc.
  "temperature": 0.7,
  "max_tokens": 4096
}
```

### 4. Install Dependencies

```bash
cd adws
uv sync  # Installs python-dotenv and pydantic (no longer needs google-generativeai)
```

### 5. Verify Setup

```bash
# Check Claude Code CLI is available
which claude

# Check Gemini API key is configured
echo $GEMINI_API_KEY

# Run a test ADW workflow
cd adws
uv run adw_plan_build.py <issue-number>
```

---

## File Changes

### Modified Files

1. **adws/adw_modules/claude_code_agent.py** (NEW)
   - New module for Claude Code CLI integration
   - Executes slash commands via subprocess
   - Parses JSONL output from Claude Code CLI

2. **adws/adw_modules/workflow_ops.py**
   - Updated to use `claude_code_agent.execute_template()`
   - Changed all `model="gemini-2.5-flash"` to `model="claude-code"`
   - No longer imports Gemini agent module

3. **adws/pyproject.toml**
   - Removed `google-generativeai>=0.3.0` dependency
   - ADW now only depends on: python-dotenv, pydantic

4. **.env.sample**
   - Marked `GEMINI_API_KEY` as optional for ADW (required for SQL only)
   - Added comments explaining Claude Code configuration
   - Updated descriptions

---

## Migration Path

### For Existing ADW Users

1. No code changes needed in your GitHub workflows
2. Update `.env` file (remove Gemini API key requirement for ADW)
3. Install Claude Code CLI (if not already present)
4. Run `cd adws && uv sync` to update dependencies
5. Test with: `uv run adw_plan_build.py <issue-number>`

### Rollback (if needed)

If you need to revert to Gemini API for ADW:

```bash
git checkout HEAD -- adws/adw_modules/workflow_ops.py
git checkout HEAD -- adws/pyproject.toml
uv sync  # Re-installs google-generativeai
```

Then edit `.env` to restore `GEMINI_API_KEY`:

```bash
GEMINI_API_KEY=your-key-here
```

---

## SQL Operations Still Use Gemini

### Requirements

- `GEMINI_API_KEY` environment variable must be set
- `GEMINI_MODEL` defaults to `gemini-2.5-flash`

### Endpoints Affected

1. **POST /api/query** - Natural language to SQL conversion
2. **POST /api/random-sql** - Random SQL description generation
3. **POST /api/insights** - Column statistics generation

### Example Usage

```bash
# Random SQL description (uses Gemini)
curl -X POST http://localhost:8000/api/random-sql

# Natural language query (uses Gemini)
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "show me all customers from New York"}'
```

---

## Troubleshooting

### Claude Code CLI Not Found

```
Error: claude: command not found
```

**Solution:**
1. Install Claude Code: `curl https://claude.com/install.sh | bash`
2. Add to PATH: `export PATH="$PATH:$HOME/.claude/bin"`
3. Restart terminal

### Gemini API Key Error

```
Error: Failed to import google.generativeai
```

**Solution:**
1. Verify `.env` has `GEMINI_API_KEY` for SQL operations
2. Backend server still needs Gemini: `cd app/server && uv sync`
3. Check API key is valid at https://aistudio.google.com/app/apikey

### ADW Execution Fails

```
Error executing Claude Code command: ...
```

**Solution:**
1. Check Claude Code CLI is installed: `which claude`
2. Verify `.claude/settings.json` has valid configuration
3. Check GitHub PAT if using private repos: `echo $GITHUB_PAT`
4. Run with verbose logging: `export DEBUG=1 && uv run adw_plan_build.py <issue>`

### Slash Command Not Found

```
Error: /classify_issue not found
```

**Solution:**
1. Verify `.claude/commands/` directory exists with slash command files
2. Check Claude Code CLI is pointing to correct project root
3. Restart Claude Code: `claude --version`

---

## Command Mapping

| ADW Function | Command | Provider |
|---|---|---|
| Classify Issue | `/classify_issue` | Claude Code |
| Plan Feature | `/feature` | Claude Code |
| Plan Bug Fix | `/bug` | Claude Code |
| Plan Chore | `/chore` | Claude Code |
| Implement Plan | `/implement` | Claude Code |
| Generate Branch | `/generate_branch_name` | Claude Code |
| Create Commit | `/commit` | Claude Code |
| Create PR | `/pull_request` | Claude Code |
| Random SQL | `/random-sql` API call | Gemini API |
| NL to SQL | `/query` API call | Gemini API |

---

## Performance Notes

### Claude Code vs Gemini

| Aspect | Claude Code | Gemini |
|---|---|---|
| **Speed** | Fast (local execution) | Medium (API calls) |
| **Cost** | Included with Claude Code | Per-API-call billing |
| **Context** | Full file access | Limited by API |
| **Use Case** | Complex workflows | SQL generation |
| **Accuracy** | High for coding | High for SQL |

### Optimization Tips

1. **Batch ADW operations** - Process multiple issues in sequence
2. **Cache plans** - Reuse implementation plans when possible
3. **Use Gemini only for SQL** - Don't call Gemini for non-SQL tasks
4. **Monitor Claude Code logs** - Check `.claude/logs/` for performance

---

## Support

- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code/claude_code_docs_map.md
- **Gemini API Docs**: https://ai.google.dev/
- **GitHub Issues**: Report bugs and feature requests

---

## Summary

✅ **ADW now uses Claude Code CLI** for planning, implementation, and testing
✅ **Gemini API reserved for SQL operations** where it excels
✅ **Reduced dependencies** - No longer requires google-generativeai in ADW
✅ **Better performance** - Local execution + focused API usage
✅ **Easier setup** - Only one API key needed for SQL, Claude Code handles the rest
