# E2E Test: Random Query Generator Button

## User Story
As a data analyst,
I want to click a "Generate Query" button and get a natural language query suggestion based on my database structure,
So that I can easily explore my data and discover interesting insights without having to manually write queries.

## Test Steps

### Setup Phase
1. Navigate to http://localhost:5173 (application homepage)
2. Verify the page loads successfully
3. Verify the "Generate Query" button is visible in the secondary buttons section (next to "Random SQL")
4. Verify the "Generate Query" button is enabled (not grayed out)
5. Verify button styling matches "Upload Data" button (white background, blue border)

### Test Phase 1: Error Handling - No Data Loaded
1. Without uploading any data, click the "Generate Query" button
2. Verify an error message appears indicating no tables are loaded
3. Verify the button remains enabled and returns to normal state
4. Verify error message is user-friendly and helpful

### Test Phase 2: With Sample Data - Users Dataset
1. Click "Upload Data" button
2. In the modal, click "Users Data" sample button
3. Wait for upload success message
4. Verify tables are loaded in the "Available Tables" section showing "users" table
5. Click the "Generate Query" button
6. Verify button shows "Generating..." text and is disabled
7. Wait for generation to complete (should be < 10 seconds)
8. Verify button text returns to "Generate Query" and is re-enabled
9. Verify the query input field is populated with a generated natural language query
10. Verify the description is 1-2 sentences maximum
11. Verify the description references actual table/column names from the users table (e.g., "users", "email", "signup_date")
12. Verify the description is a practical question (e.g., "Show me users who signed up in the last 30 days")

### Test Phase 3: Multiple Generations - Verify Randomness
1. Click "Generate Query" button again
2. Wait for generation to complete
3. Verify a different description appears in the query input field
4. Click "Generate Query" button a third time
5. Wait for generation to complete
6. Verify the description is different from the previous two (randomness is working)

### Test Phase 4: Query Execution - Test Generated Query
1. After getting a generated description, click the "Query" button
2. Verify the query executes successfully
3. Verify results are displayed in the "Query Results" section
4. Verify no errors occur during query execution

### Test Phase 5: With Multiple Tables - Products Dataset
1. Click "Upload Data" button
2. Click "Product Inventory" sample button
3. Wait for upload success
4. Verify two tables are now loaded: "users" and "products"
5. Click "Generate Query" button
6. Wait for generation
7. Verify the description might reference both tables or complex queries
8. Verify description is still practical and 1-2 sentences

### Test Phase 6: Overwriting Existing Text
1. Type some text in the query input field: "This is test text that should be replaced"
2. Click "Generate Query" button
3. Wait for generation
4. Verify the query input field is completely overwritten with the new generated description
5. Verify "This is test text that should be replaced" is no longer in the field

### Test Phase 7: Loading State Visual Feedback
1. Click "Generate Query" button
2. Immediately observe the button
3. Verify button text changes to "Generating..."
4. Verify button is disabled (grayed out) during generation
5. Verify cursor changes to "not-allowed" if hovering over disabled button
6. Wait for completion
7. Verify button re-enables and text returns to "Generate Query"

### Test Phase 8: Button Positioning and Styling
1. Verify "Generate Query" button is positioned in the secondary-buttons container
2. Verify it's positioned next to or near the "Random SQL" button
3. Verify button styling is consistent with other secondary buttons (Upload Data)
4. Verify button has proper spacing and alignment
5. Verify button is responsive on smaller screen sizes

### Test Phase 9: Keyboard Navigation and Focus Management
1. Use Tab key to navigate to the "Generate Query" button
2. Verify button receives focus (visible focus indicator)
3. Press Enter to activate the button
4. Verify the button generates a query as expected
5. Verify focus is moved to the query input field after generation

### Test Phase 10: Rapid Clicking - Prevent Multiple Concurrent Requests
1. Click "Generate Query" button rapidly multiple times
2. Verify only one API request is made (button is disabled during processing)
3. Verify no duplicate or overlapping query generations occur
4. Verify button completes cleanly with a single result

## Success Criteria

- ✅ Generate Query button is visible and properly styled (secondary-button class)
- ✅ Button is positioned correctly next to Random SQL button
- ✅ Button matches Upload Data button styling (white background, blue border)
- ✅ Clicking button without data shows user-friendly error message
- ✅ Clicking button with data generates query description within 10 seconds
- ✅ Generated descriptions are 1-2 sentences maximum
- ✅ Generated descriptions are practical and context-relevant questions
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
- ✅ Button is responsive on all screen sizes
- ✅ Keyboard navigation and focus management work correctly

## Expected Button Behavior

### Normal Flow
1. User clicks "Generate Query" button
2. Button disables and text changes to "Generating..."
3. API call to `/api/random-sql` is made
4. Gemini LLM generates natural language query description based on schema
5. Response is received with description and tables analyzed
6. Query input field is populated with description (overwrites existing)
7. Button re-enables and text returns to "Generate Query"
8. Focus is moved to query input field
9. User can now click Query to execute or modify the description

### Error Flow
1. User clicks "Generate Query" button
2. Button disables temporarily
3. API call fails or returns error
4. Error message is displayed in results section
5. Button re-enables
6. User can try again or load data first

## Test Screenshots to Capture

1. **Initial State** - Application loaded with "Generate Query" button visible
2. **Button Positioning** - Screenshot showing button next to "Random SQL" button
3. **Error Message** - No data loaded error displayed
4. **Loading State** - Button showing "Generating..." text, disabled
5. **Generated Description** - Query input field populated with description
6. **Multiple Descriptions** - Showing different descriptions from multiple clicks
7. **Query Results** - Successfully executed generated query showing results
8. **Multiple Tables** - Generate Query working with multiple tables loaded
9. **Text Overwrite** - Before and after showing text was completely replaced

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
- The generated descriptions should vary significantly between calls
- Descriptions should demonstrate real-world scenarios and questions
- Generation should use Gemini Flash model for fast, reliable responses
- Feature integrates with existing `/api/random-sql` endpoint
- Feature uses existing `generate_random_sql_description()` function from backend
- No new backend dependencies are required
