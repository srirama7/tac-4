# E2E Test: Natural Language Query Generator Button

Test the Generate Query button functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want to generate sample queries based on my data
So that I can discover interesting questions to ask

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the Generate Query button is present in the query controls section
4. **Verify** the button is positioned separately from Query and Upload Data buttons (using space-between layout)

5. Click the Upload Data button
6. Click the "Users Data" sample button to load sample data
7. **Verify** the users table appears in the Available Tables section
8. Take a screenshot of the loaded table

9. Click the Generate Query button
10. **Verify** the button shows loading state ("Generating..." text with spinner)
11. Wait for the query to be generated
12. **Verify** the query input field is populated with a natural language query
13. **Verify** the generated query is 2 sentences or less
14. **Verify** the generated query references table/column names from the schema
15. Take a screenshot of the populated query

16. Click the Query button to execute the generated query
17. **Verify** the query executes successfully
18. **Verify** results are displayed
19. Take a screenshot of the results

20. Click the Generate Query button again
21. **Verify** a different query is generated (or it may be similar due to randomness)
22. Take a screenshot of the second generated query

## Edge Case: No Tables

23. Remove the users table (click the × button)
24. Confirm the removal
25. Click the Generate Query button
26. **Verify** an error message is displayed: "No tables available. Please upload data first."
27. Take a screenshot of the error message

## Success Criteria
- Generate Query button is present and properly styled (secondary-button style)
- Button is positioned with space-between layout (separated from Query/Upload Data buttons)
- Button shows loading state while generating
- Query input field is populated with generated query on success
- Generated query is 2 sentences or less
- Generated query references actual table/column names
- Generated query can be executed successfully
- Error message is shown when no tables are available
- 5 screenshots are taken
