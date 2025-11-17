#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright Connection Helper - Brute force connection with retries
"""

import time
import sys
import requests
from playwright.sync_api import Page, Browser, BrowserContext

def wait_for_server(url: str, max_attempts: int = 30, delay: float = 1.0) -> bool:
    """
    Brute force connection to server with retries

    Args:
        url: The URL to connect to
        max_attempts: Maximum number of connection attempts
        delay: Delay between attempts in seconds

    Returns:
        True if connection successful, False otherwise
    """
    print(f"Attempting to connect to {url}...")

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✓ Connected successfully on attempt {attempt}")
                return True
        except requests.exceptions.RequestException as e:
            if attempt < max_attempts:
                print(f"Attempt {attempt}/{max_attempts} failed: {str(e)[:50]}... Retrying in {delay}s")
                time.sleep(delay)
            else:
                print(f"✗ All {max_attempts} connection attempts failed")
                return False

    return False


def goto_with_retry(page: Page, url: str, max_attempts: int = 5, timeout: int = 30000) -> bool:
    """
    Navigate to URL with retry logic

    Args:
        page: Playwright page object
        url: The URL to navigate to
        max_attempts: Maximum number of attempts
        timeout: Timeout for each attempt in milliseconds

    Returns:
        True if navigation successful, False otherwise
    """
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Navigation attempt {attempt}/{max_attempts} to {url}")
            page.goto(url, wait_until='networkidle', timeout=timeout)
            print(f"✓ Navigation successful on attempt {attempt}")
            return True
        except Exception as e:
            if attempt < max_attempts:
                print(f"Navigation attempt {attempt} failed: {str(e)[:100]}... Retrying")
                time.sleep(2)
            else:
                print(f"✗ All {max_attempts} navigation attempts failed")
                return False

    return False


def ensure_element_visible(page: Page, selector: str, timeout: int = 10000, retries: int = 3) -> bool:
    """
    Ensure element is visible with retry logic

    Args:
        page: Playwright page object
        selector: CSS selector or locator string
        timeout: Timeout for each attempt in milliseconds
        retries: Number of retries

    Returns:
        True if element becomes visible, False otherwise
    """
    for attempt in range(1, retries + 1):
        try:
            element = page.locator(selector)
            element.wait_for(state='visible', timeout=timeout)
            return True
        except Exception as e:
            if attempt < retries:
                print(f"Element '{selector}' not visible (attempt {attempt}/{retries}), retrying...")
                time.sleep(1)
            else:
                print(f"✗ Element '{selector}' failed to appear after {retries} attempts")
                return False

    return False


def click_with_retry(page: Page, selector: str, max_attempts: int = 3, delay: float = 0.5) -> bool:
    """
    Click element with retry logic

    Args:
        page: Playwright page object
        selector: CSS selector or locator string
        max_attempts: Maximum number of click attempts
        delay: Delay between attempts

    Returns:
        True if click successful, False otherwise
    """
    for attempt in range(1, max_attempts + 1):
        try:
            element = page.locator(selector)
            element.click(timeout=5000)
            print(f"✓ Clicked '{selector}' on attempt {attempt}")
            return True
        except Exception as e:
            if attempt < max_attempts:
                print(f"Click attempt {attempt} failed: {str(e)[:50]}... Retrying")
                time.sleep(delay)
            else:
                print(f"✗ Failed to click '{selector}' after {max_attempts} attempts")
                return False

    return False


def wait_for_network_idle(page: Page, timeout: int = 30000, max_attempts: int = 3) -> bool:
    """
    Wait for network to be idle with retry logic

    Args:
        page: Playwright page object
        timeout: Timeout in milliseconds
        max_attempts: Maximum number of attempts

    Returns:
        True if network became idle, False otherwise
    """
    for attempt in range(1, max_attempts + 1):
        try:
            page.wait_for_load_state('networkidle', timeout=timeout)
            print(f"✓ Network idle on attempt {attempt}")
            return True
        except Exception as e:
            if attempt < max_attempts:
                print(f"Network idle wait failed (attempt {attempt}): {str(e)[:50]}...")
                time.sleep(1)
            else:
                print(f"✗ Network did not become idle after {max_attempts} attempts")
                return False

    return False
