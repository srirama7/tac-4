# E2E Test: Query Generator Button

Test the query generator functionality that generates interesting natural language queries based on database schema.

## User Story

As a user of the Natural Language SQL Interface
I want to click a button that generates interesting natural language queries based on my database tables
So that I can discover new ways to query my data and get inspiration for questions I can ask without having to think of queries from scratch

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

5. Click the "Upload Data" button to open the upload modal
6. Take a screenshot of the upload modal
7. Click the "Users Data" sample data button
8. **Verify** the modal closes
9. **Verify** a success message appears indicating the table was created
10. Take a screenshot showing the uploaded table
11. **Verify** the "Available Tables" section shows the "users" table

12. Click the "Generate Query" button
13. **Verify** the button shows a loading state while processing
14. **Verify** after processing, the query input field is populated with generated text
15. Take a screenshot of the generated query in the input field
16. **Verify** the generated query is non-empty
17. **Verify** the generated query is relevant to the users table data
18. **Verify** the generated query ends with a question mark

19. Click the "Query" button to execute the generated query
20. **Verify** the query executes successfully
21. **Verify** the SQL translation is displayed
22. Take a screenshot of the query execution results
23. **Verify** the results table contains data
24. **Verify** no error messages are displayed

25. Click the "Generate Query" button again to generate a different query
26. **Verify** the query input field is populated with new text (overwriting the previous query)
27. Take a screenshot of the second generated query
28. **Verify** the second generated query is different from the first

## Success Criteria
- Generate Query button is visible and clickable
- Button shows loading state during query generation
- Generated query populates the input field automatically
- Generated query overwrites any existing content in the input field
- Generated query is limited to two sentences maximum
- Generated query is relevant to the database schema
- Generated query can be successfully executed
- Multiple clicks generate different queries
- At least 6 screenshots are taken
