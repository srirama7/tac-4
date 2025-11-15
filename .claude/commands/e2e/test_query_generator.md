# E2E Test: Query Generator Button

Test the Generate Query button functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want to automatically generate natural language queries based on my uploaded data
So that I can discover useful ways to query my data and learn by example without having to think of queries myself

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** the Generate Query button is visible in the UI

5. Upload sample data (users.json) to populate the database:
   - Click the "Upload Data" button
   - Click the "Users Data" sample button
   - **Verify** the table is created successfully
   - Take a screenshot showing the uploaded table

6. Click the "Generate Query" button
7. **Verify** the button shows a loading state (disabled with spinner)
8. **Verify** the query input field gets populated with a generated query
9. Take a screenshot of the generated query in the input field
10. **Verify** the generated query is relevant to the users table
11. **Verify** the generated query is 2 sentences or less

12. Click the "Generate Query" button again
13. **Verify** the existing query is overwritten with a new generated query
14. Take a screenshot showing the new generated query

15. Execute the generated query:
    - Click the "Query" button
    - **Verify** results are returned successfully
    - Take a screenshot of the query results

16. Test with multiple tables:
    - Upload products.csv sample data
    - Click the "Generate Query" button
    - **Verify** the generated query references either users or products table
    - Take a screenshot of the multi-table generated query

17. Test error handling (no tables):
    - Remove all tables from the database
    - Click the "Generate Query" button
    - **Verify** an error message is displayed indicating no tables are available
    - Take a screenshot of the error state

## Success Criteria
- Generate Query button is visible and styled consistently with Upload Data button
- Button is positioned separately from primary action buttons (justify-apart layout)
- Button shows loading state while generating query
- Generated query populates the input field
- Generated query is relevant to the database schema
- Generated query is limited to 2 sentences maximum
- Existing content in input field is overwritten by new generated query
- Generated queries can be executed successfully
- Error handling works when no tables are loaded
- 7 screenshots are taken documenting the feature flow
