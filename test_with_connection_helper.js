/**
 * E2E Test with Brute Force Connection Helper
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const {
  waitForServer,
  gotoWithRetry,
  ensureElementVisible,
  clickWithRetry,
  waitForNetworkIdle
} = require('./playwright_connection_helper');

const APP_URL = 'http://localhost:5173';
const SCREENSHOT_DIR = 'test_screenshots';

// Ensure screenshot directory exists
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

const testResult = {
  test_name: "Connection Test with Retries",
  status: "passed",
  screenshots: [],
  error: null
};

async function runTest() {
  let browser, context, page;

  try {
    // Step 1: Brute force wait for server to be available
    console.log('='.repeat(60));
    console.log('STEP 1: Waiting for server to be available...');
    console.log('='.repeat(60));
    const serverAvailable = await waitForServer(APP_URL, 30, 1000);
    if (!serverAvailable) {
      throw new Error('Server is not available after 30 attempts');
    }

    // Step 2: Launch browser
    console.log('\n' + '='.repeat(60));
    console.log('STEP 2: Launching browser...');
    console.log('='.repeat(60));
    browser = await chromium.launch({ headless: false });
    context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    page = await context.newPage();

    // Step 3: Navigate with retry
    console.log('\n' + '='.repeat(60));
    console.log(`STEP 3: Navigating to ${APP_URL} with retry logic...`);
    console.log('='.repeat(60));
    const navigated = await gotoWithRetry(page, APP_URL, 5, 30000);
    if (!navigated) {
      throw new Error('Failed to navigate to application');
    }

    // Step 4: Wait for network idle with retry
    console.log('\n' + '='.repeat(60));
    console.log('STEP 4: Waiting for network to be idle...');
    console.log('='.repeat(60));
    const networkIdle = await waitForNetworkIdle(page, 30000, 3);
    if (!networkIdle) {
      console.log('⚠ Warning: Network did not become idle, continuing anyway...');
    }

    // Step 5: Take screenshot
    console.log('\n' + '='.repeat(60));
    console.log('STEP 5: Taking screenshot of initial state...');
    console.log('='.repeat(60));
    const screenshot1 = path.join(SCREENSHOT_DIR, '01_initial_state.png');
    await page.screenshot({ path: screenshot1 });
    testResult.screenshots.push(screenshot1);
    console.log(`✓ Screenshot saved: ${screenshot1}`);

    // Step 6: Ensure query input is visible with retry
    console.log('\n' + '='.repeat(60));
    console.log('STEP 6: Waiting for query input to be visible...');
    console.log('='.repeat(60));
    const queryInputVisible = await ensureElementVisible(page, '#query-input', 10000, 3);
    if (!queryInputVisible) {
      throw new Error('Query input not found');
    }
    console.log('✓ Query input is visible');

    // Step 7: Ensure query button is visible with retry
    console.log('\n' + '='.repeat(60));
    console.log('STEP 7: Waiting for query button to be visible...');
    console.log('='.repeat(60));
    const queryButtonVisible = await ensureElementVisible(page, '#query-button', 10000, 3);
    if (!queryButtonVisible) {
      throw new Error('Query button not found');
    }
    console.log('✓ Query button is visible');

    // Step 8: Fill query input
    console.log('\n' + '='.repeat(60));
    console.log('STEP 8: Filling query input...');
    console.log('='.repeat(60));
    const queryInput = page.locator('#query-input');
    const queryText = 'Show me all users from the users table';
    await queryInput.fill(queryText);
    console.log(`✓ Query entered: ${queryText}`);

    // Step 9: Click query button with retry
    console.log('\n' + '='.repeat(60));
    console.log('STEP 9: Clicking query button with retry logic...');
    console.log('='.repeat(60));
    const clicked = await clickWithRetry(page, '#query-button', 3, 500);
    if (!clicked) {
      throw new Error('Failed to click query button');
    }

    // Step 10: Wait for results with retry
    console.log('\n' + '='.repeat(60));
    console.log('STEP 10: Waiting for results section to appear...');
    console.log('='.repeat(60));
    const resultsVisible = await ensureElementVisible(page, '#results-section', 20000, 3);
    if (!resultsVisible) {
      // Check for error messages
      const errorMessages = page.locator('.error-message');
      const errorCount = await errorMessages.count();
      if (errorCount > 0) {
        const errorText = await errorMessages.first().textContent();
        throw new Error(`Error shown: ${errorText}`);
      }
      throw new Error('Results section did not appear');
    }
    console.log('✓ Results section appeared');

    // Step 11: Take final screenshot
    console.log('\n' + '='.repeat(60));
    console.log('STEP 11: Taking final screenshot...');
    console.log('='.repeat(60));
    const screenshot2 = path.join(SCREENSHOT_DIR, '02_final_state.png');
    await page.screenshot({ path: screenshot2 });
    testResult.screenshots.push(screenshot2);
    console.log(`✓ Screenshot saved: ${screenshot2}`);

    console.log('\n' + '='.repeat(60));
    console.log('✓ ALL TEST STEPS COMPLETED SUCCESSFULLY!');
    console.log('='.repeat(60));

    testResult.status = 'passed';

  } catch (error) {
    console.error(`\n✗ Test failed: ${error.message}`);
    testResult.status = 'failed';
    testResult.error = error.message;

    if (page) {
      const failScreenshot = path.join(SCREENSHOT_DIR, '99_failure.png');
      await page.screenshot({ path: failScreenshot }).catch(() => {});
      testResult.screenshots.push(failScreenshot);
    }
  } finally {
    if (browser) {
      await browser.close();
    }

    fs.writeFileSync('test_results.json', JSON.stringify(testResult, null, 2));
    console.log('\n' + '='.repeat(60));
    console.log('TEST RESULT');
    console.log('='.repeat(60));
    console.log(JSON.stringify(testResult, null, 2));
  }
}

runTest();
