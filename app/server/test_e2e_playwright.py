#!/usr/bin/env python3
"""
E2E Test: Basic Query Execution
Automated test using Playwright to validate the Natural Language SQL Interface
"""

import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

# Test configuration
ADW_ID = "073ed71b"
AGENT_NAME = "e2e_test_runner_0_0"
APPLICATION_URL = "http://localhost:5173"
BASE_PATH = Path("C:/Users/amogh/Downloads/tac5/tac-5")
SCREENSHOT_DIR = BASE_PATH / "agents" / ADW_ID / AGENT_NAME / "img" / "basic_query"

def run_test():
    """Execute the E2E test"""
    test_result = {
        "test_name": "Basic Query Execution",
        "status": "failed",
        "screenshots": [],
        "error": None
    }

    try:
        with sync_playwright() as p:
            # Launch browser in headed mode
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()

            # Step 1: Navigate to application
            print(f"Step 1: Navigating to {APPLICATION_URL}...")
            page.goto(APPLICATION_URL, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)

            # Step 2: Take screenshot of initial state
            print("Step 2: Taking screenshot of initial state...")
            screenshot_path = SCREENSHOT_DIR / "01_initial_state.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            test_result["screenshots"].append(str(screenshot_path))

            # Step 3: Verify page title
            print("Step 3: Verifying page title...")
            title = page.title()
            if "Natural Language SQL Interface" not in title:
                raise AssertionError(f"(Step 3 FAILED) Expected title to contain 'Natural Language SQL Interface', got '{title}'")
            print(f"[PASS] Page title verified: {title}")

            # Step 4: Verify core UI elements
            print("Step 4: Verifying core UI elements...")

            # Check for query input textbox
            query_input = page.locator('textarea[placeholder*="natural language"]').or_(
                page.locator('textarea[placeholder*="query"]')
            ).or_(page.locator('textarea').first)

            if not query_input.is_visible(timeout=5000):
                raise AssertionError("(Step 4 FAILED) Query input textbox not found")
            print("[PASS] Query input textbox found")

            # Check for Query button
            query_button = page.get_by_role("button", name="Query", exact=True)
            if not query_button.is_visible(timeout=5000):
                raise AssertionError("(Step 4 FAILED) Query button not found")
            print("[PASS] Query button found")

            # Check for Upload Data button
            upload_button = page.get_by_role("button", name="Upload Data").or_(
                page.locator('button:has-text("Upload Data")')
            )
            if not upload_button.is_visible(timeout=5000):
                raise AssertionError("(Step 4 FAILED) Upload Data button not found")
            print("[PASS] Upload Data button found")

            # Check for Available Tables section
            tables_section = page.locator('text=/Available Tables/i').or_(
                page.locator('h2:has-text("Available Tables")').or_(
                    page.locator('h3:has-text("Available Tables")')
                )
            )
            if not tables_section.is_visible(timeout=5000):
                raise AssertionError("(Step 4 FAILED) Available Tables section not found")
            print("[PASS] Available Tables section found")

            # Step 4b: Verify tables are loaded
            print("Step 4b: Verifying database tables are loaded...")
            page.wait_for_timeout(2000)  # Wait for schema to load

            # Check if users table is visible
            users_table_visible = page.locator('text=/users/i').first.is_visible(timeout=3000)
            if not users_table_visible:
                # Take screenshot showing no tables
                no_tables_path = SCREENSHOT_DIR / "debug_no_tables.png"
                page.screenshot(path=str(no_tables_path), full_page=True)
                raise AssertionError(f"(Step 4b FAILED) Users table not found in Available Tables. The database may not be loaded. Screenshot: {no_tables_path}")
            print("[PASS] Users table is loaded and visible")

            # Step 5: Enter the query
            print("Step 5: Entering query...")
            query_text = "Show me all users from the users table"
            query_input.fill(query_text)
            page.wait_for_timeout(1000)

            # Step 6: Take screenshot of query input
            print("Step 6: Taking screenshot of query input...")
            screenshot_path = SCREENSHOT_DIR / "02_query_input.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            test_result["screenshots"].append(str(screenshot_path))

            # Step 7: Click the Query button
            print("Step 7: Clicking Query button...")
            query_button.click()

            # Wait for results to load
            page.wait_for_timeout(5000)

            # Step 8: Verify query results appear
            print("Step 8: Verifying query results appear...")

            # First check if there's an error message
            http_error = page.locator('text=/HTTP error/i')
            if http_error.is_visible(timeout=2000):
                error_text = http_error.inner_text()
                # Take error screenshot
                error_path = SCREENSHOT_DIR / "debug_http_error.png"
                page.screenshot(path=str(error_path), full_page=True)
                raise AssertionError(f"(Step 8 FAILED) Query returned an error: {error_text}. This may be due to missing API keys or backend configuration. Screenshot: {error_path}")

            results_section = page.locator('#results-section').or_(
                page.get_by_role("heading", name="Query Results")
            ).first

            if not results_section.is_visible(timeout=10000):
                # Try looking for SQL text or table data as alternative indicators
                sql_visible = page.locator('text=/SELECT/i').first.is_visible(timeout=2000)
                table_visible = page.locator('table').first.is_visible(timeout=2000)

                if not sql_visible and not table_visible:
                    raise AssertionError("(Step 8 FAILED) Query results did not appear")
            print("[PASS] Query results appeared")

            # Step 9: Verify SQL translation is displayed
            print("Step 9: Verifying SQL translation...")

            # Wait a bit more for the SQL to appear
            page.wait_for_timeout(3000)

            # Try multiple approaches to find the SQL
            sql_found = False
            sql_text = ""

            # Try finding code or pre element with SELECT
            try:
                sql_elem = page.locator('code, pre').filter(has_text="SELECT").first
                if sql_elem.is_visible(timeout=5000):
                    sql_text = sql_elem.inner_text()
                    sql_found = True
            except:
                pass

            # If not found, try looking for any element containing SELECT
            if not sql_found:
                try:
                    sql_elem = page.get_by_text("SELECT", exact=False).first
                    if sql_elem.is_visible(timeout=5000):
                        sql_text = sql_elem.inner_text()
                        sql_found = True
                except:
                    pass

            if not sql_found:
                # Take a debug screenshot
                debug_path = SCREENSHOT_DIR / "debug_no_sql.png"
                page.screenshot(path=str(debug_path), full_page=True)
                raise AssertionError(f"(Step 9 FAILED) SQL translation not found. Debug screenshot saved to {debug_path}")

            if "users" not in sql_text.lower():
                raise AssertionError(f"(Step 9 FAILED) SQL translation doesn't reference users table: {sql_text}")
            print(f"[PASS] SQL translation verified: {sql_text}")

            # Step 10: Take screenshot of SQL translation
            print("Step 10: Taking screenshot of SQL translation...")
            screenshot_path = SCREENSHOT_DIR / "03_sql_translation.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            test_result["screenshots"].append(str(screenshot_path))

            # Step 11: Verify results table contains data
            print("Step 11: Verifying results table contains data...")
            results_table = page.locator('table').first

            if not results_table.is_visible(timeout=5000):
                raise AssertionError("(Step 11 FAILED) Results table not found")

            # Check for table rows (at least header + 1 data row)
            rows = page.locator('table tr')
            row_count = rows.count()

            if row_count < 2:
                raise AssertionError(f"(Step 11 FAILED) Results table has insufficient rows: {row_count}")
            print(f"[PASS] Results table verified with {row_count} rows")

            # Step 12: Take screenshot of results
            print("Step 12: Taking screenshot of results...")
            screenshot_path = SCREENSHOT_DIR / "04_results.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            test_result["screenshots"].append(str(screenshot_path))

            # Step 13: Click Hide button
            print("Step 13: Clicking Hide button...")
            hide_button = page.get_by_role("button", name="Hide").or_(
                page.locator('button:has-text("Hide")')
            )

            if hide_button.is_visible(timeout=5000):
                hide_button.click()
                page.wait_for_timeout(1000)
                print("[PASS] Hide button clicked")
            else:
                print("[WARN] Hide button not found (may not be required)")

            # All steps passed
            print("\n[PASS] All test steps completed successfully!")
            test_result["status"] = "passed"

            # Close browser
            browser.close()

    except AssertionError as e:
        test_result["error"] = str(e)
        print(f"\n[FAIL] Test failed: {e}")
    except Exception as e:
        test_result["error"] = f"Unexpected error: {str(e)}"
        print(f"\n[FAIL] Test failed with unexpected error: {e}")

    return test_result

if __name__ == "__main__":
    # Ensure screenshot directory exists
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # Run the test
    result = run_test()

    # Output JSON result
    print("\n" + "="*60)
    print("TEST RESULT:")
    print("="*60)
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["status"] == "passed" else 1)
