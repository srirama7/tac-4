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
SCREENSHOT_DIR = BASE_PATH / "agents/475d6f12/e2e_test_resolver_0/img/basic_query"
APPLICATION_URL = "http://localhost:5173"
TEST_NAME = "Basic Query Execution"

# Ensure screenshot directory exists
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def run_test():
    """Execute E2E test steps"""
    test_result = {
        "test_name": TEST_NAME,
        "status": "passed",
        "test_path": ".claude/commands/e2e/test_basic_query.md",
        "screenshots": [],
        "error": None
    }

    browser = None
    try:
        with sync_playwright() as p:
            # Launch browser in headed mode for visibility
            browser = p.chromium.launch(headless=False)
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
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Step 3: Verify page title
            print("Step 3: Verifying page title")
            page_title = page.title()
            if "Natural Language SQL Interface" not in page_title:
                raise AssertionError(f"(Step 3 ❌) Page title mismatch. Expected 'Natural Language SQL Interface', got '{page_title}'")
            print(f"✓ Page title verified: {page_title}")

            # Step 4: Verify core UI elements
            print("Step 4: Verifying core UI elements")

            # Query input textbox
            query_input = page.locator('textarea[placeholder*="Ask a question"]')
            if not query_input.is_visible():
                raise AssertionError("(Step 4 ❌) Query input textbox not found")
            print("✓ Query input textbox found")

            # Query button
            query_button = page.locator('button#query-button')
            if not query_button.is_visible():
                raise AssertionError("(Step 4 ❌) Query button not found")
            print("✓ Query button found")

            # Upload Data button
            upload_button = page.locator('button:has-text("Upload Data")')
            if not upload_button.is_visible():
                raise AssertionError("(Step 4 ❌) Upload Data button not found")
            print("✓ Upload Data button found")

            # Available Tables section
            available_tables = page.locator('text=Available Tables')
            if not available_tables.is_visible():
                raise AssertionError("(Step 4 ❌) Available Tables section not found")
            print("✓ Available Tables section found")

            # Step 5: Enter query
            print("Step 5: Entering query")
            query_text = "Show me all users from the users table"
            query_input.fill(query_text)
            time.sleep(1)
            print(f"✓ Query entered: {query_text}")

            # Step 6: Take screenshot of query input
            print("Step 6: Taking screenshot of query input")
            screenshot_path = SCREENSHOT_DIR / "02_query_input.png"
            page.screenshot(path=str(screenshot_path))
            test_result["screenshots"].append(str(screenshot_path))
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Step 7: Click Query button
            print("Step 7: Clicking Query button")
            query_button.click()
            time.sleep(3)  # Wait for query to execute
            print("✓ Query button clicked")

            # Step 8: Verify query results appear
            print("Step 8: Verifying query results appear")

            # Check for error message
            error_message = page.locator('text=/HTTP error/i')
            if error_message.is_visible():
                error_text = error_message.text_content()
                raise AssertionError(f"(Step 8 ❌) Query execution failed with error: {error_text}")

            # Wait for results to appear
            results_section = page.locator('text=Query Results')
            try:
                results_section.wait_for(state="visible", timeout=5000)
                print("✓ Query results appeared")
            except Exception as e:
                raise AssertionError(f"(Step 8 ❌) Query results did not appear: {str(e)}")

            # Step 9: Verify SQL translation
            print("Step 9: Verifying SQL translation")
            sql_translation = page.locator('text=/SELECT.*FROM.*users/i')
            if not sql_translation.is_visible():
                raise AssertionError("(Step 9 ❌) SQL translation not displayed or does not contain 'SELECT * FROM users'")
            sql_text = sql_translation.text_content()
            print(f"✓ SQL translation verified: {sql_text}")

            # Step 10: Take screenshot of SQL translation
            print("Step 10: Taking screenshot of SQL translation")
            screenshot_path = SCREENSHOT_DIR / "03_sql_translation.png"
            page.screenshot(path=str(screenshot_path))
            test_result["screenshots"].append(str(screenshot_path))
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Step 11: Verify results table contains data
            print("Step 11: Verifying results table contains data")
            results_table = page.locator('table')
            if not results_table.is_visible():
                raise AssertionError("(Step 11 ❌) Results table not found")

            # Check for at least one data row (excluding header)
            table_rows = page.locator('table tbody tr')
            row_count = table_rows.count()
            if row_count == 0:
                raise AssertionError("(Step 11 ❌) Results table is empty")
            print(f"✓ Results table contains {row_count} rows of data")

            # Step 12: Take screenshot of results
            print("Step 12: Taking screenshot of results")
            screenshot_path = SCREENSHOT_DIR / "04_results.png"
            page.screenshot(path=str(screenshot_path))
            test_result["screenshots"].append(str(screenshot_path))
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Step 13: Click Hide button
            print("Step 13: Clicking Hide button")
            hide_button = page.locator('button:has-text("Hide")')
            if not hide_button.is_visible():
                raise AssertionError("(Step 13 ❌) Hide button not found")
            hide_button.click()
            time.sleep(1)
            print("✓ Hide button clicked")

            # Verify results are hidden
            if results_section.is_visible():
                raise AssertionError("(Step 13 ❌) Results section did not hide after clicking Hide button")
            print("✓ Results section hidden successfully")

            print("\n✓ All test steps completed successfully!")
            test_result["status"] = "passed"

    except AssertionError as e:
        print(f"\n✗ Test failed: {str(e)}")
        test_result["status"] = "failed"
        test_result["error"] = str(e)

        # Take error screenshot
        try:
            if browser:
                screenshot_path = SCREENSHOT_DIR / "99_error.png"
                page.screenshot(path=str(screenshot_path))
                test_result["screenshots"].append(str(screenshot_path))
                print(f"Error screenshot saved: {screenshot_path}")
        except:
            pass

    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        test_result["status"] = "failed"
        test_result["error"] = f"Unexpected error: {str(e)}"

        # Take error screenshot
        try:
            if browser:
                screenshot_path = SCREENSHOT_DIR / "99_error.png"
                page.screenshot(path=str(screenshot_path))
                test_result["screenshots"].append(str(screenshot_path))
                print(f"Error screenshot saved: {screenshot_path}")
        except:
            pass

    finally:
        try:
            if browser:
                browser.close()
        except:
            pass

    return test_result

if __name__ == "__main__":
    result = run_test()
    print("\n" + "="*60)
    print("TEST RESULT:")
    print("="*60)
    print(json.dumps(result, indent=2))
