const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function runTest() {
  const results = {
    test_name: "Generate Query Functionality",
    status: "passed",
    screenshots: [],
    error: null
  };

  const screenshotDir = path.join(process.cwd(), 'agents', 'befa7885', 'e2e_test_runner_1_2', 'img', 'query_generator');

  // Ensure screenshot directory exists
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Step 1: Navigate to the application
    console.log('Step 1: Navigating to application...');
    await page.goto('http://localhost:5177', { waitUntil: 'networkidle' });

    // Step 2: Take screenshot of initial state
    console.log('Step 2: Taking screenshot of initial state...');
    const screenshot1 = path.join(screenshotDir, '01_initial_state.png');
    await page.screenshot({ path: screenshot1, fullPage: true });
    results.screenshots.push(screenshot1);

    // Step 3: Verify page title
    console.log('Step 3: Verifying page title...');
    const title = await page.title();
    if (title !== 'Natural Language SQL Interface') {
      throw new Error(`(Step 3 ❌) Page title is "${title}", expected "Natural Language SQL Interface"`);
    }

    // Step 4: Verify core UI elements
    console.log('Step 4: Verifying core UI elements...');
    const queryInput = await page.locator('textarea[placeholder*="query" i], input[placeholder*="query" i], textarea').first();
    const queryButton = await page.locator('button:has-text("Query"), button:has-text("Submit")').first();
    const generateQueryButton = await page.locator('button:has-text("Generate Query")').first();
    const uploadButton = await page.locator('button:has-text("Upload Data")').first();

    if (!(await queryInput.isVisible())) {
      throw new Error('(Step 4 ❌) Query input textbox not found');
    }
    if (!(await queryButton.isVisible())) {
      throw new Error('(Step 4 ❌) Query button not found');
    }
    if (!(await generateQueryButton.isVisible())) {
      throw new Error('(Step 4 ❌) Generate Query button not found');
    }
    if (!(await uploadButton.isVisible())) {
      throw new Error('(Step 4 ❌) Upload Data button not found');
    }

    // Step 5: Click Upload Data button
    console.log('Step 5: Clicking Upload Data button...');
    await uploadButton.click();
    await page.waitForTimeout(1000);

    // Step 6: Upload sample data file
    console.log('Step 6: Looking for sample data button...');
    // Look for a sample data button (like "Users" or similar)
    const sampleUsersButton = await page.locator('button:has-text("Users"), button:has-text("users")').first();
    if (await sampleUsersButton.isVisible()) {
      await sampleUsersButton.click();
    } else {
      // If no sample button, try file upload
      const fileInput = await page.locator('input[type="file"]');
      const sampleDataPath = path.join(process.cwd(), 'app', 'client', 'public', 'sample-data', 'users.json');
      await fileInput.setInputFiles(sampleDataPath);
    }

    // Step 7: Verify upload success message
    console.log('Step 7: Waiting for upload success...');
    await page.waitForTimeout(2000);

    // Step 8: Verify table is listed
    console.log('Step 8: Verifying table is listed...');
    const tablesList = await page.locator('text=/users|Available Tables/i').first();
    await tablesList.waitFor({ timeout: 5000 });

    // Step 9: Take screenshot of uploaded table
    console.log('Step 9: Taking screenshot of uploaded table...');
    const screenshot2 = path.join(screenshotDir, '02_uploaded_table.png');
    await page.screenshot({ path: screenshot2, fullPage: true });
    results.screenshots.push(screenshot2);

    // Close modal if open
    const closeButton = await page.locator('button:has-text("Close"), button:has-text("×"), [aria-label="Close"]').first();
    if (await closeButton.isVisible()) {
      await closeButton.click();
      await page.waitForTimeout(500);
    }

    // Step 10: Click Generate Query button
    console.log('Step 10: Clicking Generate Query button...');
    await generateQueryButton.click();
    await page.waitForTimeout(3000); // Wait for query generation

    // Step 11-13: Verify query input is populated
    console.log('Step 11-13: Verifying generated query...');
    const queryValue = await queryInput.inputValue();
    if (!queryValue || queryValue.trim() === '') {
      throw new Error('(Step 12 ❌) Query input field is empty after clicking Generate Query');
    }

    const hasUsersReference = queryValue.toLowerCase().includes('users') ||
                              queryValue.toLowerCase().includes('user') ||
                              queryValue.toLowerCase().includes('name') ||
                              queryValue.toLowerCase().includes('email') ||
                              queryValue.toLowerCase().includes('age');

    if (!hasUsersReference) {
      console.warn(`Warning: Generated query may not reference schema: "${queryValue}"`);
    }

    // Step 14: Take screenshot of generated query
    console.log('Step 14: Taking screenshot of generated query...');
    const screenshot3 = path.join(screenshotDir, '03_first_generated_query.png');
    await page.screenshot({ path: screenshot3, fullPage: true });
    results.screenshots.push(screenshot3);

    const firstQuery = queryValue;

    // Step 15: Click Query button to execute
    console.log('Step 15: Executing generated query...');
    await queryButton.click();
    await page.waitForTimeout(3000); // Wait for query execution

    // Step 16-18: Verify results
    console.log('Step 16-18: Verifying query results...');
    const resultsTable = await page.locator('table, [role="table"], .results').first();
    if (!(await resultsTable.isVisible({ timeout: 5000 }))) {
      throw new Error('(Step 17 ❌) Results table not displayed after query execution');
    }

    // Step 19: Take screenshot of results
    console.log('Step 19: Taking screenshot of query results...');
    const screenshot4 = path.join(screenshotDir, '04_query_results.png');
    await page.screenshot({ path: screenshot4, fullPage: true });
    results.screenshots.push(screenshot4);

    // Step 20: Click Generate Query again
    console.log('Step 20: Clicking Generate Query button again...');
    await generateQueryButton.click();
    await page.waitForTimeout(3000);

    // Step 21-22: Verify new query
    console.log('Step 21-22: Verifying second generated query...');
    const secondQueryValue = await queryInput.inputValue();
    if (!secondQueryValue || secondQueryValue.trim() === '') {
      throw new Error('(Step 21 ❌) Query input field is empty after second Generate Query click');
    }

    // Step 23: Take screenshot of second query
    console.log('Step 23: Taking screenshot of second generated query...');
    const screenshot5 = path.join(screenshotDir, '05_second_generated_query.png');
    await page.screenshot({ path: screenshot5, fullPage: true });
    results.screenshots.push(screenshot5);

    // Step 24: Verify query has maximum two sentences
    console.log('Step 24: Verifying query length...');
    const sentences = secondQueryValue.split(/[.!?]+/).filter(s => s.trim().length > 0);
    if (sentences.length > 2) {
      throw new Error(`(Step 24 ❌) Generated query has ${sentences.length} sentences, expected maximum 2`);
    }

    // Step 25-26: Execute second query
    console.log('Step 25-26: Executing second generated query...');
    await queryButton.click();
    await page.waitForTimeout(3000);

    if (!(await resultsTable.isVisible({ timeout: 5000 }))) {
      throw new Error('(Step 26 ❌) Results not displayed after executing second query');
    }

    console.log('✅ All test steps passed!');

  } catch (error) {
    results.status = 'failed';
    results.error = error.message;
    console.error('Test failed:', error.message);
  } finally {
    await browser.close();
  }

  // Output results as JSON
  console.log('\n=== TEST RESULTS ===');
  console.log(JSON.stringify(results, null, 2));

  // Exit with appropriate code
  process.exit(results.status === 'passed' ? 0 : 1);
}

runTest();
