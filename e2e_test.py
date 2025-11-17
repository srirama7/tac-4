#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E2E Test: Basic Query Execution
Executes end-to-end tests using Playwright browser automation
"""

import json
import sys
import io
from playwright.sync_api import sync_playwright, expect
import time

# Set UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
APPLICATION_URL = "http://localhost:5174"
SCREENSHOT_DIR = "C:/Users/amogh/Downloads/tac5/tac-5/agents/78a3fe42/e2e_test_runner_1_0/img/basic_query"

def run_test():
    test_results = {
        "test_name": "Basic Query Execution",
        "status": "failed",  # Will be updated to "passed" if all steps succeed
        "screenshots": [],
        "error": None
    }

    try:
        with sync_playwright() as p:
            # Launch browser in headed mode for visibility
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            print("Step 1: Navigate to the Application URL")
            page.goto(APPLICATION_URL)
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            print("Step 2: Take a screenshot of the initial state")
            screenshot_path = f"{SCREENSHOT_DIR}/01_initial_state.png"
            page.screenshot(path=screenshot_path)
            test_results["screenshots"].append(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

            print("Step 3: Verify the page title is 'Natural Language SQL Interface'")
            try:
                expect(page).to_have_title("Natural Language SQL Interface", timeout=5000)
                print("✓ Page title verified")
            except Exception as e:
                test_results["error"] = f"(Step 3 ❌) Failed to verify page title: {str(e)}"
                print(test_results["error"])
                browser.close()
                return test_results

            print("Step 4: Verify core UI elements are present")

            # Check for query input textbox
            try:
                query_input = page.locator('#query-input')
                expect(query_input).to_be_visible(timeout=5000)
                print("  ✓ Query input textbox found")
            except Exception as e:
                test_results["error"] = f'(Step 4 ❌) Failed to find query input textbox: {str(e)}'
                print(test_results["error"])
                browser.close()
                return test_results

            # Check for Query button
            try:
                query_button = page.locator('#query-button')
                expect(query_button).to_be_visible(timeout=5000)
                print("  ✓ Query button found")
            except Exception as e:
                test_results["error"] = f'(Step 4 ❌) Failed to find Query button: {str(e)}'
                print(test_results["error"])
                browser.close()
                return test_results

            # Check for Upload Data button
            try:
                upload_button = page.locator('button:has-text("Upload Data")')
                expect(upload_button).to_be_visible(timeout=5000)
                print("  ✓ Upload Data button found")
            except Exception as e:
                test_results["error"] = f'(Step 4 ❌) Failed to find Upload Data button: {str(e)}'
                print(test_results["error"])
                browser.close()
                return test_results

            # Check for Available Tables section
            try:
                tables_section = page.locator('h3:has-text("Available Tables")')
                expect(tables_section).to_be_visible(timeout=5000)
                print("  ✓ Available Tables section found")
            except Exception as e:
                test_results["error"] = f'(Step 4 ❌) Failed to find Available Tables section: {str(e)}'
                print(test_results["error"])
                browser.close()
                return test_results

            print("Step 5: Enter the query: 'Show me all users from the users table'")
            query_input.fill("Show me all users from the users table")
            time.sleep(1)

            print("Step 6: Take a screenshot of the query input")
            screenshot_path = f"{SCREENSHOT_DIR}/02_query_input.png"
            page.screenshot(path=screenshot_path)
            test_results["screenshots"].append(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

            print("Step 7: Click the Query button")
            query_button.click()

            # Wait for results to appear
            print("Step 8: Verify the query results appear")

            try:
                # Look for results section to become visible
                results_section = page.locator('#results-section')
                expect(results_section).to_be_visible(timeout=20000)
                print("✓ Query results appeared")
            except Exception as e:
                # Take a debug screenshot to see what happened
                debug_screenshot = f"{SCREENSHOT_DIR}/debug_error.png"
                page.screenshot(path=debug_screenshot)
                test_results["screenshots"].append(debug_screenshot)
                test_results["error"] = f'(Step 8 ❌) Failed to find query results: {str(e)}'
                print(test_results["error"])
                print(f"Debug screenshot saved: {debug_screenshot}")
                browser.close()
                return test_results

            print("Step 9: Verify the SQL translation is displayed (should contain 'SELECT * FROM users')")
            try:
                # Wait a moment for content to load
                time.sleep(2)

                # Take screenshot before checking content
                screenshot_path_temp = f"{SCREENSHOT_DIR}/03_sql_translation.png"
                page.screenshot(path=screenshot_path_temp)
                test_results["screenshots"].append(screenshot_path_temp)
                print(f"Screenshot saved: {screenshot_path_temp}")

                # Check for error message first
                error_msg = page.locator('.error, [class*="error"]').first
                if error_msg.is_visible():
                    error_text = error_msg.text_content()
                    raise Exception(f"Query execution failed with error: {error_text}")

                # Look for SQL display element
                sql_display = page.locator('#sql-display')
                expect(sql_display).to_be_visible(timeout=5000)
                sql_text = sql_display.text_content()

                if sql_text and "SELECT" in sql_text.upper() and "FROM" in sql_text.upper():
                    print(f"✓ SQL translation verified: {sql_text[:100]}...")
                else:
                    raise Exception(f"SQL translation doesn't match expected pattern. Found: '{sql_text}'")
            except Exception as e:
                test_results["error"] = f'(Step 9 ❌) Failed to verify SQL translation: {str(e)}'
                print(test_results["error"])
                browser.close()
                return test_results

            print("Step 11: Verify the results table contains data")
            try:
                # Look for table rows with data
                table_rows = page.locator('table tr, [role="row"]')
                row_count = table_rows.count()
                if row_count > 1:  # At least header + 1 data row
                    print(f"✓ Results table contains data ({row_count} rows)")
                else:
                    raise Exception(f"Results table has insufficient data: {row_count} rows")
            except Exception as e:
                test_results["error"] = f'(Step 11 ❌) Failed to verify results table data: {str(e)}'
                print(test_results["error"])
                browser.close()
                return test_results

            print("Step 12: Take a screenshot of the results")
            screenshot_path = f"{SCREENSHOT_DIR}/04_results.png"
            page.screenshot(path=screenshot_path)
            test_results["screenshots"].append(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

            print("Step 13: Click 'Hide' button to close results")
            try:
                hide_button = page.locator('button:has-text("Hide")')
                expect(hide_button).to_be_visible(timeout=5000)
                hide_button.click()
                time.sleep(1)
                print("✓ Hide button clicked successfully")
            except Exception as e:
                test_results["error"] = f'(Step 13 ❌) Failed to click Hide button: {str(e)}'
                print(test_results["error"])
                browser.close()
                return test_results

            # All steps passed
            test_results["status"] = "passed"
            print("\n✓ All test steps completed successfully!")

            # Close browser
            browser.close()

    except Exception as e:
        test_results["error"] = f"Unexpected error during test execution: {str(e)}"
        print(test_results["error"])

    return test_results

if __name__ == "__main__":
    results = run_test()

    # Print final JSON output
    print("\n" + "="*80)
    print("FINAL TEST RESULTS:")
    print("="*80)
    print(json.dumps(results, indent=2))

    # Exit with appropriate code
    sys.exit(0 if results["status"] == "passed" else 1)
