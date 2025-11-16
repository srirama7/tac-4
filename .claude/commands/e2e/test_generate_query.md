# E2E Test: Generate Query Button

Test the Generate Query button functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want a button that generates example natural language queries based on my uploaded data
So that I can discover what kinds of questions I can ask and get started quickly without thinking of queries myself

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

5. Click the "Upload Data" button
6. **Verify** the upload modal appears
7. Click the "Users Data" sample data button
8. Wait for the upload to complete
9. **Verify** the "users" table appears in the Available Tables section
10. Take a screenshot showing the users table loaded

11. Click the "Generate Query" button
12. Wait for the query generation to complete
13. **Verify** the query input field is populated with text
14. **Verify** the generated query is relevant to the users table (should mention users, names, emails, or signup dates)
15. **Verify** the generated query is 2 sentences or less
16. Take a screenshot of the generated query in the input field

17. Click the "Query" button to execute the generated query
18. Wait for the query results to appear
19. **Verify** the query results section is displayed
20. **Verify** the SQL translation is shown
21. **Verify** the results table contains data from the users table
22. Take a screenshot of the executed query results

23. Click the "Generate Query" button again
24. Wait for the new query generation to complete
25. **Verify** the query input field is populated with a new query (may be different from the first)
26. Take a screenshot of the second generated query

## Success Criteria
- Generate Query button is visible between Query and Upload Data buttons
- Clicking Generate Query button triggers query generation
- Query input field is automatically populated with a generated query
- Generated query is contextually relevant to the uploaded users table
- Generated query is limited to a maximum of two sentences
- Loading state is shown while generating the query
- Generated query can be successfully executed using the Query button
- Results are displayed correctly after executing the generated query
- Button can be clicked multiple times to generate different queries
- 4 screenshots are taken:
  1. Users table loaded
  2. First generated query in input field
  3. Query results after executing generated query
  4. Second generated query in input field
