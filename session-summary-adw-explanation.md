# ADW System Comprehensive Guide
## Session Summary: Understanding Autonomous Development Workflows

*Generated from conversation session exploring the ADW (Autonomous Development Workflows) system*

---

## Table of Contents

1. [ADW System Health Check](#1-adw-system-health-check)
2. [ADW Plan & Build Workflow](#2-adw-plan--build-workflow)
3. [Pull Request #3: JSONL Upload Support](#3-pull-request-3-jsonl-upload-support)
4. [GitHub Integration Mechanism](#4-github-integration-mechanism)
5. [Understanding uv Package Manager](#5-understanding-uv-package-manager)
6. [Quick Reference Commands](#6-quick-reference-commands)

---

## 1. ADW System Health Check

### What is ADW?

ADW is an AI-powered development automation system that manages the entire software workflow automatically — from understanding project issues to writing code and creating pull requests. It uses artificial intelligence to analyze tasks, plan solutions, generate or modify code, test it, and update repositories — all with minimal human input. ADW helps developers speed up software delivery, maintain consistency, and reduce manual effort in coding and project management.

**ADW (Autonomous Development Workflows)** is an AI-powered software development automation system that integrates GitHub issues with Claude Code CLI to automatically:
- Classify issues (as /chore, /bug, or /feature)
- Generate implementation plans
- Implement solutions
- Create commits and pull requests

Think of it as an **AI developer** that can work autonomously on GitHub issues.

### Health Check Purpose

The health check script (`adws/health_check.py`) validates that your development environment is properly configured to run ADW workflows. It's a **pre-flight validation** system.

### Command

```bash
uv run adws/health_check.py         # Basic health check
uv run adws/health_check.py 2       # Health check + post to issue #2
```

### What Gets Checked

#### 1. Environment Variables Check ✅
**Validates:**
- `ANTHROPIC_API_KEY` (required) - Powers Claude Code
- `CLAUDE_CODE_PATH` (optional) - Path to Claude CLI (defaults to "claude")
- `GITHUB_PAT` (optional) - GitHub token (only needed for different account)
- `E2B_API_KEY` (optional) - Sandbox environment key
- `CLOUDFLARED_TUNNEL_TOKEN` (optional) - Webhook exposure

**Why it matters:**
Without the API key, Claude Code cannot execute AI-powered workflows.

#### 2. Git Repository Check ✅
**Validates:**
- You're in a valid git repository
- Can extract GitHub repository URL from `git remote`
- Checks if still using original "disler" repository (template warning)

**Why it matters:**
ADW needs to create branches, commits, and pull requests. Must know which GitHub repository to interact with.

#### 3. GitHub CLI Check ✅
**Validates:**
- `gh` (GitHub CLI) is installed
- Authentication status with `gh auth status`
- Respects `GITHUB_PAT` if set

**Why it matters:**
ADW uses GitHub CLI to:
- Fetch issue details
- Post comments to issues
- Create pull requests
- Manage issue labels and assignees

#### 4. Claude Code CLI Check ✅
**Validates:**
- Claude Code CLI is installed and functional
- Tests actual execution with simple prompt ("What is 2+2?")
- Uses Haiku model for fast, low-cost test
- Parses JSONL output to verify response
- Has 30-second timeout to prevent hanging

**Why it matters:**
This is the heart of ADW - Claude Code is the AI agent that does the development work. The health check performs a real API call to ensure end-to-end functionality.

### Example Output

```
🏥 Running ADW System Health Check...

✅ Overall Status: HEALTHY
📅 Timestamp: 2025-11-06T18:03:17.149799

📋 Check Results:
--------------------------------------------------

✅ Environment:
   claude_code_path: claude

✅ Git Repository:
   repo_url: https://github.com/srirama7/tac-4.git
   repo_path: srirama7/tac-4
   is_disler_repo: False

✅ Github Cli:
   installed: True
   authenticated: True

✅ Claude Code:
   test_passed: True
   response: 4
   auth_method: local_auth
```

### Issue Posting Feature

When you provide an issue number:
```bash
uv run adws/health_check.py 2
```

The script posts health check results as a comment to GitHub issue #2:
```
✅ Health check completed: HEALTHY
```

This is useful for:
- Documenting environment setup
- Debugging configuration issues
- Tracking system health over time
- Integration with ADW workflows

### Key Takeaways

1. **Pre-flight check** - Validates all prerequisites before running workflows
2. **Prevents failures** - Catches configuration issues early
3. **End-to-end testing** - Actually calls Claude API, not just checks installation
4. **Optional vs Required** - Distinguishes must-have from nice-to-have components

---

## 2. ADW Plan & Build Workflow

### Overview

The ADW Plan & Build system (`adws/adw_plan_build.py`) is an **autonomous AI-powered software development pipeline** that transforms GitHub issues into production-ready code and pull requests.

### What It Does

When you run:
```bash
uv run adws/adw_plan_build.py 2
```

The system automatically:
1. Fetches GitHub issue #2
2. Classifies it (as /chore, /bug, or /feature)
3. Creates a feature branch
4. Generates a detailed implementation plan
5. Implements the entire feature
6. Creates comprehensive tests
7. Makes commits (plan + implementation)
8. Opens a pull request

**All with zero human intervention!**

### The 8-Phase Workflow

#### Phase 0: Initialization
**Duration:** < 1 second

**What happens:**
- Generates unique ADW ID: `7a5e5d23`
- Validates environment variables
- Fetches GitHub issue from repository
- Posts comment: "Starting ADW workflow"
- Creates log file: `agents/7a5e5d23/adw_plan_build/execution.log`

#### Phase 1: Issue Classification
**Agent:** `issue_classifier`
**Slash Command:** `/classify_issue`
**Duration:** ~11 seconds

**How it works:**
- Sends issue JSON to Claude Code CLI
- Claude analyzes content and selects: `/chore`, `/bug`, or `/feature`
- Returns classification

**Example:**
```bash
claude -p "/classify_issue {issue_json}" --model sonnet
```

**Output:** `/feature`

**Artifacts created:**
```
agents/7a5e5d23/issue_classifier/
├── prompts/classify_issue.txt
├── raw_output.jsonl
└── raw_output.json
```

#### Phase 2: Branch Generation
**Agent:** `branch_generator`
**Slash Command:** `/generate_branch_name`
**Duration:** ~38 seconds

**How it works:**
- Claude generates branch name: `{type}-{number}-{adw_id}-{slug}`
- Creates and switches to branch

**Generated branch:** `feature-2-7a5e5d23-add-jsonl-upload-support`

**Git commands:**
```bash
git checkout main
git pull
git checkout -b feature-2-7a5e5d23-add-jsonl-upload-support
```

#### Phase 3: Plan Generation
**Agent:** `sdlc_planner`
**Slash Command:** `/feature`
**Duration:** ~3 minutes 35 seconds

**How it works:**
- Sends issue to Claude with `/feature` command
- Claude researches the codebase:
  - Reads README.md
  - Explores app/server/ and app/client/
  - Examines existing processors
  - Studies test patterns
- Creates comprehensive plan in `specs/*.md`

**Plan created:** `specs/jsonl-upload-support.md` (281 lines)

**Plan sections:**
- Feature Description
- User Story & Problem Statement
- Solution Statement
- Relevant Files (6 to modify, 3 to create)
- Implementation Plan (3 phases)
- Step-by-Step Tasks (8 detailed sections)
- Testing Strategy
- Acceptance Criteria (14 items)
- Validation Commands
- Design Notes

#### Phase 4: Plan File Discovery
**Agent:** `plan_finder`
**Slash Command:** `/find_plan_file`
**Duration:** ~12 seconds

**How it works:**
- Extracts file path from planner's output
- Returns: `specs/jsonl-upload-support.md`

**Why needed:** The planner returns a summary message, not just the file path.

#### Phase 5: Plan Commit
**Agent:** `sdlc_planner_committer`
**Slash Command:** `/commit`
**Duration:** ~30 seconds

**How it works:**
- Claude creates git commit
- Stages plan file
- Uses conventional commit format

**Commit created:**
```bash
git add specs/jsonl-upload-support.md
git commit -m "sdlc_planner: feature: add jsonl upload support"
```

#### Phase 6: Implementation
**Agent:** `sdlc_implementor`
**Slash Command:** `/implement`
**Duration:** ~8 minutes 12 seconds (longest phase)

**How it works:**
- Claude reads the 281-line plan
- Implements everything step-by-step
- Creates new files and modifies existing ones
- Writes comprehensive tests

**What was created:**
- 4 new test data files (JSONL samples)
- 1 new test file (436 lines, 29 tests)
- Modified 6 files (parser, server, UI, tests, README)
- Total: 824 lines changed

**Implementation details:**
- JSONL parser with line-by-line processing
- Nested field flattening (`user.city` → `user__city`)
- Array indexing (`tags[0]` → `tags_0`)
- Schema inference across all JSONL lines
- Error handling with line numbers
- Full test coverage

**Test results:**
- All 81 tests pass (29 new + 52 existing)
- Zero regressions

#### Phase 7: Implementation Commit
**Agent:** `sdlc_implementor_committer`
**Slash Command:** `/commit`
**Duration:** ~57 seconds

**How it works:**
- Claude stages all changes
- Creates implementation commit

**Commit created:**
```bash
git add <all modified and new files>
git commit -m "sdlc_implementor: feature: add jsonl upload support"
```

#### Phase 8: Pull Request Creation
**Agent:** `pr_creator`
**Slash Command:** `/pull_request`
**Duration:** ~3 minutes 44 seconds

**How it works:**
- Claude analyzes all commits
- Reads implementation plan
- Runs `git diff main...HEAD`
- Creates comprehensive PR description
- Uses `gh pr create`

**PR created:**
- URL: https://github.com/srirama7/tac-4/pull/3
- Title: "feat: #2 - jsonl"
- State: OPEN
- Includes summary, changes, test info, closes #2

### Architecture

#### Agent Specialization
Each agent has a single responsibility:
- `issue_classifier` - Only classifies issues
- `branch_generator` - Only creates branches
- `sdlc_planner` - Only creates plans
- `plan_finder` - Only extracts file paths
- `sdlc_implementor` - Only writes code
- `pr_creator` - Only creates PRs

**Why?** Smaller, focused prompts are more reliable.

#### Artifact Preservation
Every agent execution saves:
- Input prompt: `prompts/<command>.txt`
- Raw JSONL output: `raw_output.jsonl`
- Parsed JSON: `raw_output.json`

**Why?** Complete traceability, debugging, audit trail.

#### Unique Workflow IDs
Each run generates an ADW ID (e.g., `7a5e5d23`):
- Used in branch name
- Used in file paths
- Included in PR body

**Why?** Enables parallel workflows and easy artifact lookup.

### Claude Code CLI Integration

**Command structure:**
```bash
claude -p "<prompt>" \
  --model sonnet \
  --output-format stream-json \
  --verbose \
  --dangerously-skip-permissions
```

**Output format (JSONL):**
```jsonl
{"type":"system","subtype":"init","session_id":"462c3759-...","tools":[...],...}
{"type":"assistant","message":{"content":[{"type":"text","text":"/feature"}],...}
{"type":"result","subtype":"success","is_error":false,"result":"/feature",...}
```

**Result parsing:**
- Reads JSONL output
- Finds last `"type":"result"` message
- Extracts `result` field
- Determines success from `is_error` boolean

### Slash Command Templates

Templates are markdown files in `.claude/commands/`:

**Example: `/feature` template**
```markdown
# Feature Planning

Create a plan in specs/*.md to implement the Feature...

## Instructions
- Research the codebase
- Follow the Plan Format

## Feature
$ARGUMENTS
```

**How it works:**
1. Template files are markdown
2. Arguments are injected via `$ARGUMENTS`
3. Claude Code resolves the template
4. Enables reusable, version-controlled prompts

### Final Outcome

**What was created:**
- ✅ Feature branch: `feature-2-7a5e5d23-add-jsonl-upload-support`
- ✅ Implementation plan: 281 lines
- ✅ JSONL processor: 4 new functions
- ✅ Test files: 3 JSONL samples + 29 unit tests
- ✅ UI updates: HTML file input
- ✅ Documentation: Updated README
- ✅ Two commits: Plan + implementation
- ✅ Pull request: #3
- ✅ 824 total lines changed
- ✅ 81/81 tests passing

**Time:** ~18 minutes (vs hours/days for human)

**Ready for:**
- Human code review
- Merge to main
- Deployment to production

---

## 3. Pull Request #3: JSONL Upload Support

### Overview

Pull Request #3 implements JSONL (JSON Lines) file upload support for the Natural Language SQL Interface application.

**Stats:**
- Files Changed: 10 files
- Lines Added: +1,154
- Lines Removed: -15
- Tests Added: 29 new unit tests
- Status: OPEN
- Link: https://github.com/srirama7/tac-4/pull/3

### The Problem

The app previously only accepted CSV and JSON array files. Many real-world data sources export in JSONL format:
- Log aggregators (application logs, system events)
- Event streams (user activity, analytics)
- Data pipelines (ETL outputs, streaming data)
- Large datasets (too big for single JSON arrays)

Users had to manually convert JSONL to JSON/CSV before uploading.

### What is JSONL?

JSONL = JSON Lines. Each line is a separate JSON object:

```jsonl
{"id": 1, "name": "Alice", "age": 30}
{"id": 2, "name": "Bob", "age": 25}
{"id": 3, "name": "Charlie", "age": 35}
```

**Key Advantages:**
- Streamable (process line-by-line)
- Appendable (add records without modifying file)
- Industry standard (logs, pipelines, analytics)
- Fault tolerant (one bad line doesn't break file)

### Implementation Features

#### 1. JSONL Parser (`parse_jsonl_file`)
**Location:** `app/server/core/file_processor.py`

- Parses JSONL line-by-line
- Validates each line is valid JSON
- Skips empty lines
- Provides error messages with line numbers

#### 2. Nested Data Flattener (`flatten_record`)
**THE KILLER FEATURE**

Converts complex nested JSON into flat database columns:

**Nested Objects:**
```json
{"user": {"address": {"city": "NYC", "zip": "10001"}}}
```
Becomes:
```
user__address__city = "NYC"
user__address__zip = "10001"
```

**Arrays:**
```json
{"tags": ["python", "sql", "data"]}
```
Becomes:
```
tags_0 = "python"
tags_1 = "sql"
tags_2 = "data"
```

**Why this matters:** You can query nested data like "Show me users from NYC" without manual transformation!

#### 3. Schema Discovery (`discover_all_fields`)

Scans ALL records to find every possible field:

**Problem:** JSONL files often have inconsistent schemas:
```jsonl
{"id": 1, "name": "Alice"}
{"id": 2, "name": "Bob", "age": 30}
{"id": 3, "email": "charlie@example.com"}
```

**Solution:** Discovers all fields and creates complete table:
```
| id | name    | age  | email               |
|----|---------|------|---------------------|
| 1  | Alice   | NULL | NULL                |
| 2  | Bob     | 30   | NULL                |
| 3  | NULL    | NULL | charlie@example.com |
```

No data loss!

#### 4. Server Integration

Updated `app/server/server.py`:
```python
# Before
if not file.filename.endswith(('.csv', '.json')):
    raise HTTPException(400, "Only .csv and .json files supported")

# After
if not file.filename.endswith(('.csv', '.json', '.jsonl')):
    raise HTTPException(400, "Only .csv, .json, and .jsonl files supported")

elif file.filename.endswith('.jsonl'):
    result = convert_jsonl_to_sqlite(content, table_name)
```

#### 5. UI Updates

Updated `app/client/index.html`:
```html
<!-- Before -->
<p>Drag and drop .csv or .json files here</p>
<input type="file" accept=".csv,.json">

<!-- After -->
<p>Drag and drop .csv, .json, or .jsonl files here</p>
<input type="file" accept=".csv,.json,.jsonl">
```

### Test Coverage

#### Test Data Files
1. **test_simple.jsonl** - Basic 3-record file
2. **test_events.jsonl** - Complex nested structures
3. **test_logs.jsonl** - Application log format
4. **invalid.jsonl** - Malformed JSON for error tests

#### Test Suite (436 lines, 29 tests)
**Location:** `app/server/tests/core/test_jsonl_processor.py`

**4 Test Classes:**
1. **TestParseJSONLFile (8 tests)**
   - Simple parsing
   - Empty lines, whitespace
   - Invalid JSON with line numbers
   - Non-dict objects
   - Invalid UTF-8

2. **TestFlattenRecord (8 tests)**
   - Flat records
   - Nested objects
   - Deeply nested (3+ levels)
   - Arrays
   - Mixed structures
   - None values

3. **TestDiscoverAllFields (5 tests)**
   - Consistent schemas
   - Inconsistent schemas
   - Nested discovery
   - Arrays of different lengths

4. **TestConvertJSONLToSQLite (12 tests)**
   - Simple conversion
   - Nested objects
   - Arrays
   - Inconsistent schemas
   - Empty files
   - Malformed JSON
   - Real file integration
   - Table replacement

**Result:** All 81 tests passing (29 new + 52 existing)

### Real-World Example

**Upload application logs:**
```jsonl
{"timestamp": "2024-01-15T10:00:00Z", "level": "INFO", "message": "User logged in", "user": {"id": 101, "name": "Alice", "country": "USA"}}
{"timestamp": "2024-01-15T10:01:00Z", "level": "ERROR", "message": "Database timeout", "error": {"code": 500, "details": "Connection failed"}}
```

**Flattened columns created:**
- `timestamp`, `level`, `message`
- `user__id`, `user__name`, `user__country`
- `error__code`, `error__details`

**Now you can query:**
- "Show me all ERROR level logs"
- "Find logs from users in USA"
- "What errors had code 500?"

### Documentation Updates

**README.md sections updated:**
1. Features - Added JSONL support with flattening explanation
2. Usage - Explained automatic flattening
3. API Endpoints - Updated file format list
4. Security - Updated file validation list

### Value Delivered

**Before:**
- ❌ Manual conversion required
- ❌ Nested data must be flattened manually
- ❌ Inconsistent schemas problematic

**After:**
- ✅ Direct JSONL upload
- ✅ Automatic nested data flattening
- ✅ Inconsistent schemas handled
- ✅ Production-ready for real-world data

### Code Quality

**Strengths:**
- Comprehensive documentation (detailed docstrings)
- Extensive testing (436 lines, edge cases)
- Error handling (clear messages with line numbers)
- Recursive design (handles arbitrary nesting)
- Type hints (all functions annotated)
- No new dependencies (stdlib only)

---

## 4. GitHub Integration Mechanism

### How It Works Automatically

The ADW system automatically connects to your GitHub repository without manual configuration.

### Automatic Repository Discovery

**3-Step Process:**

**Step 1: Extract from Git**
```bash
git remote get-url origin
# Returns: https://github.com/srirama7/tac-4.git
```

**Step 2: Parse Owner and Repo**
```python
extract_repo_path(github_url)
# Input:  "https://github.com/srirama7/tac-4.git"
# Output: "srirama7/tac-4"
```

**Step 3: Use in GitHub CLI**
```bash
gh issue view 2 -R srirama7/tac-4
gh issue comment 2 -R srirama7/tac-4 --body "..."
gh pr create -R srirama7/tac-4 --title "..."
```

**Result:** Zero configuration needed!

### Authentication: Two Methods

#### Method 1: GitHub CLI Login (Recommended)
```bash
gh auth login
```
- Stores credentials in GitHub CLI's credential store
- All `gh` commands automatically authenticated
- ADW inherits this authentication
- No environment variables needed

#### Method 2: Personal Access Token (Optional)
```bash
export GITHUB_PAT="ghp_xxxxxxxxxxxxx"
```
- Use different GitHub account
- Gets converted to `GH_TOKEN` internally
- Overrides `gh auth login`

### Key Files

#### `adws/github.py` - Core Integration

**`get_github_env()`**
```python
def get_github_env() -> Optional[dict]:
    github_pat = os.getenv("GITHUB_PAT")
    if not github_pat:
        return None  # Inherit parent environment

    return {
        "GH_TOKEN": github_pat,
        "PATH": os.environ.get("PATH", ""),
    }
```

**`get_repo_url()`**
```python
def get_repo_url() -> str:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()
```

**`extract_repo_path()`**
```python
def extract_repo_path(github_url: str) -> str:
    return github_url.replace("https://github.com/", "").replace(".git", "")
```

**`fetch_issue()`**
```python
def fetch_issue(issue_number: str, repo_path: str) -> GitHubIssue:
    cmd = ["gh", "issue", "view", issue_number, "-R", repo_path, "--json", "..."]
    env = get_github_env()
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    # Parse and return GitHubIssue model
```

**`make_issue_comment()`**
```python
def make_issue_comment(issue_id: str, comment: str) -> None:
    repo_path = extract_repo_path(get_repo_url())
    cmd = ["gh", "issue", "comment", issue_id, "-R", repo_path, "--body", comment]
    env = get_github_env()
    subprocess.run(cmd, env=env)
```

#### `adws/agent.py` - Claude Code Environment

**`get_claude_env()`**
```python
def get_claude_env() -> Dict[str, str]:
    env = {
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "PATH": os.getenv("PATH"),
        # ... other vars
    }

    github_pat = os.getenv("GITHUB_PAT")
    if github_pat:
        env["GITHUB_PAT"] = github_pat
        env["GH_TOKEN"] = github_pat

    return env
```

### Authentication Flow

#### Scenario 1: Using `gh auth login` (No GITHUB_PAT)

```
User authenticates:
  $ gh auth login
  ↓
Credentials stored in GitHub CLI
  ↓
ADW runs: adw_plan_build.py
  ↓
get_github_env() → returns None
  ↓
subprocess.run([gh, ...], env=None)
  ↓
Inherits parent environment
  ↓
gh CLI finds credentials
  ↓
GitHub API calls succeed ✓
```

#### Scenario 2: Using GITHUB_PAT

```
User sets variable:
  $ export GITHUB_PAT="ghp_xxx..."
  ↓
ADW runs: adw_plan_build.py
  ↓
get_github_env() → returns {"GH_TOKEN": "ghp_xxx...", ...}
  ↓
subprocess.run([gh, ...], env=custom_env)
  ↓
gh CLI uses GH_TOKEN
  ↓
GitHub API calls succeed ✓
```

### Complete Flow Example

When you ran `uv run adws/adw_plan_build.py 2`:

**1. Repository Discovery**
```python
github_repo_url = get_repo_url()  # git remote get-url origin
repo_path = extract_repo_path(github_repo_url)  # srirama7/tac-4
```

**2. Issue Fetching**
```python
issue = fetch_issue("2", "srirama7/tac-4")
# Executes: gh issue view 2 -R srirama7/tac-4 --json ...
```

**3. Comment Posting**
```python
make_issue_comment("2", "Starting ADW workflow")
# Executes: gh issue comment 2 -R srirama7/tac-4 --body "..."
```

**4. PR Creation** (via Claude Code)
```python
# Claude runs: gh pr create -R srirama7/tac-4 --title "..." --body "..."
```

### Key Design Principles

1. **Zero Configuration** - Works out-of-box with `gh auth login`
2. **Automatic Discovery** - Repository from git remote
3. **Flexible Authentication** - Supports local auth and PAT
4. **Environment Inheritance** - Subprocesses inherit credentials
5. **Minimal Custom Environment** - Only when `GITHUB_PAT` set

### Summary: The "Automatic" Parts

| What Gets Configured | How |
|---------------------|-----|
| Repository URL | From `git remote get-url origin` |
| Repository Owner | Parsed from URL |
| Repository Name | Parsed from URL |
| GitHub Auth | Inherited from `gh auth login` |
| Issue Access | Via `gh issue view {number} -R {owner}/{repo}` |
| Comment Posting | Via `gh issue comment {number} -R {owner}/{repo}` |
| PR Creation | Via `gh pr create -R {owner}/{repo}` |

**You only did:**
1. `gh auth login` (one-time)
2. Clone/fork repository
3. Run: `uv run adws/adw_plan_build.py 2`

**Everything else was automatic!**

---

## 5. Understanding uv Package Manager

### What is uv?

**uv** is a modern, ultra-fast Python package manager and project management tool created by Astral (makers of `ruff`).

**Key Features:**
- ⚡ 10-100x faster than pip (written in Rust)
- 🔒 Automatic virtual environment management
- 📦 Inline script dependencies (PEP 723)
- 🐍 Python version management
- 🎯 Single tool replacing pip, virtualenv, pip-tools, poetry

### What Does `uv run` Do?

`uv run` executes Python scripts with automatic environment and dependency management.

### Traditional vs uv Workflow

**Traditional (manual):**
```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install python-dotenv pydantic

# Run script
python adws/health_check.py
```

**uv (automatic):**
```bash
uv run adws/health_check.py
```

One command does everything!

### How `uv run adws/health_check.py` Works

#### 1. uv Reads Script Metadata

The script has PEP 723 inline metadata:
```python
#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "python-dotenv",
#     "pydantic",
# ]
# ///
```

This tells uv:
- Python 3.12+ required
- Two dependencies needed

#### 2. uv Creates/Reuses Virtual Environment

- Creates temporary virtual environment (cached in `~/.cache/uv/`)
- Checks if dependencies already installed
- Reuses cached environment if dependencies match

#### 3. uv Installs Dependencies

If not cached:
- Downloads packages
- Installs them (blazingly fast)
- Caches for future runs

#### 4. uv Executes Script

- Activates virtual environment
- Runs: `python adws/health_check.py`
- Script imports dependencies
- Script executes

#### 5. Script Outputs Results

Health check runs and displays results.

### Key Benefits

**1. No Manual Virtual Environment Setup**
```bash
# Don't need this anymore:
python -m venv .venv
source .venv/bin/activate
```

**2. Dependencies Declared in Script**
Script is self-contained. Anyone can run it without:
- Reading requirements.txt
- Installing dependencies manually
- Figuring out Python version

**3. Fast Execution**
- First run: Installs dependencies (very fast)
- Subsequent runs: Uses cached environment (instant)

**4. Reproducible**
Every execution uses exact same environment:
- Same Python version
- Same dependency versions
- No "works on my machine" issues

**5. Multiple Scripts, Multiple Environments**
Each script can have different dependencies:
- `health_check.py` needs: `python-dotenv`, `pydantic`
- `trigger_webhook.py` might need: `flask`, `requests`

uv manages separate cached environments automatically.

### Comparison Table

| Feature | `python script.py` | `uv run script.py` |
|---------|-------------------|--------------------|
| Virtual env | Manual setup | Automatic |
| Dependencies | Must pre-install | Auto-installs from script |
| Python version | Whatever's installed | Can specify in script |
| Speed | Fast (once setup) | Fast (after first run) |
| Portability | Requires setup docs | Self-contained |
| Caching | Manual | Automatic global cache |
| Isolation | Depends on activation | Always isolated |

### Why This Project Uses uv

**1. ADW Scripts** (Self-contained)
```bash
uv run adws/health_check.py      # Inline deps
uv run adws/adw_plan_build.py 2  # Inline deps
uv run adws/trigger_webhook.py   # Inline deps
```

**2. Backend Development**
```bash
cd app/server
uv sync --all-extras    # Install from pyproject.toml
uv run python server.py # Run FastAPI server
uv run pytest           # Run tests
```

**3. Speed & Simplicity**
From README: "⚡ Fast development with Vite and uv"

- No virtualenv commands to remember
- No dependency installation delays
- Scripts "just work" on any machine

### PEP 723: Inline Script Metadata

**Standardized format:**
```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "python-dotenv",
#     "pydantic",
# ]
# ///
```

**Allows tools like uv to:**
- Parse dependencies from script itself
- Create appropriate isolated environments
- Make scripts truly portable

### Project Files

**1. `app/server/pyproject.toml`**
- Defines main application dependencies
- Used by `uv sync`

**2. `app/server/uv.lock`**
- Lock file for reproducible builds
- Contains exact dependency versions

**3. `adws/health_check.py`**
- Self-contained with inline dependencies
- Uses PEP 723 metadata

### Summary

`uv run adws/health_check.py` is a modern Python execution command that:

✅ Automatically manages virtual environments
✅ Installs dependencies declared in script
✅ Executes in isolated environment
✅ Caches everything for fast subsequent runs
✅ Makes scripts self-contained and portable

**In simple terms:** Smart assistant that sets up the perfect Python environment for your script, then cleans up after. All automatically, all blazingly fast. 🚀

---

## 6. Quick Reference Commands

### Health Check
```bash
# Basic health check
uv run adws/health_check.py

# Health check + post to issue #2
uv run adws/health_check.py 2
```

### ADW Plan & Build Workflow
```bash
# Process GitHub issue #2
uv run adws/adw_plan_build.py 2

# Process any issue number
uv run adws/adw_plan_build.py <issue_number>
```

### GitHub CLI Setup
```bash
# Initial authentication
gh auth login

# Check authentication status
gh auth status

# View issue
gh issue view 2

# View PR
gh pr view 3
```

### Git Operations
```bash
# Check repository URL
git remote get-url origin

# View branches
git branch -a

# View commits on feature branch
git log feature-2-7a5e5d23-add-jsonl-upload-support

# View changes in PR
git diff main...feature-2-7a5e5d23-add-jsonl-upload-support
```

### uv Commands
```bash
# Run script with inline dependencies
uv run <script.py>

# Install project dependencies
cd app/server && uv sync --all-extras

# Add dependency
uv add <package>

# Remove dependency
uv remove <package>

# Run tests
uv run pytest
```

### Backend Development
```bash
# Install dependencies
cd app/server
uv sync --all-extras

# Run server
uv run python server.py

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=core --cov-report=html
```

### Examining ADW Artifacts
```bash
# View ADW workflow logs
cat agents/<adw_id>/adw_plan_build/execution.log

# View agent prompts
cat agents/<adw_id>/<agent_name>/prompts/<command>.txt

# View agent outputs
cat agents/<adw_id>/<agent_name>/raw_output.json

# View implementation plan
cat specs/<feature-name>.md
```

### Environment Setup
```bash
# Check Python version
python --version

# Check uv version
uv --version

# Check gh CLI version
gh --version

# Check Claude Code CLI
claude --version

# Check git version
git --version
```

---

## Appendix: Key Concepts

### ADW (Autonomous Development Workflows)
AI-powered system that automatically converts GitHub issues into working code and pull requests using Claude Code CLI.

### PEP 723
Python Enhancement Proposal for inline script metadata, allowing scripts to declare their dependencies directly.

### JSONL (JSON Lines)
File format where each line is a valid JSON object, commonly used for streaming data and logs.

### GitHub CLI (`gh`)
Official command-line tool for GitHub, used by ADW to interact with issues, PRs, and comments.

### Claude Code CLI
Anthropic's command-line interface for Claude AI, the engine powering autonomous development.

### Slash Commands
Reusable prompt templates stored in `.claude/commands/` as markdown files.

### Agent
Specialized Claude Code CLI invocation with a specific purpose (e.g., classifier, planner, implementor).

### ADW ID
Unique 8-character identifier for each workflow run, used for traceability and artifact organization.

---

## Summary

This document captures a comprehensive exploration of the **ADW (Autonomous Development Workflows)** system, covering:

1. **Health Check System** - Pre-flight validation ensuring all tools and authentication are configured
2. **Plan & Build Workflow** - 8-phase autonomous pipeline from GitHub issue to pull request
3. **Real Implementation Example** - JSONL upload feature with 824 lines of code, tests, and documentation
4. **GitHub Integration** - Automatic repository discovery and authentication mechanism
5. **Modern Tooling** - uv package manager for fast, reproducible Python workflows

The ADW system represents a significant advancement in software development automation, enabling AI to autonomously handle the complete SDLC from planning through implementation to pull request creation.

**Total time for PR #3:** ~18 minutes (vs hours/days for human developer)
**Code quality:** Production-ready with comprehensive tests and zero regressions
**Developer experience:** Single command execution with automatic environment management

---

*Generated: 2025-11-07*
*Session: ADW System Exploration*
*Repository: srirama7/tac-4*

# GitHub Integration: How Terminal Commands Save to GitHub

## Overview

This document explains how the ADW system posts updates, comments, and pull requests to your GitHub repository directly from your terminal. Understanding this flow helps clarify how local automation connects to GitHub's cloud infrastructure.

---

## The Question

**"How come all the issues are getting saved in GitHub through my terminal which is present in my GitHub?"**

### Short Answer

Your terminal uses the **GitHub CLI** (`gh`) with your authenticated credentials to make API calls to GitHub.com. When ADW runs commands like "post comment to issue #2", it's using YOUR GitHub account credentials that you set up with `gh auth login`.

---

## The Complete Flow: Terminal → GitHub

### What You See in Your Terminal

When you run:
```bash
uv run adws/adw_plan_build.py 2
```

Terminal output shows:
```
Successfully posted comment to issue #2
Successfully posted comment to issue #2
Successfully posted comment to issue #2
...
Pull request created: https://github.com/srirama7/tac-4/pull/3
ADW workflow completed successfully
```

### What Happens Behind the Scenes (10 Steps)

#### Step 1: You Execute ADW Script
```bash
$ uv run adws/adw_plan_build.py 2
```

Your terminal runs the Python script that orchestrates the entire workflow.

#### Step 2: Python Script Posts Status Update
```python
from adws.github import make_issue_comment

make_issue_comment("2", "Starting ADW workflow")
make_issue_comment("2", "Issue classified as: /feature")
make_issue_comment("2", "Building implementation plan")
# ... more updates throughout workflow
```

The Python code calls the `make_issue_comment()` function multiple times during the workflow.

#### Step 3: make_issue_comment() Extracts Repository Info
```python
def make_issue_comment(issue_id: str, comment: str) -> None:
    # Get repository URL from git
    github_repo_url = get_repo_url()
    # Returns: https://github.com/srirama7/tac-4.git

    # Extract owner/repo path
    repo_path = extract_repo_path(github_repo_url)
    # Returns: srirama7/tac-4
```

The system automatically determines which repository to post to by reading your git remote configuration.

#### Step 4: Build GitHub CLI Command
```python
    cmd = [
        "gh",                    # GitHub CLI
        "issue",                 # Issue operations
        "comment",               # Post comment
        issue_id,                # "2"
        "-R", repo_path,         # -R srirama7/tac-4
        "--body", comment        # Comment text
    ]
```

This constructs the command: `gh issue comment 2 -R srirama7/tac-4 --body "Starting ADW workflow"`

#### Step 5: Execute as Subprocess
```python
    env = get_github_env()  # Get authentication environment
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env
    )
```

Python runs the GitHub CLI command as a subprocess, just like you would run it manually in your terminal.

#### Step 6: GitHub CLI Reads Your Auth Token

The `gh` command reads your authentication token from:
- **Location:** `~/.config/gh/hosts.yml` (Linux/Mac) or `%APPDATA%\GitHub CLI\hosts.yml` (Windows)
- **Token format:** `gho_xxxxxxxxxxxxxxxxxxxxx` (OAuth token)
- **Created when:** You ran `gh auth login`

#### Step 7: GitHub CLI Sends HTTPS API Request

The `gh` command translates to a GitHub API call:
```http
POST https://api.github.com/repos/srirama7/tac-4/issues/2/comments
Authorization: Bearer gho_xxxxxxxxxxxxxxxxxxxxx
Content-Type: application/json

{
  "body": "Starting ADW workflow"
}
```

This is a standard REST API call to GitHub's servers.

#### Step 8: GitHub Servers Process Request

GitHub's backend:
1. **Authenticates:** Validates your OAuth token
2. **Identifies:** Determines the token belongs to user `srirama7`
3. **Authorizes:** Checks if `srirama7` has permission to comment on issue #2
4. **Creates:** Inserts the comment into the database
5. **Records:** Logs the comment as created by `srirama7` at current timestamp
6. **Notifies:** Triggers notifications for issue watchers

#### Step 9: GitHub API Responds

GitHub returns success response:
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1234567890,
  "user": {
    "login": "srirama7",
    "id": 12345678
  },
  "body": "Starting ADW workflow",
  "created_at": "2025-11-06T17:46:28Z",
  "html_url": "https://github.com/srirama7/tac-4/issues/2#issuecomment-1234567890"
}
```

#### Step 10: Python Script Prints Confirmation

```python
if result.returncode == 0:
    print("Successfully posted comment to issue #2")
```

Your terminal displays the success message, and the comment is immediately visible on GitHub.com.

---

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                        │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Terminal: uv run adws/adw_plan_build.py 2        │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                 │
│                       ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Python Script: adws/adw_plan_build.py            │   │
│  │ - Orchestrates workflow                          │   │
│  │ - Calls make_issue_comment() multiple times      │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                 │  
│                       ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Python: adws/github.py                           │   │
│  │ - get_repo_url() → git remote get-url origin     │   │
│  │ - extract_repo_path() → srirama7/tac-4           │   │
│  │ - Builds gh command                              │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                 │
│                       ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Subprocess: gh issue comment 2                   │   │
│  │ -R srirama7/tac-4 --body "..."                   │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                 │
│                       ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │ GitHub CLI reads authentication token            │   │
│  │ File: ~/.config/gh/hosts.yml                     │   │
│  │ Token: gho_xxxxxxxxxxxxxxxxxxxxx                 │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                 │
└───────────────────────┼─────────────────────────────────┘
                        │
                        │ HTTPS Request
                        │ (with OAuth token)
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   GITHUB.COM SERVERS                    │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │ API Endpoint: /repos/srirama7/tac-4/issues/2     │   │
│  │ /comments                                        │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                 │
│                       ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Authentication Layer                             │   │
│  │ - Validates OAuth token                          │   │
│  │ - Identifies user: srirama7                      │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                 │
│                       ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Authorization Layer                              │   │
│  │ - Checks: Can srirama7 comment on issue #2?      │   │
│  │ - Result: ✅ YES (user has write access)         │  │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                 │
│                       ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Database Layer                                   │   │
│  │ - INSERT INTO issue_comments (...)               │   │
│  │ - created_by = srirama7                          │   │
│  │ - created_at = 2025-11-06T17:46:28Z              │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                  │
│                       ▼                                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Notification Layer                               │   │
│  │ - Notify issue watchers                          │   │
│  │ - Send webhooks                                  │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                  │
│                       │ HTTP Response                    │
│                       │ 201 Created                      │
└───────────────────────┼──────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                         │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Terminal Output:                                 │   │
│  │ "Successfully posted comment to issue #2"        │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘

                        AND

┌─────────────────────────────────────────────────────────┐
│                   WEB BROWSER                            │
│                                                          │
│  https://github.com/srirama7/tac-4/issues/2             │
│                                                          │
│  💬 Comment appears instantly:                          │
│  srirama7 commented 1 minute ago                        │
│  "Starting ADW workflow"                                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Why Comments Appear Under Your Account

The comments and pull requests appear under your GitHub account (`srirama7`) because:

### 1. You Authenticated Your Terminal

When you ran:
```bash
gh auth login
```

**What happened:**
1. GitHub CLI opened your browser
2. You logged into GitHub with your credentials
3. You authorized "GitHub CLI" application
4. GitHub generated an OAuth token tied to your account
5. Token was saved to your local machine
6. Token grants GitHub CLI permission to act as YOU

### 2. Your Token = Your Identity

Every API call includes your OAuth token:
```http
Authorization: Bearer gho_xxxxxxxxxxxxxxxxxxxxx
```

GitHub checks this token and determines:
- **User:** srirama7
- **Permissions:** Can read, write, create PRs on srirama7/tac-4
- **Scope:** All actions taken with this token are recorded as done by srirama7

### 3. GitHub Records Your Identity

When a comment is created, GitHub stores:
```json
{
  "user": {
    "login": "srirama7",
    "id": 12345678
  },
  "created_at": "2025-11-06T17:46:28Z"
}
```

On GitHub.com, this displays as:
```
srirama7 commented 1 minute ago
Starting ADW workflow
```

---

## Security: How GitHub Verifies It's You

### OAuth Token-Based Authentication

**Token characteristics:**
- **Format:** `gho_` prefix (GitHub OAuth token)
- **Length:** 36-40 characters
- **Scope:** Configurable permissions (repo, issues, pr, etc.)
- **Expiration:** Can be set to expire
- **Revocable:** Can be revoked anytime from GitHub settings

**Storage location:**
```
Windows: %APPDATA%\GitHub CLI\hosts.yml
Linux/Mac: ~/.config/gh/hosts.yml
```

**File contents:**
```yaml
github.com:
    user: srirama7
    oauth_token: gho_xxxxxxxxxxxxxxxxxxxxx
    git_protocol: https
```

### GitHub's Verification Process

**For each API request:**

1. **Extract token** from `Authorization` header
2. **Lookup token** in GitHub's database
3. **Verify:**
   - Token exists and is valid
   - Token hasn't been revoked
   - Token hasn't expired
4. **Identify user** associated with token
5. **Check permissions:**
   - Does user have access to repository?
   - Does user have permission for this action?
   - Does token scope include required permissions?
6. **Execute or reject** based on verification results

---

## What Gets Saved to GitHub from ADW

During the workflow execution, these items are created/updated on GitHub:

### Issue Comments (via `gh issue comment`)
1. ✅ "Starting ADW workflow"
2. ✅ "Issue classified as: /feature"
3. ✅ "Working on branch: feature-2-7a5e5d23-add-jsonl-upload-support"
4. ✅ "Implementation plan created"
5. ✅ "Solution implemented"
6. ✅ "Pull request created: https://github.com/srirama7/tac-4/pull/3"
7. ✅ "ADW workflow completed successfully"

**View at:** https://github.com/srirama7/tac-4/issues/2

### Git Commits (via `git push`)
```bash
git push origin feature-2-7a5e5d23-add-jsonl-upload-support
```
- Commit 1: "sdlc_planner: feature: add jsonl upload support"
- Commit 2: "sdlc_implementor: feature: add jsonl upload support"

### Pull Request (via `gh pr create`)
```bash
gh pr create -R srirama7/tac-4 --title "feat: #2 - jsonl" --body "..."
```
- Title: "feat: #2 - jsonl"
- Description: Comprehensive PR summary
- Links to issue #2
- Status: OPEN

**View at:** https://github.com/srirama7/tac-4/pull/3

---

## Code Implementation Details

### Key Functions in `adws/github.py`

#### get_repo_url()
```python
def get_repo_url() -> str:
    """Get GitHub repository URL from git remote."""
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()
    # Returns: https://github.com/srirama7/tac-4.git
```

#### extract_repo_path()
```python
def extract_repo_path(github_url: str) -> str:
    """Extract owner/repo from GitHub URL."""
    return github_url.replace("https://github.com/", "").replace(".git", "")
    # Input:  https://github.com/srirama7/tac-4.git
    # Output: srirama7/tac-4
```

#### get_github_env()
```python
def get_github_env() -> Optional[dict]:
    """Get environment variables for GitHub CLI."""
    github_pat = os.getenv("GITHUB_PAT")

    if not github_pat:
        return None  # Use default gh auth login credentials

    # If GITHUB_PAT is set, use it instead
    return {
        "GH_TOKEN": github_pat,
        "PATH": os.environ.get("PATH", ""),
    }
```

#### make_issue_comment()
```python
def make_issue_comment(issue_id: str, comment: str) -> None:
    """Post a comment to a GitHub issue."""
    # Automatically get repository from git
    github_repo_url = get_repo_url()
    repo_path = extract_repo_path(github_repo_url)

    # Build GitHub CLI command
    cmd = [
        "gh", "issue", "comment", issue_id,
        "-R", repo_path,
        "--body", comment
    ]

    # Execute with appropriate authentication
    env = get_github_env()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env
    )

    if result.returncode != 0:
        raise Exception(f"Failed to post comment: {result.stderr}")
```

---

## Verification Commands

You can verify the GitHub integration yourself with these commands:

### Check Your GitHub Authentication
```bash
gh auth status
```

**Expected output:**
```
github.com
  ✓ Logged in to github.com as srirama7 (oauth_token)
  ✓ Git operations for github.com configured to use https protocol.
  ✓ Token: gho_************************************
```

### Check Which User You're Authenticated As
```bash
gh api user
```

**Returns your GitHub user info:**
```json
{
  "login": "srirama7",
  "id": 12345678,
  "name": "Your Name",
  "email": "your.email@example.com"
}
```

### Check Repository Connection
```bash
git remote get-url origin
```

**Returns:**
```
https://github.com/srirama7/tac-4.git
```

### Post a Test Comment Manually
```bash
gh issue comment 2 -R srirama7/tac-4 --body "Test comment from terminal"
```

Then check https://github.com/srirama7/tac-4/issues/2 - you'll see it appear instantly!

### View Issue Comments via CLI
```bash
gh issue view 2 -R srirama7/tac-4 --comments
```

Shows all comments on the issue, including those posted by ADW.

---

## Two Authentication Methods

### Method 1: gh auth login (Recommended)

**Setup:**
```bash
gh auth login
```

**How it works:**
- Token stored locally by GitHub CLI
- ADW inherits authentication from environment
- No additional configuration needed
- Most secure and convenient

**Code behavior:**
```python
env = get_github_env()  # Returns None
subprocess.run(["gh", "issue", "comment", ...], env=None)
# Inherits parent environment with gh credentials
```

### Method 2: GITHUB_PAT Environment Variable (Optional)

**Setup:**
```bash
export GITHUB_PAT="ghp_xxxxxxxxxxxxxxxxxxxxx"
```

**When to use:**
- Want to use a different GitHub account than `gh auth login`
- Need fine-grained control over token scopes
- Using in CI/CD where `gh auth login` isn't practical

**Code behavior:**
```python
env = get_github_env()  # Returns {"GH_TOKEN": "ghp_xxx...", ...}
subprocess.run(["gh", "issue", "comment", ...], env=env)
# Uses custom GH_TOKEN instead of default credentials
```

---

## Frequently Asked Questions

### Q: Why do comments appear under my username?

**A:** Because you authenticated with `gh auth login` using your GitHub account. All API calls made by the GitHub CLI use YOUR credentials, so GitHub records you as the author.

### Q: Can I use a different GitHub account for ADW?

**A:** Yes! Set the `GITHUB_PAT` environment variable with a personal access token from a different account:
```bash
export GITHUB_PAT="ghp_from_different_account"
```

### Q: Is this secure?

**A:** Yes. Your OAuth token:
- Is stored locally on your machine only
- Never transmitted to any service except GitHub
- Can be revoked anytime from GitHub settings
- Has configurable scopes/permissions
- Expires based on your settings

### Q: What if I don't have `gh` installed?

**A:** ADW requires GitHub CLI. Install it:
```bash
# Windows (winget)
winget install GitHub.cli

# Mac (homebrew)
brew install gh

# Linux (apt)
sudo apt install gh
```

### Q: Can I see what commands are being executed?

**A:** Yes! ADW saves all prompts and outputs:
```bash
# View what commands were run
cat agents/<adw_id>/*/prompts/*.txt

# View full execution logs
cat agents/<adw_id>/adw_plan_build/execution.log
```

### Q: Does this work with GitHub Enterprise?

**A:** Yes! GitHub CLI supports GitHub Enterprise. Authenticate with:
```bash
gh auth login --hostname github.enterprise.com
```

---

## Summary

**How terminal commands save to GitHub:**

1. ✅ You authenticate once with `gh auth login`
2. ✅ OAuth token stored locally on your machine
3. ✅ ADW runs Python scripts that call GitHub CLI
4. ✅ GitHub CLI uses your token to make API calls
5. ✅ GitHub verifies token and identifies you
6. ✅ Comments/PRs are created under your account
7. ✅ Changes appear instantly on GitHub.com

**Key insight:** ADW doesn't have its own GitHub credentials. It uses YOURS (via `gh auth login`). Every action taken by ADW is recorded as done by YOU because it's using YOUR authentication token.

**Analogy:** It's like giving someone your house key (OAuth token) so they can unlock the door (GitHub API) on your behalf. Everything they do inside the house is recorded as being done by the keyholder (you).

---

## Related Documentation

- [GitHub CLI Authentication](https://cli.github.com/manual/gh_auth_login)
- [GitHub REST API - Issues](https://docs.github.com/en/rest/issues)
- [OAuth Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [ADW System Overview](../session-summary-adw-explanation.md)

---

*Last Updated: 2025-11-07*
*Repository: srirama7/tac-4*
