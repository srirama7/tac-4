const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function runTest() {
  const results = {
    test_name: "Basic Query Execution",
    status: "passed",
    screenshots: [],
    error: null
  };

  const baseDir = "C:/Users/amogh/Downloads/tac5/tac-5";
  const screenshotDir = path.join(baseDir, "agents/d1f5b2a2/e2e_test_runner_0_0/img/basic_query");

  let browser;
  let page;

  try {
    // Launch browser in headed mode
    browser = await chromium.launch({
      headless: false,
      slowMo: 500 // Slow down for visibility
    });

    const context = await browser.newContext();
    page = await context.newPage();

    // Listen to console messages
    page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
    page.on('pageerror', error => console.error('BROWSER ERROR:', error.message));

    // Step 1: Navigate to the Application URL
    console.log("Step 1: Navigating to http://localhost:5173");
    await page.goto('http://localhost:5173', { waitUntil: 'networkidle' });

    // Step 2: Take a screenshot of the initial state
    console.log("Step 2: Taking screenshot of initial state");
    const screenshot1 = path.join(screenshotDir, "01_initial_state.png");
    await page.screenshot({ path: screenshot1, fullPage: true });
    results.screenshots.push(screenshot1);

    // Step 3: Verify the page title
    console.log("Step 3: Verifying page title");
    const title = await page.title();
    if (title !== "Natural Language SQL Interface") {
      throw new Error(`(Step 3 ❌) Expected title "Natural Language SQL Interface" but got "${title}"`);
    }
    console.log("✓ Page title verified");

    // Step 4: Verify core UI elements are present
    console.log("Step 4: Verifying core UI elements");

    // Query input textbox
    const queryInput = await page.locator('#query-input').count();
    if (queryInput === 0) {
      throw new Error('(Step 4 ❌) Failed to find element with selector "#query-input"');
    }
    console.log("✓ Query input found");

    // Query button
    const queryButton = await page.locator('button:has-text("Query")').count();
    if (queryButton === 0) {
      throw new Error('(Step 4 ❌) Failed to find Query button');
    }
    console.log("✓ Query button found");

    // Upload Data button
    const uploadButton = await page.locator('button:has-text("Upload Data")').count();
    if (uploadButton === 0) {
      throw new Error('(Step 4 ❌) Failed to find Upload Data button');
    }
    console.log("✓ Upload Data button found");

    // Available Tables section
    const tablesSection = await page.locator('text=Available Tables').count();
    if (tablesSection === 0) {
      throw new Error('(Step 4 ❌) Failed to find Available Tables section');
    }
    console.log("✓ Available Tables section found");

    // Step 5: Enter the query
    console.log("Step 5: Entering query text");
    await page.locator('#query-input').fill('Show me all users from the users table');

    // Step 6: Take a screenshot of the query input
    console.log("Step 6: Taking screenshot of query input");
    const screenshot2 = path.join(screenshotDir, "02_query_input.png");
    await page.screenshot({ path: screenshot2, fullPage: true });
    results.screenshots.push(screenshot2);

    // Step 7: Click the Query button
    console.log("Step 7: Clicking Query button");
    await page.locator('#query-button').click();

    // Wait for results to appear
    await page.waitForTimeout(3000);

    // Step 8: Verify the query results appear
    console.log("Step 8: Verifying query results appear");
    const resultsVisible = await page.locator('#results-section').isVisible();
    if (!resultsVisible) {
      throw new Error('(Step 8 ❌) Query results section not visible');
    }
    console.log("✓ Query results appeared");

    // Step 9: Verify the SQL translation is displayed
    console.log("Step 9: Verifying SQL translation");
    await page.waitForSelector('#sql-display .sql-query code', { timeout: 5000 });
    const sqlText = await page.locator('#sql-display .sql-query code').textContent();
    if (!sqlText || !sqlText.toLowerCase().includes('select') || !sqlText.toLowerCase().includes('users')) {
      throw new Error(`(Step 9 ❌) SQL translation does not contain expected content. Got: "${sqlText}"`);
    }
    console.log("✓ SQL translation verified");

    // Step 10: Take a screenshot of the SQL translation
    console.log("Step 10: Taking screenshot of SQL translation");
    const screenshot3 = path.join(screenshotDir, "03_sql_translation.png");
    await page.screenshot({ path: screenshot3, fullPage: true });
    results.screenshots.push(screenshot3);

    // Step 11: Verify the results table contains data
    console.log("Step 11: Verifying results table contains data");
    await page.waitForSelector('.results-table tbody tr', { timeout: 5000 });
    const tableRows = await page.locator('.results-table tbody tr').count();
    if (tableRows === 0) {
      throw new Error('(Step 11 ❌) Results table contains no data rows');
    }
    console.log(`✓ Results table has ${tableRows} rows`);

    // Step 12: Take a screenshot of the results
    console.log("Step 12: Taking screenshot of results");
    const screenshot4 = path.join(screenshotDir, "04_results.png");
    await page.screenshot({ path: screenshot4, fullPage: true });
    results.screenshots.push(screenshot4);

    // Step 13: Click "Hide" button to close results
    console.log("Step 13: Clicking Hide button");
    await page.locator('#toggle-results').click();
    await page.waitForTimeout(1000);

    const resultsContainerHidden = await page.locator('#results-container').isHidden();
    if (!resultsContainerHidden) {
      throw new Error('(Step 13 ❌) Results container still visible after clicking Hide');
    }
    console.log("✓ Hide button worked");

    console.log("\n✓ All test steps passed!");

  } catch (error) {
    console.error(`\n❌ Test failed: ${error.message}`);
    results.status = "failed";
    results.error = error.message;

    // Take error screenshot if page exists
    if (page) {
      try {
        const errorScreenshot = path.join(screenshotDir, "error_screenshot.png");
        await page.screenshot({ path: errorScreenshot, fullPage: true });
        results.screenshots.push(errorScreenshot);
      } catch (e) {
        console.error("Failed to take error screenshot:", e.message);
      }
    }
  } finally {
    if (browser) {
      await browser.close();
    }
  }

  // Write results to JSON file
  const resultsPath = path.join(baseDir, "test_results.json");
  fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));
  console.log(`\nResults written to: ${resultsPath}`);

  // Output JSON to console
  console.log("\n" + JSON.stringify(results, null, 2));

  return results;
}

runTest().catch(console.error);
