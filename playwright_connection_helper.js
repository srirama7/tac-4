/**
 * Playwright Connection Helper - Brute force connection with retries
 */

const http = require('http');

/**
 * Wait for server to be available with retries
 * @param {string} url - The URL to connect to
 * @param {number} maxAttempts - Maximum number of connection attempts
 * @param {number} delay - Delay between attempts in milliseconds
 * @returns {Promise<boolean>} True if connection successful
 */
async function waitForServer(url, maxAttempts = 30, delay = 1000) {
  console.log(`Attempting to connect to ${url}...`);

  const urlObj = new URL(url);

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      await new Promise((resolve, reject) => {
        const req = http.get({
          hostname: urlObj.hostname,
          port: urlObj.port,
          path: urlObj.pathname,
          timeout: 5000
        }, (res) => {
          if (res.statusCode === 200 || res.statusCode === 304) {
            resolve(true);
          } else {
            reject(new Error(`Status ${res.statusCode}`));
          }
        });

        req.on('error', reject);
        req.on('timeout', () => {
          req.destroy();
          reject(new Error('Request timeout'));
        });
      });

      console.log(`✓ Connected successfully on attempt ${attempt}`);
      return true;

    } catch (error) {
      if (attempt < maxAttempts) {
        console.log(`Attempt ${attempt}/${maxAttempts} failed: ${error.message.substring(0, 50)}... Retrying in ${delay/1000}s`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        console.log(`✗ All ${maxAttempts} connection attempts failed`);
        return false;
      }
    }
  }

  return false;
}

/**
 * Navigate to URL with retry logic
 * @param {import('playwright').Page} page - Playwright page object
 * @param {string} url - The URL to navigate to
 * @param {number} maxAttempts - Maximum number of attempts
 * @param {number} timeout - Timeout for each attempt in milliseconds
 * @returns {Promise<boolean>} True if navigation successful
 */
async function gotoWithRetry(page, url, maxAttempts = 5, timeout = 30000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      console.log(`Navigation attempt ${attempt}/${maxAttempts} to ${url}`);
      await page.goto(url, { waitUntil: 'networkidle', timeout });
      console.log(`✓ Navigation successful on attempt ${attempt}`);
      return true;
    } catch (error) {
      if (attempt < maxAttempts) {
        console.log(`Navigation attempt ${attempt} failed: ${error.message.substring(0, 100)}... Retrying`);
        await new Promise(resolve => setTimeout(resolve, 2000));
      } else {
        console.log(`✗ All ${maxAttempts} navigation attempts failed`);
        return false;
      }
    }
  }

  return false;
}

/**
 * Ensure element is visible with retry logic
 * @param {import('playwright').Page} page - Playwright page object
 * @param {string} selector - CSS selector
 * @param {number} timeout - Timeout for each attempt in milliseconds
 * @param {number} retries - Number of retries
 * @returns {Promise<boolean>} True if element becomes visible
 */
async function ensureElementVisible(page, selector, timeout = 10000, retries = 3) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      await page.locator(selector).waitFor({ state: 'visible', timeout });
      return true;
    } catch (error) {
      if (attempt < retries) {
        console.log(`Element '${selector}' not visible (attempt ${attempt}/${retries}), retrying...`);
        await new Promise(resolve => setTimeout(resolve, 1000));
      } else {
        console.log(`✗ Element '${selector}' failed to appear after ${retries} attempts`);
        return false;
      }
    }
  }

  return false;
}

/**
 * Click element with retry logic
 * @param {import('playwright').Page} page - Playwright page object
 * @param {string} selector - CSS selector
 * @param {number} maxAttempts - Maximum number of click attempts
 * @param {number} delay - Delay between attempts in milliseconds
 * @returns {Promise<boolean>} True if click successful
 */
async function clickWithRetry(page, selector, maxAttempts = 3, delay = 500) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      await page.locator(selector).click({ timeout: 5000 });
      console.log(`✓ Clicked '${selector}' on attempt ${attempt}`);
      return true;
    } catch (error) {
      if (attempt < maxAttempts) {
        console.log(`Click attempt ${attempt} failed: ${error.message.substring(0, 50)}... Retrying`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        console.log(`✗ Failed to click '${selector}' after ${maxAttempts} attempts`);
        return false;
      }
    }
  }

  return false;
}

/**
 * Wait for network to be idle with retry logic
 * @param {import('playwright').Page} page - Playwright page object
 * @param {number} timeout - Timeout in milliseconds
 * @param {number} maxAttempts - Maximum number of attempts
 * @returns {Promise<boolean>} True if network became idle
 */
async function waitForNetworkIdle(page, timeout = 30000, maxAttempts = 3) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      await page.waitForLoadState('networkidle', { timeout });
      console.log(`✓ Network idle on attempt ${attempt}`);
      return true;
    } catch (error) {
      if (attempt < maxAttempts) {
        console.log(`Network idle wait failed (attempt ${attempt}): ${error.message.substring(0, 50)}...`);
        await new Promise(resolve => setTimeout(resolve, 1000));
      } else {
        console.log(`✗ Network did not become idle after ${maxAttempts} attempts`);
        return false;
      }
    }
  }

  return false;
}

module.exports = {
  waitForServer,
  gotoWithRetry,
  ensureElementVisible,
  clickWithRetry,
  waitForNetworkIdle
};
