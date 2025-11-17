# E2E Test: Natural Language Query Generator Button

Test the natural language query generator button functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want to generate example natural language queries based on my uploaded tables
So that I can quickly explore my data without having to think of queries myself

## Test Steps

### Setup
1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. Click the "Upload Data" button
5. Upload sample data (users.json) to create a table with data
6. **Verify** the table appears in the "Available Tables" section

### Test Generate Query Button Presence
7. **Verify** the "Generate Query" button is visible in the query controls section
8. **Verify** the button is styled consistently with the "Upload Data" button
9. **Verify** the button is positioned with spacing from the primary action buttons
10. Take a screenshot showing the Generate Query button

### Test Query Generation - Happy Path
11. Click the "Generate Query" button
12. **Verify** the button shows a loading state (disabled with loading spinner)
13. **Verify** a natural language query is generated and populated in the input field
14. **Verify** the generated query is limited to two sentences maximum
15. Take a screenshot of the generated query in the input field
16. **Verify** the button returns to normal state after generation completes

### Test Query Overwrite Behavior
17. Manually type some text in the query input field
18. Take a screenshot of the manually entered text
19. Click the "Generate Query" button again
20. **Verify** the manually entered text is completely overwritten by the generated query
21. **Verify** no remnants of the previous text remain
22. Take a screenshot showing the overwritten query

### Test Generated Query Execution
23. With a generated query in the input field, click the "Query" button
24. **Verify** the generated query executes successfully
25. **Verify** results are displayed
26. **Verify** the SQL translation is shown
27. Take a screenshot of the executed query results

### Test Error Handling - No Tables
28. Remove all tables from the database (click X on all table items)
29. **Verify** no tables are shown in the "Available Tables" section
30. Click the "Generate Query" button
31. **Verify** an appropriate error message is displayed
32. **Verify** the error message mentions "no tables available" or similar
33. Take a screenshot of the error message
34. **Verify** the button returns to normal state

### Test Loading State Prevention
35. Upload sample data again to have tables available
36. Click the "Generate Query" button
37. Immediately click it again while it's loading
38. **Verify** the second click has no effect (button remains disabled during loading)
39. **Verify** only one query is generated
40. Take a screenshot showing the final state

### Test Multiple Generations Produce Different Queries
41. Click the "Generate Query" button
42. Note the generated query text
43. Click the "Generate Query" button again
44. **Verify** a new query is generated (may be different due to LLM variability)
45. Take a screenshot of the second generated query

## Success Criteria
- Generate Query button is visible and properly styled
- Button shows loading state during generation
- Generated queries populate the input field
- Generated queries are limited to two sentences maximum
- Existing content in input field is overwritten
- Generated queries can be executed successfully
- Error handling works when no tables are available
- Button cannot be clicked multiple times while loading
- All 10 screenshots are taken successfully

## Expected Behavior Notes
- The generated query should be contextually relevant to the available tables
- The query should use natural language, not SQL syntax
- The query should be realistic (like a user would actually type)
- Loading state should prevent concurrent requests
- Focus should move to the input field after generation
