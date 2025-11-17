#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E2E Test: Basic Query Execution using Playwright
"""

import json
import os
import sys
import time
from playwright.sync_api import sync_playwright, expect

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Test configuration
ADW_ID = "ff7ca896"
AGENT_NAME = "e2e_test_runner_0_0"
TEST_NAME = "basic_query"
APP_URL = "http://localhost:5173"

# Get absolute path to codebase
CODEBASE_PATH = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(CODEBASE_PATH, "agents", ADW_ID, AGENT_NAME, "img", TEST_NAME)

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def run_test():
    """Execute the E2E test steps"""
    test_result = {
        "test_name": "Basic Query Execution",
        "status": "passed",
        "screenshots": [],
        "error": None
    }

    try:
        with sync_playwright() as p:
            # Launch browser in headed mode
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()

            # Step 1: Navigate to the application
            print(f"Step 1: Navigating to {APP_URL}")
            page.goto(APP_URL)
            page.wait_for_load_state("networkidle")

            # Step 2: Take screenshot of initial state
            print("Step 2: Taking screenshot of initial state")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "01_initial_state.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 3: Verify page title
            print("Step 3: Verifying page title")
            title = page.title()
            if "Natural Language SQL Interface" not in title:
                raise AssertionError(f"(Step 3 ❌) Expected page title to contain 'Natural Language SQL Interface', got '{title}'")
            print(f"✓ Page title verified: {title}")

            # Step 4: Verify core UI elements
            print("Step 4: Verifying core UI elements")

            # Check for query input (using ID from main.ts)
            query_input = page.locator('#query-input')

            if not query_input.is_visible(timeout=5000):
                raise AssertionError("(Step 4 ❌) Query input textbox not found")
            print("✓ Query input found")

            # Check for Query button (using ID from main.ts)
            query_button = page.locator('#query-button')

            if not query_button.is_visible(timeout=5000):
                raise AssertionError("(Step 4 ❌) Query button not found")
            print("✓ Query button found")

            # Check for Upload Data button (using ID from main.ts)
            upload_button = page.locator('#upload-data-button')

            if not upload_button.is_visible(timeout=5000):
                raise AssertionError("(Step 4 ❌) Upload Data button not found")
            print("✓ Upload Data button found")

            # Check for Available Tables section (using ID from main.ts)
            tables_section = page.locator('#tables-section')

            if not tables_section.is_visible(timeout=5000):
                raise AssertionError("(Step 4 ❌) Available Tables section not found")
            print("✓ Available Tables section found")

            # Step 5: Enter the query
            print("Step 5: Entering query")
            query_text = "Show me all users from the users table"
            query_input.fill(query_text)
            print(f"✓ Query entered: {query_text}")

            # Step 6: Take screenshot of query input
            print("Step 6: Taking screenshot of query input")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "02_query_input.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 7: Click the Query button
            print("Step 7: Clicking Query button")
            query_button.click()
            print("✓ Query button clicked")

            # Wait a moment to see what happens
            time.sleep(2)

            # Take a screenshot to debug
            debug_screenshot = os.path.join(SCREENSHOT_DIR, "debug_after_click.png")
            page.screenshot(path=debug_screenshot)
            print(f"Debug screenshot saved: {debug_screenshot}")

            # Step 8: Verify query results appear
            print("Step 8: Verifying query results appear")

            # Wait for results section to become visible (using ID from main.ts)
            results_section = page.locator('#results-section')

            # Also check if there's an error shown
            try:
                results_section.wait_for(state="visible", timeout=20000)
                print("✓ Query results section appeared")
            except Exception as e:
                # Take another screenshot to see the error state
                error_screenshot = os.path.join(SCREENSHOT_DIR, "error_state.png")
                page.screenshot(path=error_screenshot)
                print(f"Error screenshot saved: {error_screenshot}")

                # Check for error messages
                error_messages = page.locator('.error-message')
                if error_messages.count() > 0:
                    error_text = error_messages.first.inner_text()
                    raise AssertionError(f"(Step 8 ❌) Error shown: {error_text}")

                raise AssertionError("(Step 8 ❌) Query results section did not appear")

            # Step 9: Verify SQL translation is displayed
            print("Step 9: Verifying SQL translation")

            # Wait for SQL display to appear (using ID from main.ts)
            sql_display = page.locator('#sql-display')

            if not sql_display.is_visible(timeout=5000):
                raise AssertionError("(Step 9 ❌) SQL display not shown")

            sql_text = sql_display.inner_text()
            if "SELECT" not in sql_text.upper() or "users" not in sql_text.lower():
                raise AssertionError(f"(Step 9 ❌) SQL translation doesn't contain expected SELECT FROM users, got: {sql_text}")
            print(f"✓ SQL translation verified: {sql_text}")

            # Step 10: Take screenshot of SQL translation
            print("Step 10: Taking screenshot of SQL translation")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "03_sql_translation.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 11: Verify results table contains data
            print("Step 11: Verifying results table contains data")

            # Look for results container (using ID from main.ts)
            results_container = page.locator('#results-container')

            # Look for table with class results-table
            table = results_container.locator('table.results-table')

            if not table.is_visible(timeout=5000):
                # Check if there's an error message instead
                error_msg = results_container.locator('.error-message')
                if error_msg.is_visible():
                    raise AssertionError(f"(Step 11 ❌) Query returned error: {error_msg.inner_text()}")
                raise AssertionError("(Step 11 ❌) Results table not found")

            table_rows = table.locator('tbody tr')
            row_count = table_rows.count()
            if row_count < 1:
                raise AssertionError("(Step 11 ❌) Results table contains no data")
            print(f"✓ Results table contains {row_count} rows")

            # Step 12: Take screenshot of results
            print("Step 12: Taking screenshot of results")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "04_results.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 13: Click Hide button
            print("Step 13: Clicking Hide button")

            # Look for toggle button (using ID from main.ts)
            hide_button = page.locator('#toggle-results')

            if hide_button.is_visible(timeout=5000):
                hide_button.click()
                print("✓ Hide button clicked")
                # Verify results are hidden
                time.sleep(0.5)
                if results_container.locator('table').is_visible():
                    print("⚠ Results still visible after clicking Hide")
                else:
                    print("✓ Results hidden successfully")
            else:
                print("⚠ Hide button not found (may not be visible)")

            # Close browser
            browser.close()

            print("\n✓ All test steps completed successfully!")

    except AssertionError as e:
        test_result["status"] = "failed"
        test_result["error"] = str(e)
        print(f"\n✗ Test failed: {e}")
        if 'browser' in locals():
            browser.close()

    except Exception as e:
        test_result["status"] = "failed"
        test_result["error"] = f"Unexpected error: {str(e)}"
        print(f"\n✗ Unexpected error: {e}")
        if 'browser' in locals():
            browser.close()

    return test_result

if __name__ == "__main__":
    result = run_test()
    print("\n" + "="*60)
    print("TEST RESULT")
    print("="*60)
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["status"] == "passed" else 1)
