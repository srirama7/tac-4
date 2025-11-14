# E2E Test: Query Generator Button

Test the random query generator functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want a button that generates example queries based on my data
So that I can discover interesting insights and understand what types of questions I can ask

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Generate Query button
   - Upload Data button
   - Available Tables section

5. **Upload Sample Data**
   - Click the "Upload Data" button
   - Take a screenshot of the upload modal
   - Click on the "Users Data" sample button
   - **Verify** success message appears
   - **Verify** users table appears in Available Tables section
   - Take a screenshot showing the loaded table

6. **Test Generate Query Button - First Generation**
   - **Verify** Generate Query button is visible and enabled
   - Click the "Generate Query" button
   - **Verify** loading state is shown (button disabled with spinner)
   - Wait for query generation to complete
   - **Verify** query input field is populated with generated query
   - **Verify** generated query is natural language (NOT SQL)
   - **Verify** generated query is two sentences or less
   - Take a screenshot of the generated query
   - Store the generated query text for comparison

7. **Test Generated Query Execution**
   - Click the "Query" button to execute the generated query
   - **Verify** query results appear
   - **Verify** SQL translation is displayed
   - **Verify** results table contains data
   - Take a screenshot of the query results

8. **Test Generate Query Button - Second Generation**
   - Click the "Generate Query" button again
   - Wait for query generation to complete
   - **Verify** a new query is generated (different from the first one)
   - **Verify** new query overwrites the previous content in input field
   - Take a screenshot of the second generated query

9. **Test Generated Query Variety**
   - Click the "Generate Query" button a third time
   - Wait for query generation to complete
   - **Verify** another query is generated
   - **Verify** queries show variety (not all identical)

10. **Test with Multiple Tables**
    - Click "Upload Data" button
    - Click on "Product Inventory" sample button
    - **Verify** products table appears in Available Tables
    - Click the "Generate Query" button
    - **Verify** generated query may reference multiple tables
    - Take a screenshot of the multi-table query

11. **Test Error Handling - No Tables**
    - Remove all tables from the database
    - Click the "Generate Query" button
    - **Verify** appropriate error message or informative text is shown
    - Take a screenshot of the error state

## Success Criteria

- Generate Query button is visible and properly positioned
- Button is styled consistently with Upload Data button (secondary-button style)
- Button is separated from Query button using space-between layout
- Clicking button shows loading state (disabled with spinner)
- Generated query appears in input field
- Generated query is natural language (NOT SQL)
- Generated query is limited to two sentences maximum
- Generated query is contextually relevant to database schema
- Query overwrites existing content in input field
- Each click generates a different/varied query
- Generated queries can be executed successfully
- Works with single table
- Works with multiple tables
- Handles no tables scenario gracefully
- At least 7 screenshots are taken
- No console errors during test execution

## Expected Query Characteristics

Generated queries should:
- Be natural language questions (e.g., "What is the average age of users?")
- NOT be SQL (e.g., NOT "SELECT AVG(age) FROM users")
- Be specific to actual tables and columns in the database
- Be two sentences or less
- Showcase different types of analysis (aggregations, filters, comparisons, etc.)
- Be actionable and interesting to a data analyst
