# E2E Test Runner

Execute end-to-end (E2E) tests using Playwright browser automation. If any errors occur and assertions fail mark the test as failed and explain exactly what went wrong.

## Variables

adw_id: $1 if provided, otherwise generate a random 8 character hex string
agent_name: $2 if provided, otherwise use 'test_e2e'
e2e_test_file: $3
application_url: $4 if provided, otherwise use http://localhost:5173

## Execution Strategy

**IMPORTANT**: This test can be executed in two ways:

1. **MCP Playwright Tools (Preferred)**: If Playwright MCP tools are available, use them directly for browser automation
2. **Python Playwright Package (Fallback)**: If MCP tools are NOT available, create and execute a Python script using the `playwright` package

### Detecting MCP Availability

Check if Playwright MCP tools (like `mcp__playwright__*`) are available. If they are NOT available, you MUST use the Python fallback approach described below.

### Python Fallback Approach

When MCP tools are unavailable:
1. Create a temporary Python script that implements the test steps using `playwright.sync_api`
2. The script should:
   - Import `from playwright.sync_api import sync_playwright`
   - Read and parse the test file to understand the steps
   - Execute each test step programmatically
   - Capture screenshots at the specified points
   - Return results in the required JSON format
3. Execute the Python script using: `uv run --with playwright <script_path>`
4. Parse the JSON output from the script

## Instructions

- Read the `e2e_test_file`
- Digest the `User Story` to first understand what we're validating
- IMPORTANT: Check if Playwright MCP tools are available. If NOT, use the Python fallback approach
- IMPORTANT: Execute the `Test Steps` detailed in the `e2e_test_file` using Playwright browser automation
- Review the `Success Criteria` and if any of them fail, mark the test as failed and explain exactly what went wrong
- Review the steps that say '**Verify**...' and if they fail, mark the test as failed and explain exactly what went wrong
- Capture screenshots as specified
- IMPORTANT: Return results in the format requested by the `Output Format`
- Initialize Playwright browser in headed mode for visibility
- Use the `application_url`
- Allow time for async operations and element visibility
- IMPORTANT: After taking each screenshot, save it to `Screenshot Directory` with descriptive names. Use absolute paths to move the files to the `Screenshot Directory` with the correct name.
- Capture and report any errors encountered
- Ultra think about the `Test Steps` and execute them in order
- If you encounter an error, mark the test as failed immediately and explain exactly what went wrong and on what step it occurred. For example: '(Step 1 ❌) Failed to find element with selector "query-input" on page "http://localhost:5173"'
- Use `pwd` or equivalent to get the absolute path to the codebase for writing and displaying the correct paths to the screenshots

## Setup

- IMPORTANT: Reset the database by running `scripts/reset_db.sh`
- IMPORTANT: Make sure the server and client are running on a background process before executing the test steps. Read `scripts/` and `README.md` for more information on how to start, stop and reset the server and client


## Screenshot Directory

<absolute path to codebase>/agents/<adw_id>/<agent_name>/img/<directory name based on test file name>/*.png

Each screenshot should be saved with a descriptive name that reflects what is being captured. The directory structure ensures that:
- Screenshots are organized by ADW ID (workflow run)
- They are stored under the specified agent name (e.g., e2e_test_runner_0, e2e_test_resolver_iter1_0)
- Each test has its own subdirectory based on the test file name (e.g., test_basic_query → basic_query/)

## Report

- Exclusively return the JSON output as specified in the test file
- Capture any unexpected errors
- IMPORTANT: Ensure all screenshots are saved in the `Screenshot Directory`

### Output Format

```json
{
  "test_name": "Test Name Here",
  "status": "passed|failed",
  "screenshots": [
    "<absolute path to codebase>/agents/<adw_id>/<agent_name>/img/<test name>/01_<descriptive name>.png",
    "<absolute path to codebase>/agents/<adw_id>/<agent_name>/img/<test name>/02_<descriptive name>.png",
    "<absolute path to codebase>/agents/<adw_id>/<agent_name>/img/<test name>/03_<descriptive name>.png"
  ],
  "error": null
}
```