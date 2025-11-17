const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const APPLICATION_URL = 'http://localhost:5178';
const SCREENSHOT_DIR = 'C:/Users/amogh/Downloads/tac5/tac-5/agents/ff7ca896/e2e_test_runner_1_2/img/query_generator';
const SAMPLE_DATA_PATH = 'C:/Users/amogh/Downloads/tac5/tac-5/app/client/public/sample-data/users.json';

async function runTest() {
  const results = {
    test_name: "Generate Query Functionality",
    status: "passed",
    screenshots: [],
    error: null,
    step_failures: []
  };

  let browser;
  let context;
  let page;

  try {
    // Launch browser in headed mode
    browser = await chromium.launch({
      headless: false,
      slowMo: 100
    });
    context = await browser.newContext();
    page = await context.newPage();

    // Step 1: Navigate to Application URL
    console.log('Step 1: Navigate to Application URL');
    await page.goto(APPLICATION_URL);
    await page.waitForLoadState('networkidle');

    // Step 2: Take screenshot of initial state
    console.log('Step 2: Take screenshot of initial state');
    const screenshot1 = path.join(SCREENSHOT_DIR, '01_initial_state.png');
    await page.screenshot({ path: screenshot1, fullPage: true });
    results.screenshots.push(screenshot1);

    // Step 3: Verify page title
    console.log('Step 3: Verify page title');
    const title = await page.title();
    if (title !== 'Natural Language SQL Interface') {
      results.step_failures.push(`(Step 3 ❌) Page title is "${title}", expected "Natural Language SQL Interface"`);
    }

    // Step 4: Verify core UI elements are present
    console.log('Step 4: Verify core UI elements');
    const queryInput = await page.locator('#query-input').count();
    const queryButton = await page.locator('#query-button').count();
    const generateQueryButton = await page.locator('#generate-query-button').count();
    const uploadButton = await page.locator('#upload-data-button').count();

    if (queryInput === 0) {
      results.step_failures.push('(Step 4 ❌) Query input textbox not found');
    }
    if (queryButton === 0) {
      results.step_failures.push('(Step 4 ❌) Query button not found');
    }
    if (generateQueryButton === 0) {
      results.step_failures.push('(Step 4 ❌) Generate Query button not found');
    }
    if (uploadButton === 0) {
      results.step_failures.push('(Step 4 ❌) Upload Data button not found');
    }

    // Step 5: Click Upload Data button
    console.log('Step 5: Click Upload Data button');
    await page.locator('#upload-data-button').click();
    await page.waitForTimeout(1000);

    // Step 6: Upload sample data file
    console.log('Step 6: Upload sample data file');
    const fileInput = await page.locator('input[type="file"]');
    await fileInput.setInputFiles(SAMPLE_DATA_PATH);
    await page.waitForTimeout(2000);

    // Step 7: Verify upload success message
    console.log('Step 7: Verify upload success message');
    try {
      await page.waitForSelector('text=/uploaded successfully|Table.*created/i', { timeout: 5000 });
    } catch (e) {
      results.step_failures.push('(Step 7 ❌) Upload success message not found');
    }

    // Step 8: Verify table is listed in Available Tables
    console.log('Step 8: Verify table in Available Tables');
    try {
      await page.waitForSelector('text=/Available Tables|users/i', { timeout: 5000 });
    } catch (e) {
      results.step_failures.push('(Step 8 ❌) Table not found in Available Tables section');
    }

    // Step 9: Take screenshot of uploaded table
    console.log('Step 9: Take screenshot of uploaded table');
    const screenshot2 = path.join(SCREENSHOT_DIR, '02_uploaded_table.png');
    await page.screenshot({ path: screenshot2, fullPage: true });
    results.screenshots.push(screenshot2);

    // Close upload modal if still open
    const closeButton = await page.locator('button:has-text("Close"), button:has-text("×")').first();
    if (await closeButton.isVisible()) {
      await closeButton.click();
      await page.waitForTimeout(500);
    }

    // Step 10: Click Generate Query button
    console.log('Step 10: Click Generate Query button');
    await page.locator('#generate-query-button').click();
    await page.waitForTimeout(3000);

    // Step 11: Verify query input field is populated
    console.log('Step 11: Verify query input field is populated');
    let queryTextarea, queryValue;
    try {
      queryTextarea = await page.locator('#query-input');
      queryValue = await queryTextarea.inputValue();
    } catch (e) {
      results.step_failures.push(`(Step 11 ❌) Failed to get query input value: ${e.message}`);
      throw e;
    }

    // Step 12: Verify query text is not empty
    console.log('Step 12: Verify query text is not empty');
    if (!queryValue || queryValue.trim().length === 0) {
      results.step_failures.push('(Step 12 ❌) Query text is empty after clicking Generate Query');
    }

    // Step 13: Verify query references actual table/column names
    console.log('Step 13: Verify query references table/column names');
    if (!queryValue.toLowerCase().includes('users')) {
      results.step_failures.push('(Step 13 ❌) Generated query does not reference the "users" table');
    }

    // Step 14: Take screenshot of generated query
    console.log('Step 14: Take screenshot of generated query');
    const screenshot3 = path.join(SCREENSHOT_DIR, '03_first_generated_query.png');
    await page.screenshot({ path: screenshot3, fullPage: true });
    results.screenshots.push(screenshot3);

    const firstQuery = queryValue;

    // Step 15: Click Query button to execute
    console.log('Step 15: Click Query button to execute');
    await page.locator('#query-button').click();
    await page.waitForTimeout(3000);

    // Step 16: Verify query execution succeeds
    console.log('Step 16: Verify query execution succeeds');
    const errorMessage = await page.locator('text=/error|failed/i').count();
    if (errorMessage > 0) {
      results.step_failures.push('(Step 16 ❌) Query execution failed');
    }

    // Step 17: Verify results are displayed
    console.log('Step 17: Verify results are displayed');
    const resultsTable = await page.locator('table, [class*="result"], [class*="table"]').count();
    if (resultsTable === 0) {
      results.step_failures.push('(Step 17 ❌) Query results not displayed');
    }

    // Step 18: Verify SQL translation is displayed
    console.log('Step 18: Verify SQL translation is displayed');
    const sqlDisplay = await page.locator('text=/SELECT|SQL:/i').count();
    if (sqlDisplay === 0) {
      results.step_failures.push('(Step 18 ❌) SQL translation not displayed');
    }

    // Step 19: Take screenshot of query results
    console.log('Step 19: Take screenshot of query results');
    const screenshot4 = path.join(SCREENSHOT_DIR, '04_query_results.png');
    await page.screenshot({ path: screenshot4, fullPage: true });
    results.screenshots.push(screenshot4);

    // Step 20: Click Generate Query button again
    console.log('Step 20: Click Generate Query button again');
    await page.locator('#generate-query-button').click();
    await page.waitForTimeout(3000);

    // Step 21: Verify query input field is overwritten
    console.log('Step 21: Verify query input field is overwritten');
    const secondQueryValue = await queryTextarea.inputValue();

    // Step 22: Verify new query is different
    console.log('Step 22: Verify new query is different');
    if (secondQueryValue === firstQuery) {
      results.step_failures.push('(Step 22 ❌) Second generated query is identical to the first');
    }

    // Step 23: Take screenshot of second generated query
    console.log('Step 23: Take screenshot of second generated query');
    const screenshot5 = path.join(SCREENSHOT_DIR, '05_second_generated_query.png');
    await page.screenshot({ path: screenshot5, fullPage: true });
    results.screenshots.push(screenshot5);

    // Step 24: Verify generated query contains maximum two sentences
    console.log('Step 24: Verify query contains max two sentences');
    const sentenceCount = (secondQueryValue.match(/[.!?]+/g) || []).length;
    if (sentenceCount > 2) {
      results.step_failures.push(`(Step 24 ❌) Generated query has ${sentenceCount} sentences, expected maximum 2`);
    }

    // Step 25: Execute second generated query
    console.log('Step 25: Execute second generated query');
    await page.locator('#query-button').click();
    await page.waitForTimeout(3000);

    // Step 26: Verify second query executes successfully
    console.log('Step 26: Verify second query executes successfully');
    const secondErrorMessage = await page.locator('text=/error|failed/i').count();
    if (secondErrorMessage > 0) {
      results.step_failures.push('(Step 26 ❌) Second query execution failed');
    }

    // Determine overall status
    if (results.step_failures.length > 0) {
      results.status = 'failed';
      results.error = results.step_failures.join('\n');
    }

    console.log('\n=== Test Complete ===');
    console.log('Status:', results.status);
    console.log('Screenshots:', results.screenshots.length);
    if (results.error) {
      console.log('Failures:\n', results.error);
    }

  } catch (error) {
    results.status = 'failed';
    results.error = `Unexpected error: ${error.message}\nStack: ${error.stack}`;
    console.error('Test failed with error:', error);
  } finally {
    // Write results to file
    const resultsPath = 'C:/Users/amogh/Downloads/tac5/tac-5/test_query_generator_results.json';
    fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));
    console.log('\nResults written to:', resultsPath);

    if (browser) {
      await browser.close();
    }
  }

  return results;
}

runTest().catch(console.error);
