# E2E Test: Random SQL Generator Button

## User Story
As a user,
I want to click a "Random SQL" button and get a randomly generated SQL description,
So that I can discover interesting queries to ask about my data without having to think of questions from scratch.

## Test Steps

### Setup Phase
1. Navigate to http://localhost:5173 (application homepage)
2. Verify the page loads successfully
3. Verify the "Random SQL" button is visible in the query controls section
4. Verify the "Random SQL" button is enabled (not grayed out)

### Test Phase 1: Error Handling - No Data Loaded
1. Without uploading any data, click the "Random SQL" button
2. Verify an error message appears: "Please upload data first before generating random SQL"
3. Verify the button remains enabled

### Test Phase 2: With Sample Data - Users Dataset
1. Click "Upload Data" button
2. In the modal, click "Users Data" sample button
3. Wait for upload success message
4. Verify tables are loaded in the "Available Tables" section showing "users" table
5. Click the "Random SQL" button
6. Verify button shows "Generating..." text and is disabled
7. Wait for generation to complete (should be < 10 seconds)
8. Verify button text returns to "Random SQL" and is re-enabled
9. Verify the query input field is populated with a random SQL description
10. Verify the description is 1-3 sentences maximum
11. Verify the description references actual table/column names from the users table (e.g., "users", "email", "signup_date")
12. Verify the description is practical (e.g., "Show me users who signed up in the last 30 days")

### Test Phase 3: Multiple Generations - Verify Randomness
1. Click "Random SQL" button again
2. Wait for generation to complete
3. Verify a different description appears in the query input field
4. Click "Random SQL" button a third time
5. Wait for generation to complete
6. Verify the description is different from the previous two (randomness is working)

### Test Phase 4: Query Execution - Test Generated Query
1. After getting a generated description, click the "Query" button
2. Verify the query executes successfully
3. Verify results are displayed in the "Query Results" section
4. Verify no errors occur

### Test Phase 5: With Multiple Tables - Orders Dataset
1. Click "Upload Data" button
2. Click "Product Inventory" sample button
3. Wait for upload success
4. Verify two tables are now loaded: "users" and "products"
5. Click "Random SQL" button
6. Wait for generation
7. Verify the description might reference both tables or complex queries (JOINs, aggregations)
8. Verify description is still practical and 1-3 sentences

### Test Phase 6: Overwriting Existing Text
1. Type some text in the query input field: "Test query text"
2. Click "Random SQL" button
3. Wait for generation
4. Verify the query input field is completely overwritten with the new generated description
5. Verify "Test query text" is no longer in the field

### Test Phase 7: Loading State Visual Feedback
1. Click "Random SQL" button
2. Immediately observe the button
3. Verify button text changes to "Generating..."
4. Verify button is disabled (grayed out) during generation
5. Verify cursor changes to "not-allowed" if hovering over disabled button
6. Wait for completion
7. Verify button re-enables and text returns to "Random SQL"

### Test Phase 8: Error Handling - API Failure
1. (Optional: Requires mocking or network tampering)
2. Simulate network failure
3. Click "Random SQL" button
4. Verify an error message appears
5. Verify button re-enables after error

## Success Criteria

- ✅ Random SQL button is visible and properly styled (secondary-button class)
- ✅ Button is positioned correctly next to Upload Data button
- ✅ Clicking button without data shows user-friendly error message
- ✅ Clicking button with data generates SQL description within 10 seconds
- ✅ Generated descriptions are 1-3 sentences maximum
- ✅ Generated descriptions are practical and context-relevant
- ✅ Descriptions reference actual table and column names from loaded data
- ✅ Multiple clicks generate different descriptions (randomness works)
- ✅ Button shows loading state during generation (text changes to "Generating...")
- ✅ Button is disabled during API call
- ✅ Button re-enables after API call completes (success or failure)
- ✅ Generated description populates query input field
- ✅ Existing text in query field is completely overwritten
- ✅ Generated queries can be executed successfully (Query button works)
- ✅ No errors appear in browser console
- ✅ Error handling is graceful with user-friendly messages
- ✅ Works with single table and multiple tables
- ✅ Works with different data types (users, products, events)

## Expected Button Behavior

### Normal Flow
1. User clicks "Random SQL" button
2. Button disables and text changes to "Generating..."
3. API call to `/api/random-sql` is made
4. Gemini LLM generates description based on schema
5. Response is received with description and tables analyzed
6. Query input field is populated with description
7. Button re-enables and text returns to "Random SQL"
8. User can now click Query or modify the description

### Error Flow
1. User clicks "Random SQL" button
2. Button disables temporarily
3. API call fails or returns error
4. Error message is displayed in results section
5. Button re-enables
6. User can try again or load data first

## Test Screenshots to Capture

1. **Initial State** - Application loaded with "Random SQL" button visible
2. **Error Message** - "Please upload data first" error displayed
3. **Loading State** - Button showing "Generating..." text, disabled
4. **Generated Description** - Query input field populated with description
5. **Multiple Descriptions** - Showing different descriptions from multiple clicks
6. **Query Results** - Successfully executed generated query showing results

## Timeout Handling

- API call should complete within 10 seconds
- If API call takes longer than 10 seconds, display timeout error
- Button should remain responsive (always re-enable after completion)

## Browser Compatibility

Test on:
- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest) - if available
- Edge (latest) - if available

## Notes

- Ensure `GEMINI_API_KEY` environment variable is set before running tests
- The random descriptions should vary significantly between calls (different query patterns, tables, columns)
- Descriptions should demonstrate real-world scenarios (not generic like "Show all data")
- Generation should use Gemini 2.5 Flash model for fast, reliable responses
