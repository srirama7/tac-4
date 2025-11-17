# E2E Test: Generate Query Functionality

Test the Generate Query button functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want to generate random queries based on my uploaded data
So that I can explore my data without having to think of queries myself

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Generate Query button
   - Upload Data button

5. Click "Upload Data" button
6. Upload sample data file (`users.json`)
7. **Verify** the upload success message appears
8. **Verify** the table is listed in the "Available Tables" section
9. Take a screenshot of the uploaded table

10. Click "Generate Query" button
11. **Verify** the query input field is populated with text
12. **Verify** the query text is not empty
13. **Verify** the query references actual table/column names from the schema (e.g., "users" table)
14. Take a screenshot of the generated query

15. Click the "Query" button to execute the generated query
16. **Verify** query execution succeeds
17. **Verify** results are displayed successfully
18. **Verify** SQL translation is displayed
19. Take a screenshot of the query results

20. Click "Generate Query" button again
21. **Verify** the query input field is overwritten with a new query
22. **Verify** the new query is different from the previous one (or at least the field was updated)
23. Take a screenshot of the second generated query

24. **Verify** the generated query contains maximum two sentences
25. Execute the second generated query by clicking "Query" button
26. **Verify** the second query also executes successfully

## Success Criteria

- Generate Query button is visible and clickable
- Query is generated and populated into input field after button click
- Query is contextually relevant to uploaded data (references real tables/columns)
- Generated query overwrites any existing text in the input field
- Generated query is maximum two sentences
- Generated query can be successfully executed by clicking the Query button
- Results are displayed correctly after executing the generated query
- Subsequent clicks on Generate Query button produce new queries
- At least 4 screenshots are captured:
  1. Initial state
  2. Uploaded table
  3. First generated query
  4. Query results
  5. Second generated query

## Edge Cases to Test

- Click "Generate Query" before uploading any data (should show error message)
- Click "Generate Query" multiple times in succession
- Generated queries should vary in complexity (filters, aggregations, sorting, etc.)
- Generated queries should use natural, conversational language
