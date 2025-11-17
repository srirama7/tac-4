const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Use proper Windows path
  const baseDir = path.join('C:', 'Users', 'amogh', 'Downloads', 'tac5', 'tac-5');
  const screenshotDir = path.join(baseDir, 'agents', 'ff7ca896', 'e2e_test_runner_1_0', 'img', 'basic_query');
  
  // Ensure directory exists
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }
  
  const results = {
    test_name: "Basic Query Execution",
    status: "passed",
    screenshots: [],
    error: null
  };
  
  try {
    // Step 1: Navigate to the Application URL
    console.log('Step 1: Navigating to http://localhost:5173...');
    await page.goto('http://localhost:5173', { waitUntil: 'networkidle' });
    
    // Step 2: Take a screenshot of the initial state
    console.log('Step 2: Taking screenshot of initial state...');
    const screenshot1 = path.join(screenshotDir, '01_initial_state.png');
    await page.screenshot({ path: screenshot1, fullPage: true });
    results.screenshots.push(screenshot1);
    
    // Step 3: Verify the page title
    console.log('Step 3: Verifying page title...');
    const title = await page.title();
    if (title !== 'Natural Language SQL Interface') {
      throw new Error(`(Step 3 ❌) Expected page title "Natural Language SQL Interface", got "${title}"`);
    }
    console.log('✓ Page title verified');
    
    // Step 4: Verify core UI elements are present
    console.log('Step 4: Verifying core UI elements...');
    
    const queryInput = page.locator('#query-input');
    if (!(await queryInput.isVisible())) {
      throw new Error('(Step 4 ❌) Query input textbox not found');
    }
    console.log('✓ Query input textbox found');
    
    const queryButton = page.locator('#query-button');
    if (!(await queryButton.isVisible())) {
      throw new Error('(Step 4 ❌) Query button not found');
    }
    console.log('✓ Query button found');
    
    const uploadButton = page.locator('#upload-data-button');
    if (!(await uploadButton.isVisible())) {
      throw new Error('(Step 4 ❌) Upload Data button not found');
    }
    console.log('✓ Upload Data button found');
    
    const tablesSection = page.locator('h3:has-text("Available Tables")');
    if (!(await tablesSection.isVisible())) {
      throw new Error('(Step 4 ❌) Available Tables section not found');
    }
    console.log('✓ Available Tables section found');
    
    // Step 5: Enter the query
    console.log('Step 5: Entering query...');
    await queryInput.fill('Show me all users from the users table');
    
    // Step 6: Take a screenshot of the query input
    console.log('Step 6: Taking screenshot of query input...');
    const screenshot2 = path.join(screenshotDir, '02_query_input.png');
    await page.screenshot({ path: screenshot2, fullPage: true });
    results.screenshots.push(screenshot2);
    
    // Step 7: Click the Query button
    console.log('Step 7: Clicking Query button...');
    await queryButton.click();
    
    // Wait for results section to become visible
    console.log('Waiting for query results...');
    const resultsSection = page.locator('#results-section');
    await resultsSection.waitFor({ state: 'visible', timeout: 15000 });
    
    // Step 8: Verify the query results appear
    console.log('Step 8: Verifying query results appear...');
    if (!(await resultsSection.isVisible())) {
      throw new Error('(Step 8 ❌) Query results did not appear');
    }
    console.log('✓ Query results appeared');
    
    // Step 9: Verify the SQL translation is displayed
    console.log('Step 9: Verifying SQL translation...');
    const sqlDisplay = page.locator('#sql-display');
    if (!(await sqlDisplay.isVisible())) {
      throw new Error('(Step 9 ❌) SQL display section not visible');
    }
    
    const sqlContent = await sqlDisplay.textContent();
    if (!sqlContent || (!sqlContent.toLowerCase().includes('select') || !sqlContent.toLowerCase().includes('users'))) {
      throw new Error(`(Step 9 ❌) SQL translation does not contain expected "SELECT ... FROM users", got: ${sqlContent}`);
    }
    console.log('✓ SQL translation verified');
    
    // Step 10: Take a screenshot of the SQL translation
    console.log('Step 10: Taking screenshot of SQL translation...');
    const screenshot3 = path.join(screenshotDir, '03_sql_translation.png');
    await page.screenshot({ path: screenshot3, fullPage: true });
    results.screenshots.push(screenshot3);
    
    // Step 11: Verify the results table contains data
    console.log('Step 11: Verifying results table contains data...');
    const resultsContainer = page.locator('#results-container');
    const dataTable = resultsContainer.locator('table');
    if (!(await dataTable.isVisible())) {
      throw new Error('(Step 11 ❌) Results table not found');
    }
    
    const rows = await dataTable.locator('tr').count();
    if (rows < 2) {
      throw new Error(`(Step 11 ❌) Results table does not contain data (found ${rows} rows)`);
    }
    console.log(`✓ Results table contains data (${rows} rows)`);
    
    // Step 12: Take a screenshot of the results
    console.log('Step 12: Taking final screenshot of results...');
    const screenshot4 = path.join(screenshotDir, '04_results.png');
    await page.screenshot({ path: screenshot4, fullPage: true });
    results.screenshots.push(screenshot4);
    
    // Step 13: Click "Hide" button to close results
    console.log('Step 13: Clicking Hide button...');
    const hideButton = page.locator('#toggle-results');
    if (await hideButton.isVisible()) {
      await hideButton.click();
      console.log('✓ Hide button clicked');
      
      await page.waitForTimeout(500);
      const containerDisplay = await resultsContainer.evaluate(el => window.getComputedStyle(el).display);
      if (containerDisplay !== 'none') {
        console.log('! Warning: Results container may not be hidden');
      } else {
        console.log('✓ Results hidden successfully');
      }
    } else {
      throw new Error('(Step 13 ❌) Hide button not found');
    }
    
    console.log('\n✅ All test steps completed successfully!');
    
  } catch (error) {
    results.status = 'failed';
    results.error = error.message;
    console.error('\n❌ Test failed:', error.message);
  } finally {
    await browser.close();
    
    const outputPath = path.join(baseDir, 'test_results.json');
    fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
    console.log(`\nTest results written to ${outputPath}`);
    
    // Also print the results
    console.log('\n' + JSON.stringify(results, null, 2));
  }
})();
