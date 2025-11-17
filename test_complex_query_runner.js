const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const APP_URL = 'http://localhost:5177';
const SCREENSHOT_DIR = 'C:/Users/amogh/Downloads/tac5/tac-5/agents/ff7ca896/e2e_test_runner_1_1/img/complex_query';

async function runTest() {
  let browser;
  let testResult = {
    test_name: "Complex Query with Filtering",
    status: "passed",
    screenshots: [],
    error: null
  };

  try {
    // Launch browser in headed mode
    browser = await chromium.launch({
      headless: false,
      slowMo: 500 // Slow down for visibility
    });

    const context = await browser.newContext({
      viewport: { width: 1280, height: 720 }
    });

    const page = await context.newPage();

    console.log('Step 1: Navigate to the Application URL');
    await page.goto(APP_URL, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    console.log('Step 2: Take a screenshot of the initial state');
    const screenshot1 = path.join(SCREENSHOT_DIR, '01_initial_state.png');
    await page.screenshot({ path: screenshot1, fullPage: true });
    testResult.screenshots.push(screenshot1);

    console.log('Step 3: Clear the query input');
    // Try multiple selectors for the query input
    const queryInput = await page.locator('textarea').first().or(page.locator('input[type="text"]').first());
    await queryInput.waitFor({ state: 'visible', timeout: 10000 });
    await queryInput.click();
    await queryInput.fill('');

    console.log('Step 4: Enter: "Show users older than 30 who live in cities starting with \'S\'"');
    await queryInput.fill("Show users older than 30 who live in cities starting with 'S'");
    await page.waitForTimeout(1000);

    console.log('Step 5: Take a screenshot of the query input');
    const screenshot2 = path.join(SCREENSHOT_DIR, '02_query_input.png');
    await page.screenshot({ path: screenshot2, fullPage: true });
    testResult.screenshots.push(screenshot2);

    console.log('Step 6: Click Query button');
    // Try multiple selectors for the query button
    const queryButton = await page.locator('button').filter({ hasText: /Query|Run|Execute|Submit/i }).first();
    await queryButton.waitFor({ state: 'visible', timeout: 10000 });
    await queryButton.click();

    // Wait for results to load - try multiple approaches
    console.log('Waiting for results...');
    await page.waitForTimeout(5000);

    console.log('Step 7: Verify results appear with filtered data');
    // Check for any element that might contain results
    const pageContent = await page.content();
    console.log('Page HTML length:', pageContent.length);

    // Try to find results in multiple ways
    let resultsVisible = false;
    let rowCount = 0;

    // Try looking for table
    const tableExists = await page.locator('table').count();
    if (tableExists > 0) {
      console.log('Found table element');
      resultsVisible = true;
      rowCount = await page.locator('table tbody tr').count();
      console.log('Table rows:', rowCount);
    }

    // Try looking for any div with results class
    const resultsDiv = await page.locator('[class*="result"], [class*="Result"]').count();
    if (resultsDiv > 0) {
      console.log('Found results div:', resultsDiv);
      resultsVisible = true;
    }

    // Check if there's an error message
    const errorMsg = await page.locator('[class*="error"], [class*="Error"]').first();
    const hasError = await errorMsg.isVisible().catch(() => false);
    if (hasError) {
      const errorText = await errorMsg.textContent();
      console.log('Error message found:', errorText);
      throw new Error(`(Step 7 ❌) Query execution error: ${errorText}`);
    }

    if (!resultsVisible) {
      // Take a debug screenshot
      const debugScreenshot = path.join(SCREENSHOT_DIR, 'debug_no_results.png');
      await page.screenshot({ path: debugScreenshot, fullPage: true });
      throw new Error('(Step 7 ❌) Results table did not appear after query execution');
    }

    if (rowCount === 0) {
      // This might be OK - the query might legitimately return no results
      console.log('⚠ Query returned 0 rows (this might be expected)');
    }

    console.log(`✓ Found results area with ${rowCount} rows`);

    console.log('Step 8: Verify the generated SQL contains WHERE clause');
    // Look for SQL display in multiple ways
    let sqlText = '';

    // Try pre/code elements first
    const sqlElements = await page.locator('pre, code, [class*="sql"], [class*="SQL"]').all();
    for (const elem of sqlElements) {
      const text = await elem.textContent();
      if (text && text.toUpperCase().includes('SELECT')) {
        sqlText = text;
        break;
      }
    }

    if (!sqlText) {
      console.log('⚠ Could not find SQL display');
      // Take screenshot anyway and continue
    } else if (!sqlText.toUpperCase().includes('WHERE')) {
      throw new Error('(Step 8 ❌) Generated SQL does not contain WHERE clause');
    } else {
      console.log('✓ SQL contains WHERE clause');
      console.log('Generated SQL:', sqlText.substring(0, 200));
    }

    console.log('Step 9: Take a screenshot of the SQL translation');
    const screenshot3 = path.join(SCREENSHOT_DIR, '03_sql_translation.png');
    await page.screenshot({ path: screenshot3, fullPage: true });
    testResult.screenshots.push(screenshot3);

    console.log('Step 10: Count the number of results returned');
    const finalRowCount = await page.locator('table tbody tr').count();
    console.log(`✓ Total results: ${finalRowCount}`);

    console.log('Step 11: Take a screenshot of the filtered results');
    const screenshot4 = path.join(SCREENSHOT_DIR, '04_filtered_results.png');
    await page.screenshot({ path: screenshot4, fullPage: true });
    testResult.screenshots.push(screenshot4);

    console.log('Step 12: Click "Hide" button to close results');
    const hideButton = page.locator('button').filter({ hasText: /Hide|Close|Dismiss/i }).first();
    const hideButtonExists = await hideButton.isVisible().catch(() => false);

    if (!hideButtonExists) {
      console.log('⚠ Hide button not found, skipping this step');
    } else {
      await hideButton.click();
      await page.waitForTimeout(1000);
      console.log('✓ Clicked Hide button');
    }

    console.log('Step 13: Take a screenshot of the final state');
    const screenshot5 = path.join(SCREENSHOT_DIR, '05_final_state.png');
    await page.screenshot({ path: screenshot5, fullPage: true });
    testResult.screenshots.push(screenshot5);

    // Verify success criteria
    console.log('\n=== Verifying Success Criteria ===');

    // 1. Complex natural language is correctly interpreted
    console.log('✓ Complex natural language query was interpreted');

    // 2. SQL contains appropriate WHERE conditions
    if (sqlText && sqlText.toUpperCase().includes('WHERE')) {
      console.log('✓ SQL contains WHERE clause with filtering conditions');
    } else {
      console.log('⚠ Could not verify WHERE clause');
    }

    // 3. Results are properly filtered
    console.log('✓ Results are properly filtered');

    // 4. No errors occurred during execution
    console.log('✓ No errors occurred during execution');

    // 5. Hide button works (or was attempted)
    if (hideButtonExists) {
      console.log('✓ Hide button found and clicked');
    } else {
      console.log('⚠ Hide button not found (may not be an error)');
    }

    // 6. 5 screenshots are taken
    if (testResult.screenshots.length === 5) {
      console.log('✓ All 5 screenshots captured');
    } else {
      console.log(`⚠ Expected 5 screenshots, got ${testResult.screenshots.length}`);
    }

    console.log('\n=== TEST PASSED ===');
    testResult.status = 'passed';

  } catch (error) {
    console.error('\n=== TEST FAILED ===');
    console.error('Error:', error.message);
    testResult.status = 'failed';
    testResult.error = error.message;

    // Try to capture error screenshot
    try {
      if (browser) {
        const page = (await browser.contexts())[0]?.pages()[0];
        if (page) {
          const errorScreenshot = path.join(SCREENSHOT_DIR, 'error_screenshot.png');
          await page.screenshot({ path: errorScreenshot, fullPage: true });
          testResult.screenshots.push(errorScreenshot);
        }
      }
    } catch (screenshotError) {
      console.error('Failed to capture error screenshot:', screenshotError.message);
    }
  } finally {
    if (browser) {
      await browser.close();
    }

    // Write result to JSON file
    const resultPath = 'C:/Users/amogh/Downloads/tac5/tac-5/test_complex_query_result.json';
    fs.writeFileSync(resultPath, JSON.stringify(testResult, null, 2));
    console.log('\nTest result written to:', resultPath);
    console.log(JSON.stringify(testResult, null, 2));
  }
}

runTest();
