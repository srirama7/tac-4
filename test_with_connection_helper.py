#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E2E Test with Brute Force Connection Helper
"""

import json
import os
import sys
from playwright.sync_api import sync_playwright
from playwright_connection_helper import (
    wait_for_server,
    goto_with_retry,
    ensure_element_visible,
    click_with_retry,
    wait_for_network_idle
)

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Test configuration
APP_URL = "http://localhost:5173"
SCREENSHOT_DIR = "test_screenshots"

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def run_test():
    """Execute the E2E test with brute force connection"""
    test_result = {
        "test_name": "Connection Test with Retries",
        "status": "passed",
        "screenshots": [],
        "error": None
    }

    try:
        # Step 1: Brute force wait for server to be available
        print("="*60)
        print("STEP 1: Waiting for server to be available...")
        print("="*60)
        if not wait_for_server(APP_URL, max_attempts=30, delay=1.0):
            raise Exception("Server is not available after 30 attempts")

        with sync_playwright() as p:
            # Launch browser
            print("\n" + "="*60)
            print("STEP 2: Launching browser...")
            print("="*60)
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()

            # Step 3: Navigate with retry
            print("\n" + "="*60)
            print(f"STEP 3: Navigating to {APP_URL} with retry logic...")
            print("="*60)
            if not goto_with_retry(page, APP_URL, max_attempts=5, timeout=30000):
                raise Exception("Failed to navigate to application")

            # Step 4: Wait for network idle with retry
            print("\n" + "="*60)
            print("STEP 4: Waiting for network to be idle...")
            print("="*60)
            if not wait_for_network_idle(page, timeout=30000, max_attempts=3):
                print("⚠ Warning: Network did not become idle, continuing anyway...")

            # Step 5: Take screenshot
            print("\n" + "="*60)
            print("STEP 5: Taking screenshot of initial state...")
            print("="*60)
            screenshot_path = os.path.join(SCREENSHOT_DIR, "01_initial_state.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Step 6: Ensure query input is visible with retry
            print("\n" + "="*60)
            print("STEP 6: Waiting for query input to be visible...")
            print("="*60)
            if not ensure_element_visible(page, '#query-input', timeout=10000, retries=3):
                raise Exception("Query input not found")
            print("✓ Query input is visible")

            # Step 7: Ensure query button is visible with retry
            print("\n" + "="*60)
            print("STEP 7: Waiting for query button to be visible...")
            print("="*60)
            if not ensure_element_visible(page, '#query-button', timeout=10000, retries=3):
                raise Exception("Query button not found")
            print("✓ Query button is visible")

            # Step 8: Fill query input
            print("\n" + "="*60)
            print("STEP 8: Filling query input...")
            print("="*60)
            query_input = page.locator('#query-input')
            query_text = "Show me all users from the users table"
            query_input.fill(query_text)
            print(f"✓ Query entered: {query_text}")

            # Step 9: Click query button with retry
            print("\n" + "="*60)
            print("STEP 9: Clicking query button with retry logic...")
            print("="*60)
            if not click_with_retry(page, '#query-button', max_attempts=3, delay=0.5):
                raise Exception("Failed to click query button")

            # Step 10: Wait for results with retry
            print("\n" + "="*60)
            print("STEP 10: Waiting for results section to appear...")
            print("="*60)
            if not ensure_element_visible(page, '#results-section', timeout=20000, retries=3):
                # Check for error messages
                error_messages = page.locator('.error-message')
                if error_messages.count() > 0:
                    error_text = error_messages.first.inner_text()
                    raise Exception(f"Error shown: {error_text}")
                raise Exception("Results section did not appear")
            print("✓ Results section appeared")

            # Step 11: Take final screenshot
            print("\n" + "="*60)
            print("STEP 11: Taking final screenshot...")
            print("="*60)
            screenshot_path = os.path.join(SCREENSHOT_DIR, "02_final_state.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Close browser
            browser.close()

            print("\n" + "="*60)
            print("✓ ALL TEST STEPS COMPLETED SUCCESSFULLY!")
            print("="*60)

    except Exception as e:
        test_result["status"] = "failed"
        test_result["error"] = str(e)
        print(f"\n✗ Test failed: {e}")
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
