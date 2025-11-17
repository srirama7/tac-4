const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const APPLICATION_URL = 'http://localhost:5173';
const SCREENSHOT_DIR = 'C:/Users/amogh/Downloads/tac5/tac-5/agents/ff7ca896/e2e_test_runner_0_2/img/query_generator';
const USERS_JSON_PATH = 'C:/Users/amogh/Downloads/tac5/tac-5/app/client/public/sample-data/users.json';

const testResult = {
  test_name: "Generate Query Functionality",
  status: "passed",
  screenshots: [],
  error: null
};

async function runTest() {
  let browser, context, page;
  try {
    browser = await chromium.launch({ headless: false, slowMo: 500 });
    context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    page = await context.newPage();

    console.log('Step 1: Navigating to application...');
    await page.goto(APPLICATION_URL, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    console.log('Step 2: Taking screenshot of initial state...');
    const screenshot1 = path.join(SCREENSHOT_DIR, '01_initial_state.png');
    await page.screenshot({ path: screenshot1, fullPage: true });
    testResult.screenshots.push(screenshot1);

    console.log('Step 3: Verifying page title...');
    const title = await page.title();
    if (title !== 'Natural Language SQL Interface') {
      throw new Error(`(Step 3) Expected title but got "${title}"`);
    }

    console.log('Step 4: Verifying core UI elements...');
    const queryInput = page.locator('textarea').first();
    const queryButton = page.locator('button:has-text("Query")').first();
    const generateButton = page.locator('button:has-text("Generate Query")').first();
    const uploadButton = page.locator('button:has-text("Upload Data")').first();
    
    await Promise.all([
      queryInput.waitFor({ state: 'visible' }),
      queryButton.waitFor({ state: 'visible' }),
      generateButton.waitFor({ state: 'visible' }),
      uploadButton.waitFor({ state: 'visible' })
    ]);

    console.log('Step 5: Clicking Upload Data button...');
    await uploadButton.click();
    await page.waitForTimeout(1000);

    console.log('Step 6: Uploading users.json file...');
    const fileInput = page.locator('input[type="file"]').first();
    await fileInput.setInputFiles(USERS_JSON_PATH);
    await page.waitForTimeout(3000);

    console.log('Step 7: Verifying upload success...');
    // Check for success message or verify that modal closed automatically
    const hasSuccessMsg = await page.locator('text=/success|uploaded/i').isVisible({ timeout: 2000 }).catch(() => false);
    const closeBtn = page.locator('button:has-text("Close"), button:has-text("×")').first();
    const hasCloseBtn = await closeBtn.isVisible({ timeout: 1000 }).catch(() => false);

    if (hasCloseBtn) {
      await closeBtn.click();
      await page.waitForTimeout(1000);
    }

    console.log('Step 8: Verifying table in Available Tables...');
    // Wait for users table to appear in Available Tables section
    await page.waitForSelector('text=users', { timeout: 5000 });

    console.log('Step 9: Taking screenshot of uploaded table...');
    const screenshot2 = path.join(SCREENSHOT_DIR, '02_uploaded_table.png');
    await page.screenshot({ path: screenshot2, fullPage: true });
    testResult.screenshots.push(screenshot2);

    console.log('Step 10: Clicking Generate Query button...');
    await generateButton.click();
    await page.waitForTimeout(2000);

    // Wait for the query to be generated and populated - check for value change
    let queryValue = '';
    let attempts = 0;
    while (attempts < 30 && (!queryValue || !queryValue.trim())) {
      await page.waitForTimeout(1000);
      queryValue = await queryInput.inputValue();
      attempts++;

      // Check for error messages during generation
      const hasError = await page.locator('text=/HTTP error|error|failed/i').isVisible({ timeout: 500 }).catch(() => false);
      if (hasError) {
        const errorText = await page.locator('text=/HTTP error|error|failed/i').first().textContent();
        throw new Error(`(Step 10) Generate Query failed with error: ${errorText}`);
      }
    }

    console.log('Step 11-13: Verifying generated query...');
    if (!queryValue || !queryValue.trim()) {
      throw new Error('(Step 12) Generated query is empty after 30 second timeout');
    }
    if (!queryValue.toLowerCase().includes('user')) {
      throw new Error('(Step 13) Query does not reference users table');
    }

    console.log('Step 14: Taking screenshot of generated query...');
    console.log(`Generated: "${queryValue}"`);
    const screenshot3 = path.join(SCREENSHOT_DIR, '03_first_generated_query.png');
    await page.screenshot({ path: screenshot3, fullPage: true });
    testResult.screenshots.push(screenshot3);

    console.log('Step 15: Executing query...');
    await queryButton.click();
    await page.waitForTimeout(5000);

    console.log('Step 16-18: Verifying query results...');
    if (await page.locator('text=/error|failed/i').isVisible({ timeout: 2000 }).catch(() => false)) {
      throw new Error('(Step 16) Query execution failed');
    }
    await page.waitForSelector('table, [class*="result"]', { timeout: 5000 });
    await page.waitForSelector('text=/SELECT|FROM/i', { timeout: 3000 });

    console.log('Step 19: Taking screenshot of results...');
    const screenshot4 = path.join(SCREENSHOT_DIR, '04_query_results.png');
    await page.screenshot({ path: screenshot4, fullPage: true });
    testResult.screenshots.push(screenshot4);

    console.log('Step 20: Generating second query...');
    await generateButton.click();
    await page.waitForTimeout(8000);

    console.log('Step 21-22: Verifying new query...');
    const newQueryValue = await queryInput.inputValue();
    if (!newQueryValue || !newQueryValue.trim()) {
      throw new Error('(Step 22) Second query is empty');
    }

    console.log('Step 23: Taking screenshot of second query...');
    console.log(`Generated: "${newQueryValue}"`);
    const screenshot5 = path.join(SCREENSHOT_DIR, '05_second_generated_query.png');
    await page.screenshot({ path: screenshot5, fullPage: true });
    testResult.screenshots.push(screenshot5);

    console.log('Step 24: Verifying sentence count...');
    const sentenceCount = (newQueryValue.match(/[.!?]+/g) || []).length;
    if (sentenceCount > 2) {
      throw new Error(`(Step 24) Query has ${sentenceCount} sentences, max 2 expected`);
    }

    console.log('Step 25-26: Executing second query...');
    await queryButton.click();
    await page.waitForTimeout(5000);
    if (await page.locator('text=/error|failed/i').isVisible({ timeout: 2000 }).catch(() => false)) {
      throw new Error('(Step 26) Second query execution failed');
    }

    console.log('All tests passed!');
    testResult.status = 'passed';

  } catch (error) {
    console.error('Test failed:', error.message);
    testResult.status = 'failed';
    testResult.error = error.message;
    if (page) {
      const failScreenshot = path.join(SCREENSHOT_DIR, '99_failure.png');
      await page.screenshot({ path: failScreenshot, fullPage: true }).catch(() => {});
      testResult.screenshots.push(failScreenshot);
    }
  } finally {
    if (browser) await browser.close();
    fs.writeFileSync('test_results.json', JSON.stringify(testResult, null, 2));
    console.log('Results:', JSON.stringify(testResult, null, 2));
  }
}

runTest();
