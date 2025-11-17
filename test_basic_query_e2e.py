"""
E2E Test: Basic Query Execution
Tests basic query functionality in the Natural Language SQL Interface application.
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

# Configuration
APPLICATION_URL = "http://localhost:5173"
ADW_ID = "1cd3c052"
AGENT_NAME = "e2e_test_runner_0_0"
TEST_NAME = "basic_query"
SCREENSHOT_DIR = Path(f"/c/Users/amogh/Downloads/tac5/tac-5/agents/{ADW_ID}/{AGENT_NAME}/img/{TEST_NAME}")

def run_test():
    """Execute the E2E test for basic query functionality."""
    results = {
        "test_name": "Basic Query Execution",
        "status": "passed",
        "screenshots": [],
        "error": None
    }

    try:
        with sync_playwright() as p:
            # Launch browser in headed mode for visibility
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()

            # Step 1: Navigate to the Application URL
            print(f"Step 1: Navigating to {APPLICATION_URL}...")
            page.goto(APPLICATION_URL, wait_until="networkidle")
            page.wait_for_timeout(2000)  # Allow time for async operations

            # Step 2: Take a screenshot of the initial state
            print("Step 2: Taking screenshot of initial state...")
            screenshot_path = SCREENSHOT_DIR / "01_initial_state.png"
            page.screenshot(path=str(screenshot_path))
            results["screenshots"].append(str(screenshot_path))

            # Step 3: Verify the page title is "Natural Language SQL Interface"
            print("Step 3: Verifying page title...")
            title = page.title()
            if "Natural Language SQL Interface" not in title:
                raise AssertionError(f"(Step 3 X) Expected page title to contain 'Natural Language SQL Interface', got '{title}'")
            print(f"[OK] Page title verified: {title}")

            # Step 4: Verify core UI elements are present
            print("Step 4: Verifying core UI elements...")

            # Check for query input textbox
            query_input = page.locator('textarea[placeholder*="query" i], input[placeholder*="query" i], textarea, input[type="text"]').first
            if not query_input.is_visible():
                raise AssertionError("(Step 4 [FAIL]) Query input textbox not found")
            print("[OK] Query input textbox found")

            # Check for Query button
            query_button = page.get_by_role("button", name="Query").or_(page.locator('button:has-text("Query")')).first
            if not query_button.is_visible():
                raise AssertionError("(Step 4 [FAIL]) Query button not found")
            print("[OK] Query button found")

            # Check for Upload Data button
            upload_button = page.get_by_role("button", name="Upload Data").or_(page.locator('button:has-text("Upload Data")')).first
            if not upload_button.is_visible():
                raise AssertionError("(Step 4 [FAIL]) Upload Data button not found")
            print("[OK] Upload Data button found")

            # Check for Available Tables section
            tables_section = page.locator('text=/Available Tables/i').or_(page.locator('h2:has-text("Available Tables")'))
            if not tables_section.is_visible():
                raise AssertionError("(Step 4 [FAIL]) Available Tables section not found")
            print("[OK] Available Tables section found")

            # Step 5: Enter the query
            print("Step 5: Entering query...")
            query_text = "Show me all users from the users table"
            query_input.fill(query_text)
            page.wait_for_timeout(1000)

            # Step 6: Take a screenshot of the query input
            print("Step 6: Taking screenshot of query input...")
            screenshot_path = SCREENSHOT_DIR / "02_query_input.png"
            page.screenshot(path=str(screenshot_path))
            results["screenshots"].append(str(screenshot_path))

            # Step 7: Click the Query button
            print("Step 7: Clicking Query button...")
            query_button.click()

            # Wait for results to appear (with timeout)
            print("Waiting for query results...")
            page.wait_for_timeout(8000)  # Allow time for API call and rendering

            # Debug: Take a screenshot to see current state
            debug_screenshot = SCREENSHOT_DIR / "debug_after_query.png"
            page.screenshot(path=str(debug_screenshot))
            print(f"Debug screenshot saved: {debug_screenshot}")

            # Step 8: Verify the query results appear
            print("Step 8: Verifying query results appear...")
            # Look for results container or any indication of results
            try:
                # Check each locator individually for better debugging
                text_results = page.locator('text=/Results/i').first
                table_elem = page.locator('table').first
                results_section = page.locator('#results-section').first

                print(f"  - text=/Results/i visible: {text_results.is_visible() if text_results.count() > 0 else False}")
                print(f"  - table visible: {table_elem.is_visible() if table_elem.count() > 0 else False}")
                print(f"  - #results-section visible: {results_section.is_visible() if results_section.count() > 0 else False}")

                results_visible = (
                    (text_results.count() > 0 and text_results.is_visible()) or
                    (table_elem.count() > 0 and table_elem.is_visible()) or
                    (results_section.count() > 0 and results_section.is_visible())
                )
            except Exception as e:
                print(f"  - Error checking visibility: {e}")
                results_visible = False

            if not results_visible:
                # Check for error messages
                error_elem = page.locator('text=/error/i').first
                if error_elem.count() > 0 and error_elem.is_visible():
                    error_text = error_elem.text_content()
                    raise AssertionError(f"(Step 8 [FAIL]) Query returned an error: {error_text}")
                raise AssertionError("(Step 8 [FAIL]) Query results did not appear")
            print("[OK] Query results appeared")

            # Step 9: Verify the SQL translation is displayed
            print("Step 9: Verifying SQL translation...")
            page_content = page.content()
            sql_visible = (
                "SELECT" in page_content.upper() and
                "FROM" in page_content.upper() and
                "users" in page_content.lower()
            )
            if not sql_visible:
                raise AssertionError("(Step 9 [FAIL]) SQL translation not found or does not contain expected SELECT FROM users")
            print("[OK] SQL translation verified")

            # Step 10: Take a screenshot of the SQL translation
            print("Step 10: Taking screenshot of SQL translation...")
            screenshot_path = SCREENSHOT_DIR / "03_sql_translation.png"
            page.screenshot(path=str(screenshot_path))
            results["screenshots"].append(str(screenshot_path))

            # Step 11: Verify the results table contains data
            print("Step 11: Verifying results table contains data...")
            table = page.locator('table').first
            if table.is_visible():
                rows = table.locator('tr').count()
                if rows <= 1:  # Only header row
                    raise AssertionError("(Step 11 [FAIL]) Results table appears empty (only header row)")
                print(f"[OK] Results table contains {rows} rows (including header)")
            else:
                raise AssertionError("(Step 11 [FAIL]) Results table not visible")

            # Step 12: Take a screenshot of the results
            print("Step 12: Taking screenshot of results...")
            screenshot_path = SCREENSHOT_DIR / "04_results.png"
            page.screenshot(path=str(screenshot_path))
            results["screenshots"].append(str(screenshot_path))

            # Step 13: Click "Hide" button to close results
            print("Step 13: Clicking Hide button...")
            hide_button = page.get_by_role("button", name="Hide").or_(page.locator('button:has-text("Hide")')).first
            if hide_button.is_visible():
                hide_button.click()
                page.wait_for_timeout(1000)
                print("[OK] Hide button clicked")
            else:
                print("[WARN] Hide button not found (may not be critical)")

            print("\n[SUCCESS] All test steps completed successfully!")

            # Close browser
            browser.close()

    except AssertionError as e:
        results["status"] = "failed"
        results["error"] = str(e)
        print(f"\n[FAIL] Test failed: {e}")
        if 'browser' in locals():
            try:
                browser.close()
            except:
                pass
    except Exception as e:
        results["status"] = "failed"
        results["error"] = f"Unexpected error: {str(e)}"
        print(f"\n[FAIL] Unexpected error: {e}")
        if 'browser' in locals():
            try:
                browser.close()
            except:
                pass

    return results

if __name__ == "__main__":
    # Ensure screenshot directory exists
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # Run the test
    test_results = run_test()

    # Output results as JSON
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(json.dumps(test_results, indent=2))

    # Exit with appropriate code
    sys.exit(0 if test_results["status"] == "passed" else 1)
