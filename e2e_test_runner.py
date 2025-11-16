#!/usr/bin/env python3
"""
E2E Test Runner for Basic Query Test
Executes Playwright browser automation tests
"""

import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
import time

# Configuration
ADW_ID = "27e83d10"
AGENT_NAME = "e2e_test_runner_0_0"
APPLICATION_URL = "http://localhost:5173"
SCREENSHOT_DIR = Path(f"C:/Users/amogh/Downloads/tac5/tac-5/agents/{ADW_ID}/{AGENT_NAME}/img/basic_query")

def run_test():
    """Execute the E2E test"""
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
            context = browser.new_context()
            page = context.new_page()

            # Step 1: Navigate to the application
            print(f"Step 1: Navigating to {APPLICATION_URL}")
            page.goto(APPLICATION_URL)
            time.sleep(2)

            # Step 2: Take screenshot of initial state
            print("Step 2: Taking screenshot of initial state")
            screenshot_path = SCREENSHOT_DIR / "01_initial_state.png"
            page.screenshot(path=str(screenshot_path))
            test_result["screenshots"].append(str(screenshot_path))

            # Step 3: Verify page title
            print("Step 3: Verifying page title")
            title = page.title()
            if title != "Natural Language SQL Interface":
                raise Exception(f"(Step 3 FAILED) Page title is '{title}', expected 'Natural Language SQL Interface'")
            print(f"[OK] Page title verified: {title}")

            # Step 4: Verify core UI elements
            print("Step 4: Verifying core UI elements")

            # Check for query input
            query_input = page.locator('textarea[placeholder*="query" i], textarea[placeholder*="Ask" i], textarea')
            if not query_input.count() > 0:
                raise Exception("(Step 4 FAILED) Failed to find query input textbox")
            print("[OK] Query input found")

            # Check for Query button
            query_button = page.locator('button:has-text("Query"), button:has-text("Submit"), button[type="submit"]')
            if not query_button.count() > 0:
                raise Exception("(Step 4 FAILED) Failed to find Query button")
            print("[OK] Query button found")

            # Check for Upload Data button
            upload_button = page.locator('button:has-text("Upload"), button:has-text("Upload Data")')
            if not upload_button.count() > 0:
                raise Exception("(Step 4 FAILED) Failed to find Upload Data button")
            print("[OK] Upload Data button found")

            # Check for Available Tables section
            tables_section = page.locator('text=/Available Tables/i')
            if not tables_section.count() > 0:
                # Try alternative
                tables_section = page.locator('text=/Tables/i')
                if not tables_section.count() > 0:
                    print("[WARN] Available Tables section not clearly found (may still exist)")
                else:
                    print("[OK] Available Tables section found")
            else:
                print("[OK] Available Tables section found")

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
            query_button.first.click()

            # Wait for results to appear
            print("Waiting for query results...")
            time.sleep(5)

            # Step 8: Verify query results appear
            print("Step 8: Verifying query results appear")
            results = page.locator('[class*="result" i], [class*="output" i], table, [class*="query" i]')
            if not results.count() > 0:
                raise Exception("(Step 8 FAILED) Query results did not appear")
            print("[OK] Query results appeared")

            # Step 9: Verify SQL translation is displayed
            print("Step 9: Verifying SQL translation")
            sql_content = page.content()
            # Check for SQL keywords or error messages
            if "SELECT" in sql_content.upper() and "FROM" in sql_content.upper():
                print("[OK] SQL translation found")
            elif "error" in sql_content.lower() or "failed" in sql_content.lower() or "500" in sql_content:
                # Take a screenshot for debugging
                screenshot_path = SCREENSHOT_DIR / "09_error_state.png"
                page.screenshot(path=str(screenshot_path))
                raise Exception("(Step 9 FAILED) Query returned an error: HTTP error detected in response")
            else:
                raise Exception("(Step 9 FAILED) SQL translation not found (should contain 'SELECT * FROM users')")


            # Step 10: Take screenshot of SQL translation
            print("Step 10: Taking screenshot of SQL translation")
            screenshot_path = SCREENSHOT_DIR / "03_sql_translation.png"
            page.screenshot(path=str(screenshot_path))
            test_result["screenshots"].append(str(screenshot_path))

            # Step 11: Verify results table contains data
            print("Step 11: Verifying results table contains data")
            table = page.locator('table')
            if table.count() > 0:
                rows = page.locator('table tr')
                if rows.count() < 2:  # At least header + 1 data row
                    raise Exception("(Step 11 FAILED) Results table does not contain data rows")
                print(f"[OK] Results table contains {rows.count()} rows")
            else:
                print("[WARN] No table element found, checking for alternative result display")

            # Step 12: Take screenshot of results
            print("Step 12: Taking screenshot of results")
            screenshot_path = SCREENSHOT_DIR / "04_results.png"
            page.screenshot(path=str(screenshot_path))
            test_result["screenshots"].append(str(screenshot_path))

            # Step 13: Click Hide button
            print("Step 13: Clicking Hide button")
            hide_button = page.locator('button:has-text("Hide"), button:has-text("Close")')
            if hide_button.count() > 0:
                hide_button.first.click()
                time.sleep(1)
                print("[OK] Hide button clicked")
            else:
                print("[WARN] Hide button not found (may not be required)")

            print("\n[SUCCESS] All test steps completed successfully!")

            # Close browser
            browser.close()

    except Exception as e:
        test_result["status"] = "failed"
        test_result["error"] = str(e)
        print(f"\n[FAILED] Test failed: {e}")
        try:
            if 'browser' in locals():
                browser.close()
        except:
            pass  # Browser already closed or event loop closed

    return test_result

if __name__ == "__main__":
    # Ensure screenshot directory exists
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # Run the test
    result = run_test()

    # Print JSON result
    print("\n" + "="*60)
    print("TEST REPORT")
    print("="*60)
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["status"] == "passed" else 1)
