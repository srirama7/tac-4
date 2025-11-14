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

## Detailed ADW Workflow Scripts Analysis

This section provides in-depth technical documentation for the five main ADW workflow scripts, including complete workflow breakdowns, state management, error handling, and usage patterns.

### 1. adw_plan.py - Planning Phase Script

**File**: `adws/adw_plan.py` (265 lines)

**Purpose**: The planning phase is the entry point for the ADW workflow. It analyzes GitHub issues, classifies them, creates git branches, and generates comprehensive implementation plans using Claude Code CLI.

#### Command-Line Interface

```bash
# Basic usage
uv run adw_plan.py <issue-number> [adw-id]

# Examples
uv run adw_plan.py 123                    # Create new plan for issue #123
uv run adw_plan.py 123 a1b2c3d4           # Resume/use specific ADW ID
```

**Arguments**:
- `issue-number` (required): GitHub issue number to process
- `adw-id` (optional): Existing ADW ID for resuming or tracking

#### Dependencies

Inline UV script dependencies:
```python
# dependencies = ["python-dotenv", "pydantic"]
```

#### Complete Workflow Breakdown

**Step 1: Initialization (Lines 61-90)**
1. Load environment variables from `.env` file
2. Parse command-line arguments
3. Generate or use provided ADW ID via `ensure_adw_id()`
4. Load existing state or create new state
5. Initialize logger with ADW ID for tracking

**Step 2: Repository Setup (Lines 91-98)**
1. Extract repository URL from git remote: `get_repo_url()`
2. Parse owner/repo path: `extract_repo_path(github_repo_url)`
3. Exit with error if repository detection fails

**Step 3: Issue Fetching (Lines 100-106)**
1. Fetch complete issue details from GitHub: `fetch_issue(issue_number, repo_path)`
2. Log issue data in JSON format (debug level)
3. Post initial status comment to GitHub issue: "✅ Starting planning phase"
4. Post current state snapshot to issue

**Step 4: Issue Classification (Lines 113-130)**
1. Classify issue using AI: `classify_issue(issue, adw_id, logger)`
   - Returns one of: `/bug`, `/feature`, `/chore`
   - Uses Claude Code with `/classify_issue` command
2. Update state with issue classification
3. Save state to `adw_state.json`
4. Post classification result to GitHub issue

**Step 5: Branch Name Generation (Lines 132-162)**
1. Generate standardized branch name: `generate_branch_name(issue, issue_command, adw_id, logger)`
   - Format: `{type}-issue-{number}-adw-{adw_id}-{slug}`
   - Example: `feat-issue-123-adw-a1b2c3d4-user-authentication`
2. Create and checkout git branch: `create_branch(branch_name)`
3. Update state with branch name
4. Save state
5. Post branch name to GitHub issue

**Step 6: Plan Generation (Lines 164-187)**
1. Build implementation plan: `build_plan(issue, issue_command, adw_id, logger)`
   - Executes appropriate slash command: `/bug`, `/feature`, or `/chore`
   - Claude Code generates detailed implementation plan
   - Returns `AgentPromptResponse` with success status
2. Post success message to GitHub issue
3. Exit with error if plan generation fails

**Step 7: Plan File Location (Lines 189-209)**
1. Find generated plan file: `get_plan_file(plan_response.output, issue_number, adw_id, logger)`
   - Searches for plan file in agent output directory
   - Pattern: `specs/issue-{issue_number}-adw-{adw_id}-*.md`
2. Update state with plan file path
3. Save state
4. Post plan file path to GitHub issue

**Step 8: Commit Creation (Lines 211-243)**
1. Generate commit message: `create_commit(AGENT_PLANNER, issue, issue_command, adw_id, logger)`
   - Format: `sdlc_planner: {type}: {description}`
   - Uses `/commit` command
2. Commit changes: `commit_changes(commit_msg)`
   - Stages all changes: `git add .`
   - Creates commit with generated message
3. Post commit success to GitHub issue

**Step 9: Git Finalization (Lines 245-246)**
1. Push branch to remote: `finalize_git_operations(state, logger)`
2. Create pull request if none exists
3. Update state with PR number if created

**Step 10: Completion (Lines 248-260)**
1. Log completion message
2. Post completion status to GitHub issue: "✅ Planning phase completed"
3. Save final state
4. Post final state summary to issue as JSON

#### State Management

**State Created**:
- `adw_id`: Workflow identifier
- `issue_number`: GitHub issue number
- `branch_name`: Git branch name
- `issue_class`: Issue classification (/bug, /feature, /chore)
- `plan_file`: Path to generated plan markdown

**State File Location**: `agents/{adw_id}/adw_state.json`

#### Error Handling

- **Repository URL Failure**: Exits with code 1, logs error
- **Issue Classification Failure**: Exits with code 1, posts error to GitHub issue
- **Branch Creation Failure**: Exits with code 1, posts error to GitHub issue
- **Plan Generation Failure**: Exits with code 1, posts error to GitHub issue
- **Plan File Not Found**: Exits with code 1, posts error to GitHub issue
- **Commit Failure**: Exits with code 1, posts error to GitHub issue

All errors are:
1. Logged to file: `agents/{adw_id}/sdlc_planner/execution.log`
2. Posted to GitHub issue with ❌ emoji
3. Result in immediate script termination

#### GitHub Integration Points

**Comments Posted**:
1. "✅ Starting planning phase" (start)
2. State snapshot (JSON)
3. "✅ Issue classified as: {classification}" (after classification)
4. "✅ Working on branch: {branch_name}" (after branch creation)
5. "✅ Building implementation plan" (before plan generation)
6. "✅ Implementation plan created" (after plan generation)
7. "✅ Plan file created: {path}" (after file location)
8. "✅ Plan committed" (after commit)
9. "✅ Planning phase completed" (completion)
10. Final state summary (JSON)

**Comment Format**: `{adw_id}_ops: {message}` or `{adw_id}_sdlc_planner: {message}`

#### Output Artifacts

1. **Plan File**: `specs/issue-{issue_number}-adw-{adw_id}-{slug}.md`
2. **State File**: `agents/{adw_id}/adw_state.json`
3. **Execution Log**: `agents/{adw_id}/sdlc_planner/execution.log`
4. **Claude Output**: `agents/{adw_id}/sdlc_planner/raw_output.jsonl`
5. **Git Commit**: Plan committed to branch
6. **Git Branch**: Feature branch created and pushed

#### Usage Patterns

**Standalone Execution**:
```bash
# New workflow
uv run adws/adw_plan.py 123

# With specific ADW ID
uv run adws/adw_plan.py 123 a1b2c3d4
```

**As Part of Pipeline**:
```bash
# Followed by build
uv run adws/adw_plan.py 123 && uv run adws/adw_build.py 123 $(get_adw_id)
```

---

### 2. adw_build.py - Implementation Phase Script

**File**: `adws/adw_build.py` (232 lines)

**Purpose**: The implementation phase reads the plan file created during planning and uses Claude Code CLI to autonomously implement the solution. It requires an existing ADW ID from a completed planning phase.

#### Command-Line Interface

```bash
# Usage (ADW ID is REQUIRED)
uv run adw_build.py <issue-number> <adw-id>

# Example
uv run adw_build.py 123 a1b2c3d4
```

**Arguments**:
- `issue-number` (required): GitHub issue number
- `adw-id` (required): ADW ID from planning phase (NOT optional)

**Why ADW ID is Required**:
1. Plan file is stored in state identified by ADW ID
2. Multiple ADW runs for same issue could exist
3. Must know exactly which plan to implement

#### Dependencies

Inline UV script dependencies:
```python
# dependencies = ["python-dotenv", "pydantic"]
```

#### Complete Workflow Breakdown

**Step 1: Initialization & State Loading (Lines 51-94)**
1. Load environment variables
2. Parse command-line arguments
3. Validate that ADW ID is provided (exit if missing)
4. Attempt to load existing state: `ADWState.load(adw_id, logger)`
5. If state found:
   - Use issue number from state
   - Post "🔍 Found existing state" to GitHub
6. If no state found:
   - Log error: "No state found for ADW ID"
   - Print error message with instructions
   - Exit with code 1

**Step 2: Environment & Repository Setup (Lines 90-102)**
1. Setup logger with ADW ID
2. Validate environment variables (Claude Code authentication)
3. Get repository URL from git remote
4. Extract repo path for GitHub operations

**Step 3: State Validation (Lines 104-133)**
1. Validate `branch_name` exists in state
   - If missing: post error to GitHub, exit with code 1
2. Validate `plan_file` exists in state
   - If missing: post error to GitHub, exit with code 1
3. Checkout the branch from state: `git checkout {branch_name}`
   - If checkout fails: post error to GitHub, exit with code 1
4. Log branch checkout success

**Step 4: Plan File Retrieval (Lines 135-142)**
1. Get plan file path from state: `state.get("plan_file")`
2. Log plan file path
3. Post status to GitHub: "✅ Starting implementation phase"

**Step 5: Solution Implementation (Lines 144-165)**
1. Post implementation start to GitHub
2. Execute implementation: `implement_plan(plan_file, adw_id, logger)`
   - Uses `/implement` slash command
   - Passes plan file path as argument
   - Claude Code reads plan and implements solution
   - Returns `AgentPromptResponse` with success status
3. If implementation fails:
   - Log error with output
   - Post error to GitHub
   - Exit with code 1
4. If successful:
   - Log debug output
   - Post success to GitHub: "✅ Solution implemented"

**Step 6: Issue Classification (Lines 167-185)**
1. Get issue classification from state: `state.get("issue_class")`
2. If not in state:
   - Fetch issue data: `fetch_issue(issue_number, repo_path)`
   - Classify issue: `classify_issue(issue, adw_id, logger)`
   - Default to `/feature` if classification fails
   - Save classification to state
3. Classification used for commit message generation

**Step 7: Commit Creation (Lines 187-216)**
1. Fetch issue data for commit message (if not already fetched)
2. Generate commit message: `create_commit(AGENT_IMPLEMENTOR, issue, issue_command, adw_id, logger)`
   - Format: `sdlc_implementor: {type}: {description}`
   - Uses `/commit` slash command
3. Commit implementation: `commit_changes(commit_msg)`
   - Stages all changes: `git add .`
   - Creates commit
4. If commit fails:
   - Log error
   - Post error to GitHub
   - Exit with code 1
5. Post success to GitHub: "✅ Implementation committed"

**Step 8: Git Finalization (Lines 218-225)**
1. Finalize git operations: `finalize_git_operations(state, logger)`
   - Push branch to remote
   - Check for existing PR
   - Create PR if none exists
2. Post completion to GitHub: "✅ Implementation phase completed"
3. Save final state

#### State Management

**State Required**:
- `adw_id`: Workflow identifier (from previous phase)
- `issue_number`: GitHub issue number
- `branch_name`: Git branch to checkout
- `plan_file`: Path to plan markdown file

**State Updated**:
- `issue_class`: Issue classification (if not already set)
- `pr_number`: PR number (if created during finalization)

**State File**: `agents/{adw_id}/adw_state.json`

#### Error Handling

- **No ADW ID Provided**: Prints usage, exits with code 1
- **State Not Found**: Logs error, posts to GitHub, exits with code 1
- **Missing Branch Name**: Posts error to GitHub, exits with code 1
- **Missing Plan File**: Posts error to GitHub, exits with code 1
- **Branch Checkout Failed**: Posts error to GitHub, exits with code 1
- **Implementation Failed**: Posts error to GitHub, exits with code 1
- **Commit Failed**: Posts error to GitHub, exits with code 1

Error message format includes:
1. Detailed error logging to `agents/{adw_id}/sdlc_implementor/execution.log`
2. GitHub issue comments with ❌ emoji
3. Script exits immediately on error

#### GitHub Integration Points

**Comments Posted**:
1. "🔍 Found existing state" + JSON (if state loaded)
2. "✅ Starting implementation phase" (start)
3. "✅ Implementing solution" (before implementation)
4. "✅ Solution implemented" (after implementation)
5. "✅ Implementation committed" (after commit)
6. "✅ Implementation phase completed" (completion)
7. Error messages with ❌ (on failures)

**Comment Format**: `{adw_id}_ops: {message}` or `{adw_id}_sdlc_implementor: {message}`

#### Output Artifacts

1. **Implemented Code**: Changes to codebase files
2. **State File**: Updated `agents/{adw_id}/adw_state.json`
3. **Execution Log**: `agents/{adw_id}/sdlc_implementor/execution.log`
4. **Claude Output**: `agents/{adw_id}/sdlc_implementor/raw_output.jsonl`
5. **Git Commit**: Implementation committed to branch
6. **Pull Request**: Created or updated (if finalization runs)

#### Usage Patterns

**After Planning Phase**:
```bash
# Plan first
uv run adws/adw_plan.py 123
# Build with ADW ID from planning
uv run adws/adw_build.py 123 a1b2c3d4
```

**Standalone with Existing State**:
```bash
# Resume implementation for existing ADW workflow
uv run adws/adw_build.py 123 a1b2c3d4
```

#### Design Notes

**Why ADW ID is REQUIRED** (intentional design decision at lines 57-65):
- The plan file is stored in state and identified by ADW ID
- Multiple ADW runs for the same issue could exist
- Need to know exactly which plan to implement
- Plan file path: `specs/issue-{issue_number}-adw-{adw_id}-*.md`

---

### 3. adw_test.py - Testing Phase Script

**File**: `adws/adw_test.py` (1107 lines - most complex script)

**Purpose**: The testing phase runs comprehensive unit and E2E tests with automatic failure resolution. It includes intelligent retry logic, test result parsing, GitHub reporting, and can create branches if running standalone.

#### Command-Line Interface

```bash
# Usage
uv run adw_test.py <issue-number> [adw-id] [--skip-e2e]

# Examples
uv run adw_test.py 123                    # Run all tests with new ADW ID
uv run adw_test.py 123 a1b2c3d4           # Use existing ADW ID
uv run adw_test.py 123 --skip-e2e         # Skip E2E tests
uv run adw_test.py 123 a1b2c3d4 --skip-e2e # Use ADW ID and skip E2E

# Piped execution (state from stdin)
echo '{"issue_number": "123"}' | uv run adw_test.py
```

**Arguments**:
- `issue-number` (required in standalone mode): GitHub issue number
- `adw-id` (optional): Existing ADW ID, or creates new one
- `--skip-e2e` (optional flag): Skip E2E tests

#### Dependencies

Inline UV script dependencies:
```python
# dependencies = ["python-dotenv", "pydantic"]
```

#### Constants & Configuration

```python
AGENT_TESTER = "test_runner"
AGENT_E2E_TESTER = "e2e_test_runner"
MAX_TEST_RETRY_ATTEMPTS = 4           # Unit test retries
MAX_E2E_TEST_RETRY_ATTEMPTS = 2       # E2E test retries
```

#### Complete Workflow Breakdown

**Phase 1: Initialization (Lines 867-907)**

1. Load environment variables from `.env`
2. Parse command-line arguments:
   - Extract `--skip-e2e` flag if present
   - Get issue number and ADW ID
3. Validate issue number is provided
4. Ensure ADW ID exists: `ensure_adw_id(issue_number, adw_id, logger)`
   - Creates new ADW ID if not provided
   - Initializes state if new
5. Load state: `ADWState.load(adw_id, logger)`
6. Setup logger with ADW ID
7. Validate environment variables:
   - `ANTHROPIC_API_KEY` (required)
   - `CLAUDE_CODE_PATH` (required)
   - Exit if missing
8. Get repository information from git remote

**Phase 2: Branch Management (Lines 909-947)**

**Case A: Existing Branch in State**
1. Get branch name from state: `state.get("branch_name")`
2. Checkout existing branch: `git checkout {branch_name}`
3. If checkout fails:
   - Log error
   - Post error to GitHub
   - Exit with code 1
4. Log success: "Checked out existing branch"

**Case B: No Branch in State**
1. Generate test branch name: `test-issue-{issue_number}-adw-{adw_id}`
   - Simpler format than feature branches
   - No classification needed
2. Create branch: `create_branch(branch_name)`
3. If creation fails:
   - Log error
   - Post error to GitHub
   - Exit with code 1
4. Update state with branch name
5. Save state
6. Post success to GitHub: "✅ Created test branch"

**Phase 3: Unit Testing with Resolution (Lines 949-972)**

**Main Loop** (Lines 411-517 in `run_tests_with_resolution`):

```
Attempt 1 to MAX_TEST_RETRY_ATTEMPTS (4):
  1. Run tests via `/test` command
  2. Parse test results (JSON output)
  3. If all passed: STOP, success
  4. If max attempts reached: STOP, report failures
  5. If failures exist:
     a. Post failure count to GitHub
     b. For each failed test:
        - Create test_resolver agent
        - Post resolution attempt to GitHub
        - Execute `/resolve_failed_test` with test data
        - If successful: increment resolved count
        - If failed: increment unresolved count
     c. Post resolution results to GitHub
     d. If resolved > 0: continue to next attempt
     e. If resolved == 0: STOP, no point retrying
```

**Test Execution** (Lines 248-268 in `run_tests`):
1. Create `AgentTemplateRequest` with `/test` command
2. Execute template: `execute_template(request)`
3. Returns `AgentPromptResponse` with test results in JSON

**Test Result Parsing** (Lines 271-285 in `parse_test_results`):
1. Parse JSON from output using `parse_json()`
2. Convert to list of `TestResult` objects
3. Count passed and failed tests
4. Return results tuple: `(results, passed_count, failed_count)`

**Test Resolution** (Lines 338-408 in `resolve_failed_tests`):
1. Iterate through failed tests
2. For each test:
   - Create test payload (JSON)
   - Generate agent name: `test_resolver_iter{iteration}_{index}`
   - Post attempt to GitHub
   - Execute `/resolve_failed_test` slash command
   - If successful: post success, increment resolved
   - If failed: post failure, increment unresolved
3. Return resolution counts

**Final Results** (Lines 965-975):
1. Format results: `format_test_results_comment(results, passed, failed)`
2. Post to GitHub with 📊 emoji
3. Log summary

**Phase 4: E2E Testing with Resolution (Lines 977-1030)**

**Conditional Execution**:
- Skip if unit tests failed
- Skip if `--skip-e2e` flag set
- Otherwise, proceed with E2E tests

**Main Loop** (Lines 763-864 in `run_e2e_tests_with_resolution`):

```
Attempt 1 to MAX_E2E_TEST_RETRY_ATTEMPTS (2):
  1. Run all E2E tests sequentially
  2. Count passed and failed
  3. If all passed: STOP, success
  4. If max attempts reached: STOP, report failures
  5. If failures exist:
     a. Post failure count to GitHub
     b. For each failed test:
        - Create e2e_test_resolver agent
        - Post resolution attempt to GitHub
        - Execute `/resolve_failed_e2e_test` with test data
        - If successful: increment resolved count
        - If failed: increment unresolved count
     c. Post resolution results to GitHub
     d. If resolved > 0: continue to next attempt
     e. If resolved == 0: STOP, no point retrying
```

**E2E Test Execution** (Lines 520-552 in `run_e2e_tests`):
1. Find all E2E test files: `glob.glob(".claude/commands/e2e/*.md")`
2. For each test file:
   - Generate agent name: `e2e_test_runner_{attempt}_{index}`
   - Execute test: `execute_single_e2e_test()`
   - If test fails: STOP (fail fast strategy)
   - If test passes: continue
3. Return list of `E2ETestResult` objects

**Single E2E Test** (Lines 555-638 in `execute_single_e2e_test`):
1. Extract test name from filename
2. Post start to GitHub
3. Create template request for `/test_e2e` command
4. Execute test
5. Parse result JSON (includes screenshots)
6. Create `E2ETestResult` object
7. Post complete result to GitHub with status emoji
8. Return result

**E2E Resolution** (Lines 690-760 in `resolve_failed_e2e_tests`):
- Similar to unit test resolution
- Uses `/resolve_failed_e2e_test` command
- Agent name: `e2e_test_resolver_iter{iteration}_{index}`

**Final E2E Results** (Lines 1013-1029):
1. Format results: `format_e2e_test_results_comment()`
2. Post to GitHub with 📊 emoji
3. Log summary

**Phase 5: Commit & Finalization (Lines 1031-1103)**

**Commit Creation** (Lines 1031-1064):
1. Fetch issue details if not already fetched
2. Get or classify issue: `classify_issue()` if needed
3. Generate commit message: `create_commit(AGENT_TESTER, issue, issue_class, adw_id, logger)`
   - Format: `test_runner: {type}: {description}`
4. If commit fails: log error but continue (don't exit)

**Comprehensive Results Logging** (Lines 1065-1066):
1. Call `log_test_results(state, results, e2e_results, logger)`
2. Generates comprehensive test summary (Lines 177-245):
   - Counts passed/failed for unit and E2E
   - Creates markdown summary with all test details
   - Includes error messages for failures
   - Includes screenshot paths for E2E tests
   - Shows overall status
3. Posts to GitHub with `test_summary` agent name

**Git Finalization** (Lines 1068-1070):
1. Finalize git operations: `finalize_git_operations(state, logger)`
   - Push branch to remote
   - Create PR if none exists
   - Update state with PR number

**State Persistence** (Lines 1072-1077):
1. Save state: `state.save("adw_test")`
2. Output state to stdout: `state.to_stdout()` (for piping)

**Exit with Status** (Lines 1079-1102):
1. Calculate total failures: `failed_count + e2e_failed_count`
2. If failures > 0:
   - Log completion with failures
   - Post detailed failure message to GitHub
   - Exit with code 1
3. If all passed:
   - Log successful completion
   - Post success message to GitHub
   - Exit with code 0

#### State Management

**State Used**:
- `adw_id`: Workflow identifier
- `issue_number`: GitHub issue number
- `branch_name`: Git branch (created if not exists)
- `issue_class`: Issue classification (fetched if needed)

**State Updated**:
- `branch_name`: Set if created during test phase
- `issue_class`: Set if classified during test phase
- `pr_number`: Set if PR created
- Test results stored but not in core state schema

#### Test Result Models

**TestResult** (Unit Tests):
```python
{
  "test_name": str,          # Test identifier
  "passed": bool,            # Pass/fail status
  "error": Optional[str],    # Error message if failed
  "attempt": int             # Which attempt number
}
```

**E2ETestResult** (E2E Tests):
```python
{
  "test_name": str,          # Test identifier
  "status": str,             # "passed" or "failed"
  "test_path": str,          # Path to test file
  "passed": bool,            # Computed property
  "error": Optional[str],    # Error message if failed
  "screenshots": List[str],  # Screenshot file paths
  "attempt": int             # Which attempt number
}
```

#### Error Handling

**Critical Errors (Exit with code 1)**:
- Missing issue number in standalone mode
- Environment variables missing (ANTHROPIC_API_KEY, CLAUDE_CODE_PATH)
- Repository URL detection failure
- Branch checkout failure
- Branch creation failure
- Test execution failure (non-test errors)

**Non-Critical Errors (Continue execution)**:
- Commit message generation failure
- Commit creation failure (logs error, continues to report results)
- Individual test failures (retried up to max attempts)

**Error Reporting**:
1. Logged to `agents/{adw_id}/test_runner/execution.log`
2. Posted to GitHub issues with ❌ emoji
3. Included in final test results summary

#### GitHub Integration Points

**Comments Posted**:
1. "✅ Created test branch" (if branch created)
2. "✅ Starting test suite" (start)
3. "✅ Running application tests..." (before unit tests)
4. "❌ Found N failed tests. Attempting resolution..." (if failures)
5. "🔧 Attempting to resolve: {test_name}" (per test resolution)
6. "✅ Successfully resolved: {test_name}" (successful resolution)
7. "❌ Failed to resolve: {test_name}" (failed resolution)
8. "✅ Resolved N/M failed tests" (resolution summary)
9. "🔄 Re-running tests (attempt X/Y)..." (retry notification)
10. "📊 Final test results" (final unit test results)
11. "✅ Starting E2E tests..." (before E2E tests)
12. "✅ Running E2E test: {name}" (per E2E test)
13. "✅/❌ E2E test completed: {name}" (E2E test result)
14. "🔧 Found N failed E2E tests. Attempting resolution..." (E2E failures)
15. "🔧 Attempting to resolve E2E test: {name}" (E2E resolution)
16. "✅ Resolved N/M failed E2E tests" (E2E resolution summary)
17. "📊 Final E2E test results" (final E2E results)
18. "✅ Committing test results" (before commit)
19. "📊 Test Run Summary" (comprehensive results)
20. "✅/❌ Test suite completed" (final status)

**Comment Format**: `{adw_id}_{agent_name}: {message}`

#### Output Artifacts

1. **Test Results**: Comprehensive test execution data
2. **Screenshots**: E2E test screenshots in `agents/{adw_id}/e2e_test_runner_{attempt}_{idx}/`
3. **State File**: Updated `agents/{adw_id}/adw_state.json`
4. **Execution Logs**: `agents/{adw_id}/test_runner/execution.log`
5. **Claude Output**: `agents/{adw_id}/test_runner/raw_output.jsonl`
6. **Git Commit**: Test results committed to branch
7. **Pull Request**: Created or updated

#### Usage Patterns

**After Build Phase**:
```bash
uv run adws/adw_build.py 123 a1b2c3d4
uv run adws/adw_test.py 123 a1b2c3d4
```

**Standalone Testing**:
```bash
# Create new test branch and run tests
uv run adws/adw_test.py 123

# Skip E2E tests
uv run adws/adw_test.py 123 --skip-e2e
```

**Piped Execution**:
```bash
uv run adws/adw_build.py 123 a1b2c3d4 | uv run adws/adw_test.py
```

#### Advanced Features

**Retry Logic**:
- Unit tests: Up to 4 resolution attempts
- E2E tests: Up to 2 resolution attempts
- Stops early if no tests resolved in an iteration
- Automatic retry after successful resolutions

**Fail-Fast Strategy**:
- E2E tests stop on first failure
- No point running remaining E2E tests if one fails
- Speeds up feedback cycle

**Intelligent Resolution**:
- Each failed test resolved individually
- Uses AI to analyze failure and generate fix
- Commits fix automatically
- Re-runs tests to verify fix
- Tracks resolution success rate

**Comprehensive Reporting**:
- Detailed test results in JSON format
- Error messages truncated to 200 chars for readability
- Screenshot paths included for E2E tests
- Overall pass/fail summary
- Posted to GitHub for full visibility

---

### 4. adw_plan_build.py - Combined Planning & Implementation

**File**: `adws/adw_plan_build.py` (72 lines)

**Purpose**: Orchestration script that runs planning and implementation phases in sequence using subprocess execution. Provides a simplified workflow for quick iteration without testing.

#### Command-Line Interface

```bash
# Usage
uv run adw_plan_build.py <issue-number> [adw-id]

# Examples
uv run adw_plan_build.py 123                # New workflow
uv run adw_plan_build.py 123 a1b2c3d4       # With specific ADW ID
```

**Arguments**:
- `issue-number` (required): GitHub issue number
- `adw-id` (optional): Existing ADW ID or creates new one

#### Dependencies

Inline UV script dependencies:
```python
# dependencies = ["python-dotenv", "pydantic"]
```

#### Complete Workflow Breakdown

**Step 1: Initialization (Lines 28-38)**
1. Validate command-line arguments
2. Parse issue number from `sys.argv[1]`
3. Parse optional ADW ID from `sys.argv[2]` (or None)
4. Ensure ADW ID exists: `ensure_adw_id(issue_number, adw_id)`
   - Creates new ID if not provided
   - Initializes state directory structure
   - Returns valid ADW ID
5. Print ADW ID for user reference

**Step 2: Get Script Directory (Lines 40-41)**
1. Determine absolute path of current script
2. Used to construct paths to other scripts in same directory

**Step 3: Run Planning Phase (Lines 43-55)**
1. Construct command:
   ```bash
   uv run {script_dir}/adw_plan.py {issue_number} {adw_id}
   ```
2. Print command for transparency
3. Execute using `subprocess.run(plan_cmd)`
   - Runs in foreground (waits for completion)
   - stdout/stderr shown to user in real-time
   - Returns `CompletedProcess` with return code
4. Check return code:
   - If non-zero: exit with code 1 (planning failed)
   - If zero: continue to build phase

**Step 4: Run Build Phase (Lines 57-67)**
1. Construct command:
   ```bash
   uv run {script_dir}/adw_build.py {issue_number} {adw_id}
   ```
2. Print command for transparency
3. Execute using `subprocess.run(build_cmd)`
   - Runs in foreground (waits for completion)
   - stdout/stderr shown to user in real-time
4. Check return code:
   - If non-zero: exit with code 1 (build failed)
   - If zero: workflow complete, exit with code 0

#### State Management

**State Lifecycle**:
1. `ensure_adw_id()` creates or loads initial state
2. `adw_plan.py` updates state with:
   - `issue_number`
   - `branch_name`
   - `issue_class`
   - `plan_file`
3. `adw_build.py` loads state and optionally adds:
   - `pr_number` (if PR created)

**State Persistence**: File-based via `agents/{adw_id}/adw_state.json`

**State Chaining**: Uses file-based state, not pipes (subprocess doesn't pipe between phases)

#### Error Handling

**Planning Phase Failure**:
- `adw_plan.py` exits with non-zero code
- `subprocess.run()` captures exit code
- Script exits immediately with code 1
- No build phase attempted

**Build Phase Failure**:
- `adw_build.py` exits with non-zero code
- `subprocess.run()` captures exit code
- Script exits with code 1
- Planning results preserved in state

**No Rollback**: If planning succeeds but building fails, the plan remains committed in git

#### Output Artifacts

**From Planning Phase**:
1. Plan file in `specs/`
2. State file with plan metadata
3. Git branch with plan committed
4. GitHub comments with planning status

**From Build Phase**:
1. Implemented code changes
2. Updated state file
3. Git commit with implementation
4. Pull request (if created)
5. GitHub comments with build status

**Combined**:
- Complete plan + implementation workflow
- All artifacts from both phases
- Branch pushed to remote with 2 commits minimum

#### Usage Patterns

**Quick Development Iteration**:
```bash
# Plan and implement without testing
uv run adws/adw_plan_build.py 123
```

**Resume from Failed Build**:
```bash
# If build failed, fix and re-run just build
uv run adws/adw_build.py 123 a1b2c3d4
```

**Advantages Over Individual Scripts**:
1. Single command execution
2. Automatic ADW ID management
3. No need to track ADW ID between phases
4. Simplified user experience

**Disadvantages**:
1. Cannot review plan before implementation
2. No testing phase included
3. Less control over individual phases

#### Design Notes

**Subprocess vs Import**:
- Uses `subprocess.run()` instead of importing and calling functions
- Allows scripts to run in isolation with their own environments
- Each phase gets fresh environment variables
- Cleaner separation of concerns
- Matches production execution model

**State Chaining**:
- File-based state sharing (not stdin/stdout pipes)
- `ensure_adw_id()` ensures state exists before planning
- Each script loads state from file
- More robust than piping for subprocess execution

**No Testing**:
- Intentionally excludes testing phase
- Use case: rapid prototyping/development
- For full workflow with tests, use `adw_plan_build_test.py`

---

### 5. adw_plan_build_test.py - Full Pipeline Script

**File**: `adws/adw_plan_build_test.py` (86 lines)

**Purpose**: Complete SDLC automation orchestration script that runs all three phases (planning, implementation, testing) in sequence. This is the production workflow for full issue-to-PR automation.

#### Command-Line Interface

```bash
# Usage
uv run adw_plan_build_test.py <issue-number> [adw-id]

# Examples
uv run adw_plan_build_test.py 123              # Full automation
uv run adw_plan_build_test.py 123 a1b2c3d4     # With specific ADW ID
```

**Arguments**:
- `issue-number` (required): GitHub issue number
- `adw-id` (optional): Existing ADW ID or creates new one

#### Dependencies

Inline UV script dependencies:
```python
# dependencies = ["python-dotenv", "pydantic"]
```

#### Complete Workflow Breakdown

**Step 1: Initialization (Lines 28-39)**
1. Validate command-line arguments
2. Parse issue number from `sys.argv[1]`
3. Parse optional ADW ID from `sys.argv[2]` (or None)
4. Ensure ADW ID exists: `ensure_adw_id(issue_number, adw_id)`
   - Creates new ADW ID if not provided
   - Initializes state directory: `agents/{adw_id}/`
   - Creates initial state file: `adw_state.json`
   - Returns valid ADW ID for tracking
5. Print ADW ID for user reference: "Using ADW ID: {adw_id}"

**Step 2: Script Directory Detection (Lines 41-42)**
1. Get absolute path of current script file
2. Extract directory path
3. Used to construct paths to sibling scripts

**Step 3: Planning Phase Execution (Lines 44-55)**
1. Construct subprocess command:
   ```bash
   uv run {script_dir}/adw_plan.py {issue_number} {adw_id}
   ```
2. Print command for transparency and debugging
3. Execute via `subprocess.run(plan_cmd)`
   - Runs synchronously (blocks until complete)
   - stdout/stderr streams to user console
   - Returns `CompletedProcess` object
4. Check exit code (`plan.returncode`)
   - If non-zero: **EXIT IMMEDIATELY** with code 1
   - If zero: Continue to build phase

**Planning Phase Actions** (via adw_plan.py):
- Fetch GitHub issue #123
- Classify issue type (bug/feature/chore)
- Generate branch name with ADW ID
- Create and checkout git branch
- Generate implementation plan using Claude Code
- Commit plan to branch
- Push branch to remote
- Create initial PR (if configured)
- Update state with: branch_name, plan_file, issue_class

**Step 4: Implementation Phase Execution (Lines 57-68)**
1. Construct subprocess command:
   ```bash
   uv run {script_dir}/adw_build.py {issue_number} {adw_id}
   ```
2. Print command for visibility
3. Execute via `subprocess.run(build_cmd)`
   - Blocks until complete
   - Shows real-time output to user
4. Check exit code (`build.returncode`)
   - If non-zero: **EXIT IMMEDIATELY** with code 1
   - If zero: Continue to test phase

**Implementation Phase Actions** (via adw_build.py):
- Load state from previous phase
- Checkout branch from state
- Load plan file from state
- Implement solution using Claude Code `/implement`
- Commit implementation to branch
- Push to remote
- Update PR (if exists)

**Step 5: Testing Phase Execution (Lines 70-81)**
1. Construct subprocess command:
   ```bash
   uv run {script_dir}/adw_test.py {issue_number} {adw_id}
   ```
2. Print command for tracking
3. Execute via `subprocess.run(test_cmd)`
   - Final phase execution
   - Comprehensive test suite with retries
4. Check exit code (`test.returncode`)
   - If non-zero: **EXIT with code 1** (tests failed)
   - If zero: **EXIT with code 0** (complete success)

**Testing Phase Actions** (via adw_test.py):
- Load state and checkout branch
- Run unit tests with retry (max 4 attempts)
- Resolve failed tests automatically
- Run E2E tests with retry (max 2 attempts)
- Resolve failed E2E tests automatically
- Commit test results
- Push final changes to remote
- Update PR with test results
- Post comprehensive test summary to GitHub issue

#### Sequential Execution Flow

```
START: adw_plan_build_test.py 123
  ↓
ensure_adw_id() → Creates/loads ADW ID (e.g., a1b2c3d4)
  ↓
subprocess: adw_plan.py 123 a1b2c3d4
  ↓ (if exitcode != 0) → EXIT 1
  ↓
Plan Complete: State saved with branch_name, plan_file
  ↓
subprocess: adw_build.py 123 a1b2c3d4
  ↓ (if exitcode != 0) → EXIT 1
  ↓
Build Complete: Implementation committed
  ↓
subprocess: adw_test.py 123 a1b2c3d4
  ↓ (if exitcode != 0) → EXIT 1
  ↓
Tests Complete: All phases successful
  ↓
EXIT 0 (Success)
```

#### State Management

**State Evolution Through Phases**:

**After Planning**:
```json
{
  "adw_id": "a1b2c3d4",
  "issue_number": "123",
  "branch_name": "feat-issue-123-adw-a1b2c3d4-user-auth",
  "plan_file": "specs/issue-123-adw-a1b2c3d4-user-auth.md",
  "issue_class": "/feature"
}
```

**After Building**:
```json
{
  "adw_id": "a1b2c3d4",
  "issue_number": "123",
  "branch_name": "feat-issue-123-adw-a1b2c3d4-user-auth",
  "plan_file": "specs/issue-123-adw-a1b2c3d4-user-auth.md",
  "issue_class": "/feature",
  "pr_number": "456"
}
```

**After Testing**:
```json
{
  "adw_id": "a1b2c3d4",
  "issue_number": "123",
  "branch_name": "feat-issue-123-adw-a1b2c3d4-user-auth",
  "plan_file": "specs/issue-123-adw-a1b2c3d4-user-auth.md",
  "issue_class": "/feature",
  "pr_number": "456"
}
```

**State Persistence**: `agents/{adw_id}/adw_state.json`

**State Access**: Each phase loads state from file (file-based chaining)

#### Error Handling & Failure Modes

**Phase Failure Isolation**:
1. **Planning Fails**: No branch created, no subsequent phases run
2. **Building Fails**: Plan committed but not implemented, no tests run
3. **Testing Fails**: Plan and implementation committed, tests failed

**Exit Codes**:
- `0`: All phases completed successfully
- `1`: At least one phase failed

**Failure Recovery**:
```bash
# If planning failed - restart from beginning
uv run adws/adw_plan_build_test.py 123

# If building failed - skip planning, resume build
uv run adws/adw_build.py 123 a1b2c3d4
uv run adws/adw_test.py 123 a1b2c3d4

# If testing failed - skip plan/build, re-run tests
uv run adws/adw_test.py 123 a1b2c3d4
```

**No Automatic Rollback**: Previous phase artifacts remain committed

#### Output Artifacts

**Complete Workflow Produces**:

1. **Git Branch**: Feature branch with all changes
2. **Commits** (3+):
   - Plan commit: "sdlc_planner: feat: implementation plan"
   - Implementation commit: "sdlc_implementor: feat: add feature"
   - Test commit: "test_runner: feat: test results"
   - Resolution commits (if tests resolved): "test_runner: feat: fix test"
3. **Plan File**: `specs/issue-{number}-adw-{id}-{slug}.md`
4. **State File**: `agents/{adw_id}/adw_state.json`
5. **Logs**:
   - `agents/{adw_id}/sdlc_planner/execution.log`
   - `agents/{adw_id}/sdlc_implementor/execution.log`
   - `agents/{adw_id}/test_runner/execution.log`
6. **Claude Outputs**:
   - `agents/{adw_id}/sdlc_planner/raw_output.jsonl`
   - `agents/{adw_id}/sdlc_implementor/raw_output.jsonl`
   - `agents/{adw_id}/test_runner/raw_output.jsonl`
7. **Pull Request**: On GitHub with all commits
8. **GitHub Comments**: Comprehensive status updates throughout

#### GitHub Integration Timeline

**Comment Sequence**:
1. Planning: "✅ Starting planning phase"
2. Planning: "✅ Issue classified as: /feature"
3. Planning: "✅ Working on branch: feat-issue-123-adw-a1b2c3d4"
4. Planning: "✅ Implementation plan created"
5. Planning: "✅ Plan committed"
6. Planning: "✅ Planning phase completed"
7. Building: "✅ Starting implementation phase"
8. Building: "✅ Solution implemented"
9. Building: "✅ Implementation committed"
10. Building: "✅ Implementation phase completed"
11. Testing: "✅ Starting test suite"
12. Testing: "✅ Running application tests..."
13. Testing: "📊 Final test results" (unit tests)
14. Testing: "✅ Starting E2E tests..."
15. Testing: "📊 Final E2E test results"
16. Testing: "📊 Test Run Summary" (comprehensive)
17. Testing: "✅ Test suite completed"

#### Usage Patterns

**Production Automation**:
```bash
# Full automated workflow
uv run adws/adw_plan_build_test.py 123
```

**Triggered by Cron**:
```python
# In trigger_cron.py
subprocess.run(["uv", "run", "adws/adw_plan_build_test.py", issue_number])
```

**Triggered by Webhook**:
```python
# In trigger_webhook.py
subprocess.run(["uv", "run", "adws/adw_plan_build_test.py", issue_number])
```

**Manual Trigger**:
```bash
# User runs directly for specific issue
uv run adws/adw_plan_build_test.py 123
```

#### Performance Considerations

**Execution Time**:
- Planning: 1-3 minutes (depends on issue complexity)
- Building: 2-5 minutes (depends on implementation size)
- Testing: 3-15 minutes (depends on test failures and retries)
- **Total**: 6-23 minutes typical, can be longer with multiple test retries

**Resource Usage**:
- CPU: Moderate (subprocess execution, Claude Code API calls)
- Memory: Low (file-based state, no large data structures)
- Disk: Moderate (logs, outputs, git objects)
- Network: API calls to Anthropic and GitHub

#### Advantages Over Individual Scripts

1. **Single Command**: Complete workflow in one command
2. **Automatic State Management**: ADW ID handled automatically
3. **Error Propagation**: Stops on first failure
4. **Production Ready**: Designed for automated triggers
5. **Complete Automation**: No manual intervention needed
6. **Comprehensive Logging**: All phases logged separately
7. **GitHub Integration**: Full visibility in issue comments

#### Design Philosophy

**Orchestration Pattern**:
- Uses subprocess execution (not function imports)
- Each phase runs in isolation
- Clean separation of concerns
- Matches production execution model

**Fail-Fast Approach**:
- Stops immediately on phase failure
- Preserves work from successful phases
- Enables targeted recovery

**File-Based State**:
- Robust state sharing between phases
- Survives script crashes
- Enables manual inspection and debugging

**Subprocess Benefits**:
- Fresh environment per phase
- Independent logging per phase
- Easier to debug individual phases
- Can run phases manually for testing

---

### Workflow Script Comparison Matrix

| Feature | adw_plan.py | adw_build.py | adw_test.py | adw_plan_build.py | adw_plan_build_test.py |
|---------|-------------|--------------|-------------|-------------------|------------------------|
| **Lines of Code** | 265 | 232 | 1107 | 72 | 86 |
| **Complexity** | Medium | Medium | High | Low | Low |
| **ADW ID Required** | No | Yes | No | No | No |
| **Creates Branch** | Yes | No | Optional | Yes (via plan) | Yes (via plan) |
| **Reads Plan File** | No | Yes | No | Yes (via build) | Yes (via build) |
| **Runs Tests** | No | No | Yes | No | Yes |
| **Test Retry Logic** | No | No | Yes (4+2) | No | Yes (via test) |
| **Creates Commits** | 1 | 1 | 1+ | 2 | 3+ |
| **Pushes to Remote** | Yes | Yes | Yes | Yes | Yes |
| **Creates PR** | Yes | Optional | Yes | Yes | Yes |
| **Use Case** | Planning only | Implementation only | Testing only | Plan + Build | Full pipeline |
| **Ideal For** | Review before implementation | Resume after plan | Standalone testing | Quick iteration | Production automation |

---

### Common Patterns Across All Scripts

#### 1. State Management Pattern

```python
# Initialize/load state
adw_id = ensure_adw_id(issue_number, adw_id, logger)
state = ADWState.load(adw_id, logger)

# Update state
state.update(key=value)
state.save("script_name")

# Use state
branch_name = state.get("branch_name")
```

#### 2. Error Handling Pattern

```python
if not success:
    logger.error(f"Error: {error}")
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, agent_name, f"❌ Error: {error}")
    )
    sys.exit(1)
```

#### 3. GitHub Status Update Pattern

```python
# Before operation
make_issue_comment(
    issue_number,
    format_issue_message(adw_id, agent_name, "✅ Starting operation")
)

# After operation
make_issue_comment(
    issue_number,
    format_issue_message(adw_id, agent_name, "✅ Operation completed")
)
```

#### 4. Subprocess Orchestration Pattern

```python
# Build command
cmd = ["uv", "run", os.path.join(script_dir, "script.py"), arg1, arg2]

# Execute
print(f"Running: {' '.join(cmd)}")
result = subprocess.run(cmd)

# Check result
if result.returncode != 0:
    sys.exit(1)
```

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
