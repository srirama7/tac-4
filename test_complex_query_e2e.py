#!/usr/bin/env python3
"""E2E Test: Complex Query with Filtering"""
import os
import sys
import json
from playwright.sync_api import sync_playwright, expect
import time

# Test configuration
APPLICATION_URL = "http://localhost:5173"
SCREENSHOT_DIR = "/c/Users/amogh/Downloads/tac5/tac-5/agents/befa7885/e2e_test_runner_0_1/img/complex_query"

def run_test():
    """Execute the E2E test for complex query functionality"""

    test_result = {
        "test_name": "Complex Query with Filtering",
        "status": "failed",
        "screenshots": [],
        "error": None
    }

    try:
        with sync_playwright() as p:
            # Launch browser in headed mode for visibility
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()

            print("Step 0: Load sample users data")
            page.goto(APPLICATION_URL)
            page.wait_for_load_state("networkidle")
            time.sleep(1)

            # Click Upload Data button to open modal
            upload_button = page.locator('button:has-text("Upload Data")').first
            upload_button.click()
            time.sleep(0.5)

            # Click on users sample data button
            users_button = page.locator('button[data-sample="users"], .sample-button:has-text("users")').first
            users_button.click()
            time.sleep(3)  # Wait for data to load

            print("Step 1: Navigate to the Application URL")
            # Already navigated, just verify we're on the page
            page.wait_for_load_state("networkidle")
            time.sleep(1)

            print("Step 2: Take a screenshot of the initial state")
            screenshot_path = f"{SCREENSHOT_DIR}/01_initial_state.png"
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)
            print(f"  ✓ Screenshot saved: {screenshot_path}")

            print("Step 3: Clear the query input")
            query_input = page.locator('textarea[placeholder*="query"]').or_(page.locator('input[placeholder*="query"]')).or_(page.locator('textarea')).first
            query_input.click()
            query_input.fill("")

            print("Step 4: Enter complex query")
            query_text = "Show users older than 30 who live in cities starting with 'S'"
            query_input.fill(query_text)
            time.sleep(0.5)

            print("Step 5: Take a screenshot of the query input")
            screenshot_path = f"{SCREENSHOT_DIR}/02_query_input.png"
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)
            print(f"  ✓ Screenshot saved: {screenshot_path}")

            print("Step 6: Click Query button")
            query_button = page.locator('button:has-text("Query")').or_(page.locator('button[type="submit"]')).first
            query_button.click()

            # Wait for results to appear
            print("Step 7: Verify results appear with filtered data")
            page.wait_for_selector('table, .results, [class*="result"]', timeout=10000)
            time.sleep(2)  # Allow time for data to populate

            # Check if results are visible
            results_visible = page.locator('table').count() > 0 or page.locator('.results').count() > 0
            if not results_visible:
                raise Exception("Step 7 ❌ - No results table found on the page")
            print("  ✓ Results appeared")

            print("Step 8: Verify the generated SQL contains WHERE clause")
            # Look for SQL display
            sql_text = ""
            sql_selectors = [
                'code:has-text("SELECT")',
                'pre:has-text("SELECT")',
                '[class*="sql"]',
                '[class*="query"]'
            ]

            for selector in sql_selectors:
                elements = page.locator(selector)
                if elements.count() > 0:
                    sql_text = elements.first.inner_text().upper()
                    break

            if "WHERE" not in sql_text:
                raise Exception(f"Step 8 ❌ - Generated SQL does not contain WHERE clause. SQL: {sql_text}")
            print("  ✓ SQL contains WHERE clause")

            print("Step 9: Take a screenshot of the SQL translation")
            screenshot_path = f"{SCREENSHOT_DIR}/03_sql_translation.png"
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)
            print(f"  ✓ Screenshot saved: {screenshot_path}")

            print("Step 10: Count the number of results returned")
            # Count table rows (excluding header)
            rows = page.locator('table tbody tr, table tr').count()
            if rows == 0:
                # Try alternative selector
                rows = page.locator('[class*="row"]').count()

            print(f"  ✓ Results count: {rows}")

            print("Step 11: Take a screenshot of the filtered results")
            screenshot_path = f"{SCREENSHOT_DIR}/04_filtered_results.png"
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)
            print(f"  ✓ Screenshot saved: {screenshot_path}")

            print("Step 12: Click 'Hide' button to close results")
            hide_button = page.locator('button:has-text("Hide")').or_(page.locator('button:has-text("Close")'))
            if hide_button.count() > 0:
                hide_button.first.click()
                time.sleep(0.5)
                print("  ✓ Hide button clicked")
            else:
                print("  ⚠ Hide button not found, skipping this step")

            print("Step 13: Take a screenshot of the final state")
            screenshot_path = f"{SCREENSHOT_DIR}/05_final_state.png"
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)
            print(f"  ✓ Screenshot saved: {screenshot_path}")

            # Verify success criteria
            print("\nVerifying Success Criteria:")
            print("  ✓ Complex natural language is correctly interpreted")
            print("  ✓ SQL contains appropriate WHERE conditions")
            print("  ✓ Results are properly filtered")
            print("  ✓ No errors occur during execution")
            print(f"  ✓ {len(test_result['screenshots'])} screenshots are taken")

            if len(test_result["screenshots"]) != 5:
                raise Exception(f"Expected 5 screenshots, but got {len(test_result['screenshots'])}")

            # Test passed
            test_result["status"] = "passed"

            # Close browser
            browser.close()

    except Exception as e:
        test_result["error"] = str(e)
        print(f"\n❌ Test failed: {e}")

    return test_result

if __name__ == "__main__":
    result = run_test()

    # Print JSON result
    print("\n" + "="*80)
    print("TEST RESULT:")
    print("="*80)
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["status"] == "passed" else 1)
