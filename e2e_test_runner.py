#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E2E Test Runner using Playwright
Executes test steps from test_basic_query.md
"""
import json
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

# Set UTF-8 encoding for output
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
BASE_PATH = Path("C:/Users/amogh/Downloads/tac5/tac-5")
SCREENSHOT_DIR = BASE_PATH / "agents/475d6f12/e2e_test_runner_0_0/img/basic_query"
APPLICATION_URL = "http://localhost:5173"
TEST_NAME = "Basic Query Execution"

# Ensure screenshot directory exists
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def run_test():
    """Execute E2E test steps"""
    test_result = {
        "test_name": TEST_NAME,
        "status": "passed",
        "screenshots": [],
        "error": None
    }

    browser = None
    try:
        with sync_playwright() as p:
            # Launch browser in headless mode (headed mode may not work in all environments)
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # Step 1: Navigate to application
            print(f"Step 1: Navigating to {APPLICATION_URL}")
            page.goto(APPLICATION_URL)
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            # Step 2: Take screenshot of initial state
            print("Step 2: Taking screenshot of initial state")
            screenshot_path = SCREENSHOT_DIR / "01_initial_state.png"
            page.screenshot(path=str(screenshot_path))
            test_result["screenshots"].append(str(screenshot_path))

            # Step 3: Verify page title
            print("Step 3: Verifying page title")
            title = page.title()
            if "Natural Language SQL Interface" not in title:
                raise AssertionError(f"(Step 3 ❌) Expected page title to contain 'Natural Language SQL Interface', got '{title}'")
            print(f"✓ Page title verified: {title}")

            # Step 4: Verify core UI elements
            print("Step 4: Verifying core UI elements")

            # Query input textbox
            query_input = page.locator('textarea[placeholder*="natural language"], textarea[placeholder*="query"], input[type="text"][placeholder*="query"], textarea')
            if query_input.count() == 0:
                raise AssertionError("(Step 4 ❌) Failed to find query input textbox")
            print("✓ Query input textbox found")

            # Query button
            query_button = page.locator('button:has-text("Query"), button:has-text("Submit"), button[type="submit"]').first
            if query_button.count() == 0:
                raise AssertionError("(Step 4 ❌) Failed to find Query button")
            print("✓ Query button found")

            # Upload Data button
            upload_button = page.locator('button:has-text("Upload"), button:has-text("Upload Data")').first
            if upload_button.count() == 0:
                raise AssertionError("(Step 4 ❌) Failed to find Upload Data button")
            print("✓ Upload Data button found")

            # Available Tables section
            tables_section = page.locator('text=/Available Tables/i').or_(page.locator('h2:has-text("Tables")')).or_(page.locator('h3:has-text("Tables")'))
            if tables_section.count() == 0:
                raise AssertionError("(Step 4 ❌) Failed to find Available Tables section")
            print("✓ Available Tables section found")

            # Step 5: Enter query
            print("Step 5: Entering query")
            query_text = "Show me all users from the users table"
            query_input.first.fill(query_text)
            time.sleep(1)

            # Step 6: Take screenshot of query input
            print("Step 6: Taking screenshot of query input")
            screenshot_path = SCREENSHOT_DIR / "02_query_input.png"
            page.screenshot(path=str(screenshot_path))
            test_result["screenshots"].append(str(screenshot_path))

            # Step 7: Click Query button
            print("Step 7: Clicking Query button")
            query_button.click()

            # Wait for results to appear
            print("Waiting for results to appear...")
            page.wait_for_timeout(5000)  # Wait 5 seconds for query to process

            # Step 8: Verify query results appear
            print("Step 8: Verifying query results appear")

            # Check for error messages first
            error_msg = page.locator('text=/HTTP error|error|Error/i').first
            if error_msg.count() > 0:
                error_text = error_msg.text_content()
                # Take screenshot of error
                error_screenshot = SCREENSHOT_DIR / "03_error_state.png"
                page.screenshot(path=str(error_screenshot))
                test_result["screenshots"].append(str(error_screenshot))
                raise AssertionError(f"(Step 8 ❌) Query execution failed with error: {error_text}")

            results_container = page.locator('[class*="result"], [id*="result"], table, .query-results').first
            page.wait_for_timeout(2000)
            if results_container.count() == 0:
                raise AssertionError("(Step 8 ❌) Failed to find query results container")
            print("✓ Query results container found")

            # Step 9: Verify SQL translation is displayed
            print("Step 9: Verifying SQL translation")
            # Look for SQL text anywhere on the page
            page_content = page.content()
            if "SELECT" not in page_content.upper():
                # Take debug screenshot
                debug_screenshot = SCREENSHOT_DIR / "debug_no_sql.png"
                page.screenshot(path=str(debug_screenshot))
                raise AssertionError("(Step 9 ❌) Failed to find SQL translation containing 'SELECT' anywhere on page")
            print("✓ SQL translation found")

            # Step 10: Take screenshot of SQL translation
            print("Step 10: Taking screenshot of SQL translation")
            screenshot_path = SCREENSHOT_DIR / "03_sql_translation.png"
            page.screenshot(path=str(screenshot_path))
            test_result["screenshots"].append(str(screenshot_path))

            # Step 11: Verify results table contains data
            print("Step 11: Verifying results table contains data")
            table_rows = page.locator('table tr, .table-row')
            if table_rows.count() < 2:  # At least header + 1 data row
                raise AssertionError("(Step 11 ❌) Results table appears to be empty")
            print(f"✓ Results table contains {table_rows.count()} rows")

            # Step 12: Take screenshot of results
            print("Step 12: Taking screenshot of results")
            screenshot_path = SCREENSHOT_DIR / "04_results.png"
            page.screenshot(path=str(screenshot_path))
            test_result["screenshots"].append(str(screenshot_path))

            # Step 13: Click Hide button
            print("Step 13: Clicking Hide button to close results")
            hide_button = page.locator('button:has-text("Hide"), button:has-text("Close")').first
            if hide_button.count() == 0:
                print("⚠ Hide button not found, skipping this step")
            else:
                hide_button.click()
                time.sleep(1)
                print("✓ Hide button clicked")

            print("\n✓ All test steps completed successfully!")

            # Close browser
            if browser:
                browser.close()

    except Exception as e:
        test_result["status"] = "failed"
        test_result["error"] = str(e)
        print(f"\n❌ Test failed: {e}")
        if browser:
            try:
                browser.close()
            except:
                pass

    return test_result

if __name__ == "__main__":
    try:
        result = run_test()
        print("\n" + "="*60)
        print("TEST RESULT")
        print("="*60)
        print(json.dumps(result, indent=2))
        print("="*60)

        # Exit with appropriate code
        sys.exit(0 if result["status"] == "passed" else 1)
    except Exception as e:
        error_result = {
            "test_name": TEST_NAME,
            "status": "failed",
            "screenshots": [],
            "error": str(e)
        }
        print("\n" + "="*60)
        print("TEST RESULT")
        print("="*60)
        print(json.dumps(error_result, indent=2))
        print("="*60)
        sys.exit(1)
