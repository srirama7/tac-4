# E2E Test: Query Generator Button

Test the query generator functionality that creates interesting natural language queries based on database schema.

## User Story

As a user
I want a button that generates example queries based on my uploaded tables
So that I can learn what types of questions to ask and discover insights in my data without having to think of queries from scratch

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Upload Data button
   - Generate Query button (should be positioned separately on the right)
   - Available Tables section

5. Click the "Upload Data" button to open the upload modal
6. Click the "Users Data" sample data button to upload sample data
7. **Verify** the modal closes automatically
8. **Verify** the "users" table appears in the Available Tables section
9. Take a screenshot showing the uploaded table

10. Click the "Generate Query" button
11. **Verify** the button shows a loading spinner while processing
12. **Verify** the query input field is populated with a generated query
13. **Verify** the generated query is non-empty
14. **Verify** the generated query appears to be natural language (not SQL)
15. **Verify** the generated query is limited to two sentences maximum
16. Take a screenshot of the generated query in the input field

17. Click the "Query" button to execute the generated query
18. **Verify** the query results appear
19. **Verify** the SQL translation is displayed
20. **Verify** the results table contains data (rows were returned)
21. Take a screenshot of the query execution results

22. Click the "Generate Query" button again (to test multiple generations)
23. **Verify** the query input field is overwritten with a new query
24. **Verify** the new query is different from the first one (or at least could be)
25. Take a screenshot of the second generated query

26. Test error handling: Remove all tables
27. Click the "Generate Query" button
28. **Verify** an appropriate error message is displayed (e.g., "No tables available")
29. Take a screenshot of the error state

## Success Criteria
- Generate Query button is visible and positioned separately from primary Query button
- Button shows loading state during API call
- Generated query populates the input field
- Generated queries are natural language, not SQL
- Generated queries are limited to two sentences
- Generated query can be successfully executed
- Button works multiple times (generates different queries)
- Error handling works when no tables exist
- 5 screenshots are taken documenting the workflow
