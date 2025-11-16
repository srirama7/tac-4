# E2E Test: Query Generator Feature

Test the query generator feature that creates natural language query suggestions based on database schema.

## User Story

As a user
I want to automatically generate interesting natural language queries based on my data structure
So that I can better understand what questions I can ask and how to phrase them naturally

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** the "Generate Query" button is present in the UI

5. Click the "Upload Data" button
6. Load the sample users data (users.json)
7. **Verify** the users table appears in the "Available Tables" section
8. Take a screenshot showing the loaded table

9. Click the "Generate Query" button
10. **Verify** the button shows a loading state (spinner)
11. Wait for the query generation to complete
12. **Verify** the query input field is populated with generated text
13. **Verify** the generated query is 2 sentences or less
14. Take a screenshot of the populated query input
15. **Verify** the generated query text is relevant to the users table schema

16. Click the "Query" button to execute the generated query
17. **Verify** the query executes successfully
18. **Verify** results are displayed
19. Take a screenshot of the query results

20. Click the "Generate Query" button again
21. **Verify** a different query suggestion is generated (or same is acceptable)
22. **Verify** the previous query text is replaced with the new suggestion

## Success Criteria
- "Generate Query" button is visible and clickable
- Button shows loading state during generation
- Generated query populates the input field
- Generated query is 2 sentences or less
- Generated query is contextually relevant to the database schema
- Generated query can be executed successfully
- Query results are displayed correctly
- Clicking "Generate Query" multiple times works properly
- 4 screenshots are taken
