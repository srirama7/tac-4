"""E2E test for basic query functionality using Playwright"""
import json
import sys
from playwright.sync_api import sync_playwright, expect
import time

def run_test():
    """Execute the E2E test"""

    # Test configuration
    app_url = "http://localhost:5175"
    screenshot_dir = "/c/Users/amogh/Downloads/tac5/tac-5/agents/befa7885/e2e_test_runner_1_0/img/basic_query"

    results = {
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

            # Step 1: Navigate to the Application URL
            print("Step 1: Navigating to application...")
            page.goto(app_url, wait_until="networkidle", timeout=30000)
            time.sleep(2)

            # Step 2: Take a screenshot of the initial state
            print("Step 2: Taking screenshot of initial state...")
            screenshot_path = f"{screenshot_dir}/01_initial_state.png"
            page.screenshot(path=screenshot_path)
            results["screenshots"].append(screenshot_path)

            # Step 3: Verify the page title
            print("Step 3: Verifying page title...")
            title = page.title()
            if title != "Natural Language SQL Interface":
                raise AssertionError(f"(Step 3 ❌) Expected title 'Natural Language SQL Interface', got '{title}'")

            # Step 4: Verify core UI elements are present
            print("Step 4: Verifying core UI elements...")

            # Try multiple possible selectors for query input
            query_input = None
            input_selectors = [
                'textarea[placeholder*="query"]',
                'textarea',
                'input[type="text"]',
                '#query-input',
                '[data-testid="query-input"]'
            ]

            for selector in input_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        query_input = element
                        print(f"  ✓ Found query input with selector: {selector}")
                        break
                except:
                    continue

            if not query_input:
                raise AssertionError("(Step 4 ❌) Failed to find query input textbox")

            # Try multiple possible selectors for query button
            query_button = None
            button_selectors = [
                'button:has-text("Query")',
                'button:has-text("Submit")',
                'button[type="submit"]',
                '#query-button',
                '[data-testid="query-button"]'
            ]

            for selector in button_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        query_button = element
                        print(f"  ✓ Found query button with selector: {selector}")
                        break
                except:
                    continue

            if not query_button:
                raise AssertionError("(Step 4 ❌) Failed to find Query button")

            # Try multiple possible selectors for upload button
            upload_button = None
            upload_selectors = [
                'button:has-text("Upload Data")',
                'button:has-text("Upload")',
                '#upload-button',
                '[data-testid="upload-button"]'
            ]

            for selector in upload_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        upload_button = element
                        print(f"  ✓ Found upload button with selector: {selector}")
                        break
                except:
                    continue

            if not upload_button:
                raise AssertionError("(Step 4 ❌) Failed to find Upload Data button")

            # Check for Available Tables section
            tables_section = None
            table_selectors = [
                ':has-text("Available Tables")',
                ':has-text("Tables")',
                '#tables-section',
                '[data-testid="tables-section"]'
            ]

            for selector in table_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        tables_section = element
                        print(f"  ✓ Found tables section with selector: {selector}")
                        break
                except:
                    continue

            if not tables_section:
                raise AssertionError("(Step 4 ❌) Failed to find Available Tables section")

            # Step 5: Enter the query
            print("Step 5: Entering query...")
            query_input.fill("Show me all users from the users table")
            time.sleep(1)

            # Step 6: Take a screenshot of the query input
            print("Step 6: Taking screenshot of query input...")
            screenshot_path = f"{screenshot_dir}/02_query_input.png"
            page.screenshot(path=screenshot_path)
            results["screenshots"].append(screenshot_path)

            # Step 7: Click the Query button
            print("Step 7: Clicking Query button...")
            query_button.click()

            # Wait for results to appear
            time.sleep(5)

            # Step 8: Verify the query results appear
            print("Step 8: Verifying query results appear...")
            results_selectors = [
                ':has-text("Results")',
                ':has-text("Query Results")',
                '.results',
                '#results',
                '[data-testid="results"]'
            ]

            results_found = False
            for selector in results_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        results_found = True
                        print(f"  ✓ Found results with selector: {selector}")
                        break
                except:
                    continue

            if not results_found:
                raise AssertionError("(Step 8 ❌) Query results did not appear")

            # Step 9: Verify the SQL translation is displayed
            print("Step 9: Verifying SQL translation...")
            sql_selectors = [
                ':has-text("SELECT")',
                ':has-text("FROM users")',
                '.sql-translation',
                '#sql-translation',
                '[data-testid="sql-translation"]'
            ]

            sql_found = False
            for selector in sql_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        text = element.text_content()
                        if "SELECT" in text and "users" in text:
                            sql_found = True
                            print(f"  ✓ Found SQL translation: {text[:100]}")
                            break
                except:
                    continue

            if not sql_found:
                raise AssertionError("(Step 9 ❌) SQL translation not displayed or doesn't contain 'SELECT * FROM users'")

            # Step 10: Take a screenshot of the SQL translation
            print("Step 10: Taking screenshot of SQL translation...")
            screenshot_path = f"{screenshot_dir}/03_sql_translation.png"
            page.screenshot(path=screenshot_path)
            results["screenshots"].append(screenshot_path)

            # Step 11: Verify the results table contains data
            print("Step 11: Verifying results table contains data...")
            table_selectors = [
                'table',
                '.results-table',
                '#results-table',
                '[data-testid="results-table"]'
            ]

            table_found = False
            for selector in table_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        # Check if table has rows
                        rows = page.locator(f"{selector} tr").count()
                        if rows > 0:
                            table_found = True
                            print(f"  ✓ Found results table with {rows} rows")
                            break
                except:
                    continue

            if not table_found:
                raise AssertionError("(Step 11 ❌) Results table does not contain data")

            # Step 12: Take a screenshot of the results
            print("Step 12: Taking screenshot of results...")
            screenshot_path = f"{screenshot_dir}/04_results.png"
            page.screenshot(path=screenshot_path)
            results["screenshots"].append(screenshot_path)

            # Step 13: Click "Hide" button to close results
            print("Step 13: Clicking Hide button...")
            hide_selectors = [
                'button:has-text("Hide")',
                'button:has-text("Close")',
                '#hide-button',
                '[data-testid="hide-button"]'
            ]

            hide_found = False
            for selector in hide_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        element.click()
                        hide_found = True
                        print(f"  ✓ Clicked hide button with selector: {selector}")
                        break
                except:
                    continue

            if not hide_found:
                raise AssertionError("(Step 13 ❌) Failed to find or click Hide button")

            time.sleep(2)

            # Close browser
            browser.close()

            print("\n✅ Test PASSED - All steps completed successfully!")

    except Exception as e:
        results["status"] = "failed"
        results["error"] = str(e)
        print(f"\n❌ Test FAILED: {e}")
        if 'browser' in locals():
            browser.close()

    # Output results as JSON
    print("\n" + "="*80)
    print(json.dumps(results, indent=2))
    print("="*80)

    return results

if __name__ == "__main__":
    result = run_test()
    sys.exit(0 if result["status"] == "passed" else 1)
