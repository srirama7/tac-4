"""E2E Test: Basic Query Execution using Playwright"""
import json
import os
from playwright.sync_api import sync_playwright, expect
import time

def run_test():
    # Configuration
    adw_id = "073ed71b"
    agent_name = "e2e_test_runner_1_0"
    application_url = "http://localhost:5173"
    codebase_path = os.getcwd()
    screenshot_dir = os.path.join(codebase_path, "agents", adw_id, agent_name, "img", "basic_query")
    os.makedirs(screenshot_dir, exist_ok=True)
    
    result = {"test_name": "Basic Query Execution", "status": "passed", "screenshots": [], "error": None}
    screenshots = []
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            print("Step 1: Navigating to " + application_url)
            page.goto(application_url, wait_until="networkidle")
            time.sleep(3)
            
            print("Step 2: Taking screenshot")
            sp = os.path.join(screenshot_dir, "01_initial_state.png")
            page.screenshot(path=sp)
            screenshots.append(sp)
            
            print("Step 3: Verifying page title")
            expect(page).to_have_title("Natural Language SQL Interface")
            
            print("Step 4: Verifying UI elements")
            expect(page.locator("#query-input")).to_be_visible()
            expect(page.locator("#query-button")).to_be_visible()
            expect(page.locator("#upload-data-button")).to_be_visible()
            expect(page.locator("text=Available Tables")).to_be_visible()
            
            print("Step 5: Entering query")
            page.locator("#query-input").fill("Show me all users from the users table")
            time.sleep(1)
            
            print("Step 6: Screenshot query input")
            sp = os.path.join(screenshot_dir, "02_query_input.png")
            page.screenshot(path=sp)
            screenshots.append(sp)
            
            print("Step 7: Clicking Query button")
            page.locator("#query-button").click()
            time.sleep(10)
            
            print("Step 8: Verifying results")
            expect(page.locator("#results-section")).to_be_visible(timeout=20000)
            
            print("Step 9: Verifying SQL")
            sql_display = page.locator("#sql-display")
            expect(sql_display).to_be_visible(timeout=10000)
            time.sleep(2)
            sql_text = sql_display.inner_text()
            
            if not sql_text or "SELECT" not in sql_text.upper():
                sp = os.path.join(screenshot_dir, "99_error.png")
                page.screenshot(path=sp)
                screenshots.append(sp)
                result["status"] = "failed"
                result["error"] = "Step 9 FAILED: SQL is empty or missing SELECT"
                result["screenshots"] = screenshots
                browser.close()
                return result
            
            print("Step 10: Screenshot SQL")
            sp = os.path.join(screenshot_dir, "03_sql_translation.png")
            page.screenshot(path=sp)
            screenshots.append(sp)
            
            print("Step 11: Verifying table data")
            expect(page.locator("table.results-table")).to_be_visible(timeout=5000)
            rows = page.locator("table.results-table tbody tr").count()
            if rows < 1:
                result["status"] = "failed"
                result["error"] = f"Step 11 FAILED: No data rows ({rows})"
                result["screenshots"] = screenshots
                browser.close()
                return result
            
            print("Step 12: Screenshot results")
            sp = os.path.join(screenshot_dir, "04_results.png")
            page.screenshot(path=sp)
            screenshots.append(sp)
            
            print("Step 13: Clicking Hide")
            expect(page.locator("#toggle-results")).to_be_visible(timeout=5000)
            page.locator("#toggle-results").click()
            time.sleep(1)
            
            print("ALL TESTS PASSED")
            result["status"] = "passed"
            result["screenshots"] = screenshots
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = f"Error: {str(e)}"
            result["screenshots"] = screenshots
            try:
                sp = os.path.join(screenshot_dir, "99_error.png")
                page.screenshot(path=sp)
                screenshots.append(sp)
            except:
                pass
        finally:
            time.sleep(2)
            browser.close()
    
    return result

if __name__ == "__main__":
    result = run_test()
    print("=" * 60)
    print("TEST REPORT")
    print("=" * 60)
    print(json.dumps(result, indent=2))
    print("=" * 60)
