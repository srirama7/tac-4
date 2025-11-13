# TAC-5 Project Specification

## Project Overview

**TAC-5** is a sophisticated AI-powered Software Development Life Cycle (SDLC) automation system that leverages Claude Code CLI to automate the complete development workflow. The system, referred to as **AI Developer Workflow (ADW)**, automatically processes GitHub issues from planning through implementation, testing, and pull request creation.

### Key Capabilities
- 🤖 Automated issue classification (bug/feature/chore)
- 📋 Intelligent implementation plan generation
- 💻 Autonomous code implementation
- ✅ Comprehensive testing with automatic failure resolution
- 🔄 Git operations and pull request management
- 📊 GitHub integration with status updates
- 🎯 Multiple trigger mechanisms (manual, cron, webhook)

---

## Command Files Documentation

### Location
`.claude/commands/` - Contains 22 command files for various development tasks

### Main Commands (18 files)

#### 1. commit.md
Generates standardized git commit messages.
- **Format**: `<agent_name>: <issue_class>: <commit message>`
- **Usage**: Ensures consistent commit message conventions

#### 2. implement.md
Implements a given plan step-by-step.
- **Purpose**: Executes implementation tasks from planning phase
- **Features**: Systematic execution of planned items

#### 3. start.md
Starts the development server.
- **Command**: `scripts/start.sh`
- **Timeout**: 300 seconds
- **Purpose**: Launch application for testing

#### 4. tools.md
Lists all built-in non-MCP development tools.
- **Purpose**: Development tool reference

#### 5. bug.md
Creates detailed bug fix plans.
- **Features**:
  - Root cause analysis
  - Step-by-step resolution strategy
  - Related component identification

#### 6. classify_adw.md
Extracts ADW workflow commands and IDs from text.
- **Output**: JSON response with:
  - Workflow commands
  - ADW IDs
  - Command parameters

#### 7. chore.md
Creates plans for maintenance and documentation tasks.
- **Use Cases**:
  - Dependency updates
  - Documentation improvements
  - Code cleanup
  - Refactoring

#### 8. classify_issue.md
Classifies GitHub issues into categories.
- **Categories**: `/chore`, `/bug`, `/feature`
- **Purpose**: Automatic issue type detection

#### 9. feature.md
Creates comprehensive feature implementation plans.
- **Includes**:
  - Feature requirements
  - Implementation steps
  - Testing strategy
  - Integration points

#### 10. find_plan_file.md
Locates plan files from planning phase.
- **Purpose**: Retrieves generated plan documents

#### 11. generate_branch_name.md
Generates standardized git branch names.
- **Format**: `{type}-issue-{number}-adw-{adw_id}-{slug}`
- **Example**: `feat-123-a1b2c3d4-add-user-authentication`

#### 12. prime.md
Initializes project context.
- **Actions**:
  - Executes `git ls-files`
  - Reads README files
  - Establishes project understanding

#### 13. install.md
Installs project dependencies.
- **Purpose**: Setup and initialization

#### 14. pull_request.md
Creates GitHub pull requests.
- **Features**: Automated PR creation with proper formatting

#### 15. resolve_failed_test.md
Fixes specific failing unit tests.
- **Strategy**: Targeted test failure resolution

#### 16. resolve_failed_e2e_test.md
Fixes specific failing E2E tests.
- **Strategy**: Browser automation test debugging

#### 17. test_e2e.md
Executes E2E tests.
- **Framework**: Playwright browser automation
- **Features**: Screenshot capture, validation

#### 18. test.md
Runs comprehensive validation test suite.
- **Scope**:
  - Frontend tests
  - Backend tests
  - Integration tests

### E2E Test Commands (4 files)

Located in `.claude/commands/e2e/`

#### 1. test_basic_query.md
Tests fundamental query functionality.

#### 2. test_sql_injection.md
Tests SQL injection protection mechanisms.

#### 3. test_complex_query.md
Tests complex queries with filtering and joins.

#### 4. test_research_assistant.md
Tests Research Assistant feature (12-step comprehensive test).

---

## ADWS Folder Structure

### Location
`adws/` - Core AI Developer Workflow System

### Directory Organization

```
adws/
├── README.md                      # Comprehensive documentation
├── __init__.py                    # Package initialization
│
├── Core Workflow Scripts:
├── adw_plan.py                    # Planning phase
├── adw_build.py                   # Implementation phase
├── adw_test.py                    # Testing phase
├── adw_plan_build.py              # Combined: plan + build
├── adw_plan_build_test.py         # Full pipeline: plan + build + test
│
├── adw_modules/                   # Core modules
│   ├── __init__.py
│   ├── agent.py                   # Claude Code CLI integration
│   ├── data_types.py              # Pydantic models
│   ├── github.py                  # GitHub API operations
│   ├── git_ops.py                 # Git operations
│   ├── state.py                   # State management
│   ├── utils.py                   # Utility functions
│   └── workflow_ops.py            # Core business logic
│
├── adw_tests/                     # Test modules
│   ├── __init__.py
│   ├── health_check.py            # System health checks
│   ├── sandbox_poc.py             # Proof of concept tests
│   ├── test_adw_test_e2e.py       # E2E workflow tests
│   └── test_agents.py             # Agent integration tests
│
└── adw_triggers/                  # Automation triggers
    ├── __init__.py
    ├── trigger_cron.py            # Cron-based monitoring
    └── trigger_webhook.py         # GitHub webhook server
```

---

## Python Projects & Modules

### Core Workflow Scripts

All scripts use Astral UV inline script format with `#!/usr/bin/env -S uv run` shebang and inline dependency declarations.

#### 1. adw_plan.py - Planning Phase
**Purpose**: Analyzes issues and creates implementation plans.

**Workflow**:
1. Classifies issue type (bug/feature/chore)
2. Generates standardized branch name
3. Creates and checks out git branch
4. Generates detailed implementation plan
5. Commits plan to branch
6. Posts status update to GitHub issue

**Output**: Plan markdown file in agent directory

#### 2. adw_build.py - Implementation Phase
**Purpose**: Implements solutions based on generated plans.

**Workflow**:
1. Reads plan file from previous phase
2. Executes implementation using `/implement` command
3. Creates implementation commit
4. Posts status update to GitHub issue

**Output**: Implemented code changes

#### 3. adw_test.py - Testing Phase
**Purpose**: Runs comprehensive test suite with automatic failure resolution.

**Workflow**:
1. Runs unit tests (Python syntax, backend linting, pytest, TypeScript, frontend build)
2. If failures occur: executes `/resolve_failed_test` (max 4 attempts)
3. Runs E2E tests (Playwright browser automation)
4. If failures occur: executes `/resolve_failed_e2e_test` (max 2 attempts)
5. Creates test commit
6. Posts detailed test results to GitHub issue

**Features**:
- Automatic retry logic
- Detailed failure reporting
- Test result persistence

#### 4. adw_plan_build.py - Combined Workflow
**Purpose**: Executes planning and implementation in sequence.

**Workflow**:
1. Runs planning phase
2. Runs implementation phase
3. Manages state between phases

**Use Case**: Quick iteration without testing

#### 5. adw_plan_build_test.py - Full Pipeline
**Purpose**: Complete SDLC automation from issue to PR.

**Workflow**:
1. Planning phase
2. Implementation phase
3. Testing phase
4. Git push and PR creation

**Features**:
- Complete automation
- Comprehensive state management
- Full GitHub integration

**Use Case**: Production workflow for issue resolution

### Trigger Systems

#### 6. trigger_cron.py - Polling Automation
**Purpose**: Monitors GitHub for new issues or "adw" comments.

**Features**:
- Polls every 20 seconds
- Processes new open issues
- Responds to "adw" comment triggers
- Maintains processed issue tracking

**Configuration**:
- Interval: 20 seconds
- Persistent tracking of processed items

#### 7. trigger_webhook.py - Event-Driven Automation
**Purpose**: FastAPI webhook server for instant GitHub event processing.

**Features**:
- Real-time issue processing
- GitHub webhook integration
- POST endpoint: `/webhook`
- Health check endpoint: `/health`

**Configuration**:
- Host: 0.0.0.0
- Port: 8000
- ASGI server: Uvicorn

---

## Core Modules (adw_modules/)

### 1. data_types.py - Type Definitions

**Pydantic Models**:

#### GitHub Models
- `GitHubIssue` - Issue data structure
- `GitHubUser` - User information
- `GitHubComment` - Comment data
- `GitHubLabel` - Label information

#### Agent Models
- `AgentPromptRequest` - Request to Claude Code
- `AgentPromptResponse` - Response from Claude Code
- `AgentTemplateRequest` - Slash command execution request

#### Test Models
- `TestResult` - Unit test results
- `E2ETestResult` - E2E test results (includes screenshot paths)

#### State Model
- `ADWStateData` - Persistent workflow state
  - Fields: `adw_id`, `issue_number`, `branch_name`, `plan_file`, `issue_class`, `pr_number`, `test_results`, `metadata`

#### Type Definitions
- `IssueClassSlashCommand` - Literal["bug", "feature", "chore"]
- `ADWWorkflow` - Literal["plan", "build", "test", "plan_build", "plan_build_test"]
- `SlashCommand` - All available slash commands

**Purpose**: Type safety and data validation throughout the system

### 2. agent.py - Claude Code Integration

**Key Functions**:

#### `prompt_claude_code(prompt, agent_name, adw_id, cwd)`
Executes Claude Code CLI with given prompt.
- **Parameters**:
  - `prompt`: Instruction text
  - `agent_name`: Identifier for logging
  - `adw_id`: Workflow tracking ID
  - `cwd`: Working directory
- **Returns**: Exit code, stdout, stderr
- **Features**: UTF-8 encoding, JSONL output, comprehensive logging

#### `execute_template(slash_command, arguments, agent_name, adw_id, cwd)`
Executes slash commands with arguments.
- **Example**: `/classify_issue "Bug in login"`
- **Features**: Template variable substitution

#### `parse_jsonl_output(output)`
Parses JSONL output from Claude Code.
- **Returns**: List of JSON objects
- **Handles**: Multi-line JSONL responses

#### `save_prompt(prompt, agent_name, adw_id, cwd)`
Saves prompts for debugging.
- **Location**: `agents/{adw_id}/{agent_name}/prompts/`

**Windows Compatibility**: Handles UTF-8 encoding properly on Windows systems

### 3. github.py - GitHub Operations

**Key Functions**:

#### `fetch_issue(issue_number, repo_url)`
Fetches complete issue details using GitHub CLI.
- **Returns**: GitHubIssue object
- **Includes**: Title, body, labels, comments, state

#### `make_issue_comment(issue_number, comment_body, repo_url)`
Posts comments to GitHub issues.
- **Uses**: `gh issue comment`
- **Purpose**: Status updates, test results

#### `fetch_open_issues(repo_url)`
Lists all open issues in repository.
- **Returns**: List of GitHubIssue objects
- **Filter**: Open issues only

#### `fetch_issue_comments(issue_number, repo_url)`
Retrieves all comments for an issue.
- **Returns**: List of GitHubComment objects

#### `get_repo_url()`
Extracts repository URL from git remote.
- **Source**: `git config --get remote.origin.url`

#### `extract_repo_path(repo_url)`
Parses owner/repo from GitHub URL.
- **Example**: `https://github.com/owner/repo` → `owner/repo`

**Dependencies**: GitHub CLI (`gh`) must be authenticated

### 4. state.py - State Management

**ADWState Class**:

#### Core Functionality
- **Persistence**: File-based storage (`adw_state.json`)
- **Composability**: Chainable via stdin/stdout
- **Thread-safe**: Atomic file operations

#### Key Methods

##### `__init__(adw_id, cwd, issue_number)`
Initializes state manager.
- **Creates**: Agent directory structure
- **Loads**: Existing state or creates new

##### `save()`
Persists state to JSON file.
- **Location**: `agents/{adw_id}/adw_state.json`
- **Format**: Pretty-printed JSON

##### `update(**kwargs)`
Updates state fields.
- **Features**: Partial updates, automatic save

##### `read_from_stdin()`
Reads state from stdin pipe.
- **Returns**: Dictionary of state data
- **Use Case**: Script chaining

##### `write_to_stdout()`
Writes state to stdout.
- **Format**: JSON
- **Use Case**: Piping to next script

#### State Fields
- `adw_id`: Unique workflow identifier (8-char UUID)
- `issue_number`: GitHub issue number
- `branch_name`: Git branch name
- `plan_file`: Path to generated plan
- `issue_class`: bug/feature/chore
- `pr_number`: Pull request number
- `test_results`: Test execution results
- `metadata`: Additional workflow data

**Design**: Enables resume/retry capabilities and script composability

### 5. git_ops.py - Git Operations

**Key Functions**:

#### `create_branch(branch_name, cwd)`
Creates and checks out new branch.
- **Commands**: `git checkout -b {branch_name}`
- **Returns**: Success boolean

#### `commit_changes(commit_message, cwd)`
Stages and commits changes.
- **Commands**:
  1. `git add .`
  2. `git commit -m "{message}"`
- **Returns**: Success boolean

#### `push_branch(branch_name, cwd)`
Pushes branch to remote.
- **Command**: `git push -u origin {branch_name}`
- **Returns**: Success boolean

#### `check_pr_exists(branch_name, cwd)`
Checks if PR exists for branch.
- **Command**: `gh pr list --head {branch_name}`
- **Returns**: Boolean

#### `finalize_git_operations(branch_name, cwd)`
Standard workflow: push and create PR.
- **Actions**:
  1. Push branch to remote
  2. Check for existing PR
  3. Create PR if none exists
- **Returns**: PR number or None

**Error Handling**: Comprehensive subprocess error management

### 6. workflow_ops.py - Business Logic

**Key Functions**:

#### `classify_issue(issue, agent_name, adw_id, cwd)`
Classifies issue type.
- **Uses**: `/classify_issue` command
- **Returns**: "bug", "feature", or "chore"
- **Method**: AI-powered classification

#### `build_plan(issue, issue_class, agent_name, adw_id, cwd)`
Generates implementation plan.
- **Uses**: `/{issue_class}` command (e.g., `/bug`, `/feature`)
- **Returns**: Path to plan markdown file
- **Content**: Detailed step-by-step implementation plan

#### `implement_plan(plan_file, agent_name, adw_id, cwd)`
Executes implementation.
- **Uses**: `/implement` command
- **Input**: Plan file path
- **Output**: Implemented code changes

#### `generate_branch_name(issue, issue_class, adw_id, agent_name, cwd)`
Creates standardized branch name.
- **Format**: `{type}-issue-{number}-adw-{adw_id}-{slug}`
- **Uses**: `/generate_branch_name` command
- **Example**: `feat-issue-123-adw-a1b2c3d4-user-authentication`

#### `create_commit(issue_class, agent_name, adw_id, cwd, description)`
Generates commit message.
- **Format**: `{agent_name}: {issue_class}: {description}`
- **Uses**: `/commit` command
- **Example**: `sdlc_planner: feat: add user authentication`

#### `create_pull_request(agent_name, adw_id, cwd)`
Creates GitHub pull request.
- **Uses**: `/pull_request` command
- **Returns**: PR number
- **Features**: Auto-generated PR description

#### `ensure_adw_id(adw_id, cwd)`
Manages ADW ID lifecycle.
- **Action**: Creates new ID if not provided
- **Returns**: Valid ADW ID
- **Purpose**: Workflow tracking

**Design Pattern**: High-level orchestration functions wrapping agent operations

### 7. utils.py - Utility Functions

**Key Functions**:

#### `make_adw_id()`
Generates unique workflow identifier.
- **Format**: 8-character lowercase hexadecimal
- **Source**: UUID4
- **Example**: `a1b2c3d4`

#### `setup_logger(name, log_file, level=logging.INFO)`
Configures logging.
- **Outputs**:
  - Console (INFO level)
  - File (detailed logging)
- **Format**: Timestamp, level, message

#### `parse_json(text)`
Extracts JSON from markdown code blocks.
- **Handles**: Markdown-wrapped JSON responses
- **Returns**: Parsed JSON object
- **Fallback**: Direct JSON parsing if no code block

**Purpose**: Common utilities for all modules

---

## Architecture & Design

### Design Principles

#### 1. Modularity
- **Scripts**: Single-responsibility workflow scripts
- **Modules**: Reusable components
- **Composability**: Scripts can chain via pipes

#### 2. Stateful Execution
- **Persistence**: File-based state storage
- **Resume**: Can resume from any phase
- **Retry**: Failed steps can be retried

#### 3. Observability
- **Logging**: Comprehensive file and console logging
- **GitHub Updates**: Status posted to issues
- **Output Preservation**: JSONL outputs saved

#### 4. Type Safety
- **Pydantic**: Runtime type validation
- **Type Hints**: Full type annotations
- **Data Validation**: Automatic input validation

#### 5. Resilience
- **Retry Logic**: Automatic test failure resolution
- **Error Handling**: Graceful failure management
- **Idempotency**: Safe to re-run operations

#### 6. Traceability
- **ADW IDs**: Unique workflow identifiers
- **Branch Names**: Include ADW ID for tracking
- **Commit Messages**: Standardized format with agent name

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
│  (Issues, Comments, Pull Requests, Webhooks)                │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ├─────────────────┬──────────────────┐
                   │                 │                  │
                   ▼                 ▼                  ▼
         ┌─────────────┐   ┌──────────────┐   ┌────────────┐
         │   Manual    │   │    Cron      │   │  Webhook   │
         │  Execution  │   │   Trigger    │   │   Server   │
         │             │   │ (20s polls)  │   │  (FastAPI) │
         └──────┬──────┘   └──────┬───────┘   └──────┬─────┘
                │                 │                   │
                └─────────────────┴───────────────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │   Workflow Orchestration │
                    │  (adw_plan_build_test)   │
                    └─────────────┬────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
        ┌───────────┐     ┌──────────┐     ┌──────────┐
        │ Planning  │     │  Build   │     │   Test   │
        │  Phase    │────▶│  Phase   │────▶│  Phase   │
        └─────┬─────┘     └────┬─────┘     └────┬─────┘
              │                │                 │
              │                │                 │
              ▼                ▼                 ▼
        ┌──────────────────────────────────────────┐
        │          State Management                │
        │      (agents/{adw_id}/adw_state.json)    │
        └──────────────────┬───────────────────────┘
                           │
                           ▼
                ┌────────────────────┐
                │   Claude Code CLI  │
                │  (AI Agent Engine) │
                └──────────┬─────────┘
                           │
                ┌──────────┼──────────┐
                │          │          │
                ▼          ▼          ▼
         ┌─────────┐ ┌────────┐ ┌────────┐
         │ GitHub  │ │  Git   │ │  Test  │
         │   API   │ │  Ops   │ │ Runner │
         └─────────┘ └────────┘ └────────┘
```

### Workflow Phases

#### Phase 1: Planning
**Trigger**: New issue or "adw" comment

**Steps**:
1. Fetch issue from GitHub
2. Classify issue type (bug/feature/chore)
3. Generate branch name with ADW ID
4. Create and checkout git branch
5. Generate detailed implementation plan
6. Save plan to markdown file
7. Commit plan to branch
8. Post status to GitHub issue

**Output**: Implementation plan file

#### Phase 2: Building
**Trigger**: After planning or manual execution

**Steps**:
1. Load plan file from state
2. Execute `/implement` command with plan
3. Claude Code implements solution
4. Create implementation commit
5. Post status to GitHub issue

**Output**: Implemented code changes

#### Phase 3: Testing
**Trigger**: After building or manual execution

**Steps**:
1. Run unit test suite:
   - Python syntax check
   - Backend linting (ruff)
   - pytest execution
   - TypeScript type check
   - Frontend build validation
2. If failures: execute `/resolve_failed_test` (max 4 attempts)
3. Run E2E test suite:
   - Playwright browser tests
   - Screenshot validation
4. If failures: execute `/resolve_failed_e2e_test` (max 2 attempts)
5. Create test commit
6. Push branch to remote
7. Create pull request
8. Post detailed results to GitHub issue

**Output**: Test results, PR creation

### State Flow Diagram

```
Issue Created/Comment "adw"
        │
        ▼
    ADW ID Generated
        │
        ▼
    State Created
        │
        ├──▶ issue_number
        ├──▶ adw_id
        ├──▶ branch_name ────▶ Generated in planning
        ├──▶ issue_class ────▶ Classified in planning
        ├──▶ plan_file ──────▶ Created in planning
        ├──▶ pr_number ──────▶ Set in testing
        └──▶ test_results ───▶ Updated during testing
                │
                ▼
        State Persisted to JSON
                │
        ┌───────┴───────┐
        │               │
    Save to File    Output to stdout
        │               │
        └───────┬───────┘
                │
    Next Phase or Resume
```

---

## Dependencies & Setup

### External Tools Required

#### 1. Claude Code CLI
- **Purpose**: AI agent execution engine
- **Installation**: Download from Anthropic
- **Environment Variable**: `CLAUDE_CODE_PATH` (optional, defaults to "claude")

#### 2. GitHub CLI (gh)
- **Purpose**: GitHub API operations
- **Installation**: `brew install gh` or download from GitHub
- **Authentication**: Run `gh auth login`

#### 3. Git
- **Purpose**: Version control operations
- **Installation**: Standard git installation
- **Configuration**: Repository must have remote origin

#### 4. UV (Astral UV)
- **Purpose**: Python dependency manager for inline scripts
- **Installation**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Features**: Fast, zero-config Python package management

### Python Dependencies

All dependencies are specified inline in scripts using UV metadata:

```python
# /// script
# dependencies = [
#     "pydantic",
#     "python-dotenv",
# ]
# ///
```

#### Core Dependencies
- **pydantic** - Data validation and models
- **python-dotenv** - Environment variable management
- **schedule** - Cron trigger scheduling (trigger_cron.py)
- **fastapi** - Webhook server framework (trigger_webhook.py)
- **uvicorn** - ASGI server (trigger_webhook.py)

### Environment Variables

#### Required
- `ANTHROPIC_API_KEY` - API key for Claude Code CLI
  - **Source**: Anthropic Console
  - **Usage**: AI agent execution

#### Optional
- `CLAUDE_CODE_PATH` - Path to Claude CLI executable
  - **Default**: `"claude"`
  - **Usage**: Custom installation location

- `GITHUB_PAT` - GitHub Personal Access Token
  - **Usage**: Only if using different account than `gh auth`
  - **Note**: `gh` CLI auth is preferred

- `GITHUB_REPO_URL` - Repository URL override
  - **Default**: Auto-detected from `git remote`
  - **Format**: `https://github.com/owner/repo`

### Setup Instructions

#### 1. Install External Tools
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install GitHub CLI
brew install gh  # macOS
# or download from https://cli.github.com/

# Authenticate with GitHub
gh auth login

# Install Claude Code CLI
# Download from Anthropic website
```

#### 2. Configure Environment
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

#### 3. Verify Setup
```bash
# Test UV
uv --version

# Test GitHub CLI
gh auth status

# Test Claude Code
claude --version

# Test Git
git remote -v
```

#### 4. Run Health Check
```bash
cd adws
uv run adw_tests/health_check.py
```

---

## Test Infrastructure

### Unit Test Suite

**Execution**: via `/test` command in test.md

#### Test Components

1. **Python Syntax Check**
   - **Command**: `python -m py_compile`
   - **Scope**: All `.py` files
   - **Purpose**: Syntax validation

2. **Backend Linting**
   - **Tool**: Ruff
   - **Command**: `ruff check`
   - **Scope**: Python codebase
   - **Purpose**: Code quality and style

3. **Backend Tests**
   - **Framework**: pytest
   - **Command**: `pytest`
   - **Scope**: All test files
   - **Purpose**: Unit and integration tests

4. **TypeScript Type Check**
   - **Command**: `tsc --noEmit`
   - **Scope**: TypeScript codebase
   - **Purpose**: Type safety validation

5. **Frontend Build**
   - **Command**: `npm run build`
   - **Scope**: Frontend application
   - **Purpose**: Build validation

### E2E Test Suite

**Framework**: Playwright browser automation

**Execution**: via `/test_e2e` command

#### Test Cases

1. **test_basic_query.md**
   - **Purpose**: Basic query functionality
   - **Validation**: Query execution and results

2. **test_sql_injection.md**
   - **Purpose**: SQL injection protection
   - **Validation**: Security measures

3. **test_complex_query.md**
   - **Purpose**: Complex queries with filtering
   - **Validation**: Advanced query features

4. **test_research_assistant.md**
   - **Purpose**: Research Assistant feature
   - **Steps**: 12-step comprehensive test
   - **Validation**: Full feature workflow

#### E2E Test Features
- **Screenshots**: Captured for validation
- **Browser Control**: Headless browser automation
- **Result Persistence**: Test paths stored for re-execution

### Test Resolution System

#### Unit Test Resolution
**Command**: `/resolve_failed_test`

**Process**:
1. Parse test failure output
2. Identify failing test
3. Analyze failure reason
4. Generate fix
5. Re-run test
6. Repeat if needed (max 4 attempts)

#### E2E Test Resolution
**Command**: `/resolve_failed_e2e_test`

**Process**:
1. Parse E2E failure output
2. Analyze screenshots
3. Identify failure point
4. Generate fix
5. Re-run test
6. Repeat if needed (max 2 attempts)

### Test Result Tracking

**Data Structure**:
```python
TestResult:
  - test_name: str
  - passed: bool
  - error_message: Optional[str]
  - attempt: int

E2ETestResult:
  - test_path: str
  - passed: bool
  - error_message: Optional[str]
  - screenshot_paths: List[str]
  - attempt: int
```

**Storage**: Persisted in ADW state JSON

**Reporting**: Posted to GitHub issue with detailed results

---

## Output & State Management

### Directory Structure

```
agents/
└── {adw_id}/                          # e.g., a1b2c3d4
    ├── adw_state.json                 # Persistent workflow state
    │
    ├── sdlc_planner/                  # Planning phase outputs
    │   ├── raw_output.jsonl           # Claude Code JSONL output
    │   ├── raw_output.json            # Converted JSON output
    │   ├── execution.log              # Detailed execution logs
    │   └── prompts/                   # Saved prompts (if enabled)
    │       └── prompt_timestamp.txt
    │
    ├── sdlc_implementor/              # Implementation phase outputs
    │   ├── raw_output.jsonl
    │   ├── raw_output.json
    │   ├── execution.log
    │   └── prompts/
    │
    └── test_runner/                   # Testing phase outputs
        ├── raw_output.jsonl
        ├── raw_output.json
        ├── execution.log
        └── prompts/
```

### State File Format

**File**: `agents/{adw_id}/adw_state.json`

```json
{
  "adw_id": "a1b2c3d4",
  "issue_number": 123,
  "branch_name": "feat-issue-123-adw-a1b2c3d4-user-auth",
  "plan_file": "agents/a1b2c3d4/sdlc_planner/plan.md",
  "issue_class": "feature",
  "pr_number": 456,
  "test_results": {
    "unit_tests": [
      {
        "test_name": "test_authentication",
        "passed": true,
        "error_message": null,
        "attempt": 1
      }
    ],
    "e2e_tests": [
      {
        "test_path": "e2e/test_login.spec.ts",
        "passed": true,
        "error_message": null,
        "screenshot_paths": ["screenshot1.png"],
        "attempt": 1
      }
    ]
  },
  "metadata": {
    "created_at": "2024-01-15T10:30:00Z",
    "last_updated": "2024-01-15T10:45:00Z"
  }
}
```

### Logging

#### Console Logging
- **Level**: INFO
- **Format**: `timestamp - level - message`
- **Purpose**: Real-time progress monitoring

#### File Logging
- **Level**: DEBUG (detailed)
- **Location**: `agents/{adw_id}/{agent_name}/execution.log`
- **Format**: `timestamp - level - message`
- **Purpose**: Debugging and audit trail

### State Composability

#### Pipe-based Chaining
```bash
# Example: Chain workflows
uv run adw_plan.py --issue 123 | uv run adw_build.py | uv run adw_test.py
```

**Mechanism**:
- Script reads state from stdin via `ADWState.read_from_stdin()`
- Script writes state to stdout via `ADWState.write_to_stdout()`
- JSON format enables cross-script communication

#### Independent Execution
```bash
# Run phases independently using file-based state
uv run adw_plan.py --issue 123
uv run adw_build.py --adw-id a1b2c3d4
uv run adw_test.py --adw-id a1b2c3d4
```

**Mechanism**:
- State persisted to JSON file after each phase
- Later phases load state from file using ADW ID

---

## Automation Options

### 1. Manual Execution

**Use Case**: Direct control, specific issues

#### Single Phase Execution
```bash
# Planning only
uv run adws/adw_plan.py --issue 123

# Implementation only (requires existing plan)
uv run adws/adw_build.py --adw-id a1b2c3d4

# Testing only (requires implementation)
uv run adws/adw_test.py --adw-id a1b2c3d4
```

#### Combined Execution
```bash
# Plan + Build
uv run adws/adw_plan_build.py --issue 123

# Plan + Build + Test (Full pipeline)
uv run adws/adw_plan_build_test.py --issue 123
```

#### Piped Execution
```bash
# Chain phases via pipes
uv run adws/adw_plan.py --issue 123 | \
uv run adws/adw_build.py | \
uv run adws/adw_test.py
```

**Advantages**:
- Full control over execution
- Easy debugging
- Selective phase execution

### 2. Cron-Based Automation

**Script**: `adws/adw_triggers/trigger_cron.py`

**Behavior**:
- Polls GitHub every 20 seconds
- Processes new open issues automatically
- Responds to "adw" comment triggers
- Maintains processed issue tracking

#### Features
- **New Issue Detection**: Automatically picks up new issues
- **Comment Triggers**: Responds to "adw" in comments
- **Duplicate Prevention**: Tracks processed issues
- **Continuous Monitoring**: Runs indefinitely

#### Usage
```bash
# Start cron monitor
uv run adws/adw_triggers/trigger_cron.py

# Runs in foreground, Ctrl+C to stop
```

#### Configuration
```python
# Polling interval: 20 seconds
schedule.every(20).seconds.do(check_for_new_issues)
```

**Advantages**:
- Simple setup
- No external dependencies
- Reliable polling

**Disadvantages**:
- 20-second delay
- Continuous polling overhead

### 3. Webhook-Based Automation

**Script**: `adws/adw_triggers/trigger_webhook.py`

**Behavior**:
- FastAPI server listening for GitHub webhooks
- Instant processing on issue creation
- Event-driven architecture

#### Endpoints

##### POST /webhook
- **Purpose**: Receives GitHub webhook events
- **Events**: `issues` (opened action)
- **Response**: HTTP 200 on success

##### GET /health
- **Purpose**: Health check endpoint
- **Response**: `{"status": "healthy"}`

#### Setup

1. **Start Webhook Server**
```bash
uv run adws/adw_triggers/trigger_webhook.py
# Server runs on http://0.0.0.0:8000
```

2. **Configure GitHub Webhook**
- Go to: Repository Settings → Webhooks → Add webhook
- **Payload URL**: `http://your-server:8000/webhook`
- **Content type**: `application/json`
- **Events**: Select "Issues"
- **Active**: ✓

3. **Expose Server** (if local)
```bash
# Use ngrok or similar for local development
ngrok http 8000
# Use ngrok URL as webhook payload URL
```

#### Server Configuration
```python
# Host: 0.0.0.0 (all interfaces)
# Port: 8000
# ASGI Server: Uvicorn
# Reload: Enabled (development)
```

**Advantages**:
- Instant processing
- Event-driven (no polling)
- Scalable

**Disadvantages**:
- Requires public endpoint
- More complex setup
- Needs webhook configuration

---

## Usage Examples

### Example 1: Manual Full Pipeline

```bash
# Process issue #123 with complete workflow
uv run adws/adw_plan_build_test.py --issue 123
```

**What happens**:
1. Fetches issue #123
2. Classifies as bug/feature/chore
3. Generates branch: `feat-issue-123-adw-a1b2c3d4-description`
4. Creates implementation plan
5. Implements solution
6. Runs unit tests (with retry)
7. Runs E2E tests (with retry)
8. Pushes to remote
9. Creates pull request
10. Posts updates to issue

### Example 2: Planning Phase Only

```bash
# Just create the plan
uv run adws/adw_plan.py --issue 123

# Review the plan (output shows path)
cat agents/a1b2c3d4/sdlc_planner/plan.md

# Continue with implementation if satisfied
uv run adws/adw_build.py --adw-id a1b2c3d4
```

**Use case**: Review plan before implementation

### Example 3: Resume After Failure

```bash
# If testing failed, check logs
cat agents/a1b2c3d4/test_runner/execution.log

# Fix issues manually, then re-run tests
uv run adws/adw_test.py --adw-id a1b2c3d4
```

**Use case**: Manual intervention between phases

### Example 4: Cron Automation

```bash
# Start monitoring
uv run adws/adw_triggers/trigger_cron.py

# In another terminal, create issue on GitHub
gh issue create --title "Add feature X" --body "Description"

# Cron picks it up within 20 seconds
# Full workflow executes automatically
```

**Use case**: Continuous automated processing

### Example 5: Webhook Automation

```bash
# Terminal 1: Start webhook server
uv run adws/adw_triggers/trigger_webhook.py

# Terminal 2: Expose with ngrok (if local)
ngrok http 8000

# Configure webhook in GitHub settings with ngrok URL
# Create issue → Instant processing
```

**Use case**: Production deployment with instant response

### Example 6: Chain Phases with Pipes

```bash
# Execute phases in sequence with state passing
uv run adws/adw_plan.py --issue 123 | \
  uv run adws/adw_build.py | \
  uv run adws/adw_test.py
```

**Use case**: Custom workflow with state chaining

---

## Naming Conventions

### Branch Names
**Format**: `{type}-issue-{number}-adw-{adw_id}-{slug}`

**Examples**:
- `feat-issue-123-adw-a1b2c3d4-user-authentication`
- `bug-issue-456-adw-b5c6d7e8-fix-login-error`
- `chore-issue-789-adw-c9d0e1f2-update-dependencies`

**Components**:
- `type`: feat, bug, chore
- `number`: GitHub issue number
- `adw_id`: 8-char workflow ID
- `slug`: Kebab-case description

### Commit Messages
**Format**: `{agent_name}: {issue_type}: {description}`

**Examples**:
- `sdlc_planner: feat: add user authentication module`
- `sdlc_implementor: bug: fix login validation error`
- `test_runner: chore: update test dependencies`

**Components**:
- `agent_name`: sdlc_planner, sdlc_implementor, test_runner
- `issue_type`: feat, bug, chore
- `description`: Concise change summary

### File Naming
**Plan Files**: `agents/{adw_id}/sdlc_planner/plan.md`
**State Files**: `agents/{adw_id}/adw_state.json`
**Log Files**: `agents/{adw_id}/{agent_name}/execution.log`
**Output Files**: `agents/{adw_id}/{agent_name}/raw_output.jsonl`

---

## Advanced Features

### Test Retry Logic

**Unit Tests**: Max 4 resolution attempts
**E2E Tests**: Max 2 resolution attempts

**Process**:
1. Run test suite
2. If failure detected:
   - Parse error output
   - Execute appropriate resolve command
   - Commit fix
   - Re-run tests
   - Increment attempt counter
3. Repeat until pass or max attempts
4. Report final status

**Benefits**:
- Automatic error correction
- Reduces manual intervention
- Comprehensive failure tracking

### GitHub Integration

**Status Updates**: Posted at each phase
- Planning: "Plan created for issue #123"
- Implementation: "Implementation complete"
- Testing: "Tests passed (unit: 15/15, e2e: 4/4)"
- PR Creation: "Pull request created: #456"

**Comment Format**:
```markdown
🤖 ADW Status Update

**ADW ID**: a1b2c3d4
**Phase**: Testing
**Status**: ✅ Success

**Test Results**:
- Unit Tests: 15/15 passed
- E2E Tests: 4/4 passed

**Pull Request**: #456
```

### Resume Capability

**Scenario**: Process interrupted mid-workflow

**Solution**:
1. State persisted after each phase
2. Resume using ADW ID
3. Picks up from last completed phase

**Example**:
```bash
# Initial run interrupted after planning
uv run adws/adw_plan.py --issue 123
# ... interrupted ...

# Resume implementation
uv run adws/adw_build.py --adw-id a1b2c3d4

# Resume testing
uv run adws/adw_test.py --adw-id a1b2c3d4
```

---

## Troubleshooting

### Common Issues

#### 1. Claude Code Not Found
**Error**: `claude: command not found`

**Solution**:
```bash
# Set CLAUDE_CODE_PATH in .env
echo "CLAUDE_CODE_PATH=/path/to/claude" >> .env
```

#### 2. GitHub Auth Failed
**Error**: `gh: authentication failed`

**Solution**:
```bash
# Re-authenticate
gh auth login
gh auth status
```

#### 3. State File Corrupted
**Error**: `JSON decode error in adw_state.json`

**Solution**:
```bash
# Remove corrupted state
rm agents/{adw_id}/adw_state.json

# Restart workflow
uv run adws/adw_plan.py --issue 123
```

#### 4. Test Failures Persist
**Error**: Max retry attempts reached

**Solution**:
1. Check logs: `agents/{adw_id}/test_runner/execution.log`
2. Review test output
3. Manual intervention required
4. Re-run after fix

### Debugging

**Enable Verbose Logging**:
```python
# In script or module
logger.setLevel(logging.DEBUG)
```

**Review Execution Logs**:
```bash
# View planning logs
cat agents/{adw_id}/sdlc_planner/execution.log

# View implementation logs
cat agents/{adw_id}/sdlc_implementor/execution.log

# View test logs
cat agents/{adw_id}/test_runner/execution.log
```

**Review Claude Output**:
```bash
# View raw JSONL output
cat agents/{adw_id}/{agent_name}/raw_output.jsonl

# View converted JSON
cat agents/{adw_id}/{agent_name}/raw_output.json
```

---

## Security Considerations

### API Keys
- Store `ANTHROPIC_API_KEY` in `.env` file
- Never commit `.env` to git
- Use `python-dotenv` for loading

### GitHub Token
- Use `gh auth login` for authentication
- Prefer built-in GitHub CLI auth over PAT
- Limit token scopes if using PAT

### Webhook Security
- Validate webhook signatures (TODO: implement)
- Use HTTPS for production webhooks
- Restrict webhook IP sources if possible

### Code Execution
- Review AI-generated code before committing
- Test thoroughly before merging PRs
- Use branch protection rules

---

## Future Enhancements

### Planned Features
1. **Webhook signature validation**
2. **Multi-repository support**
3. **Custom test frameworks**
4. **Parallel test execution**
5. **Metrics and analytics dashboard**
6. **Slack/Discord notifications**
7. **Custom workflow templates**
8. **AI model selection**

### Extensibility
- **Custom agents**: Add new agent modules
- **Custom commands**: Add `.claude/commands/*.md` files
- **Custom triggers**: Implement new trigger mechanisms
- **Custom test suites**: Extend test framework

---

## Contributing

### Development Setup
1. Fork repository
2. Install dependencies
3. Create feature branch
4. Make changes
5. Run tests
6. Submit pull request

### Code Standards
- **Type hints**: All functions must have type annotations
- **Docstrings**: Document all public functions
- **Logging**: Use structured logging
- **Error handling**: Comprehensive error handling
- **Testing**: Unit tests for all modules

---

## License

[Include license information if applicable]

---

## Support

### Documentation
- **ADW README**: `adws/README.md`
- **Command Files**: `.claude/commands/*.md`

### Issues
- Report bugs via GitHub issues
- Tag with appropriate labels
- Include ADW ID and logs

### Contact
[Include contact information if applicable]

---

**Last Updated**: 2025-11-13

**Document Version**: 1.0

**Generated by**: TAC-5 ADW System Documentation Generator
