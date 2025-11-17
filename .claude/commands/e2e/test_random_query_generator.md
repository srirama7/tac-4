# E2E Test: Random Query Generator

Test the random query generation functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want to generate random natural language queries based on my existing tables
So that I can discover interesting ways to query my data and get inspiration for data exploration

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** the "Generate Random Query" button is present and visible
5. Click the "Upload Data" button
6. Load sample data by clicking the "Users Data" sample button
7. **Verify** the "users" table appears in the Available Tables section
8. Take a screenshot after data upload
9. Click the "Generate Random Query" button
10. **Verify** the button shows a loading state (disabled with spinner)
11. Wait for the query to be generated (up to 5 seconds)
12. **Verify** the query input field is populated with text
13. **Verify** the generated query is:
    - Not empty
    - Contains relevant keywords related to the users table (e.g., "users", "name", "email", "age", "created_at")
    - Is written in natural language (not SQL)
    - Is two sentences maximum
14. Take a screenshot of the populated query input field
15. Clear the query input
16. Click the "Generate Random Query" button again
17. **Verify** a new query is generated (should be different from the first one due to temperature=0.9)
18. Take a screenshot of the second generated query
19. Test error handling: Delete all tables
20. Click the "Generate Random Query" button
21. **Verify** an error message is displayed: "No tables found in database"
22. Take a screenshot of the error state

## Success Criteria
- Generate Random Query button is visible and clickable
- Button shows loading state during query generation
- Query input field is populated with a relevant natural language query
- Generated queries are contextual to the database schema
- Generated queries are limited to two sentences
- Multiple clicks generate different queries
- Error handling works correctly when no tables exist
- 5 screenshots are taken: initial state, after upload, first query, second query, error state

## Expected Results
- The generated query should be relevant to the users table structure
- Example queries might include:
  - "What is the average age of all users?"
  - "Show me users who signed up in the last month."
  - "How many users have gmail email addresses?"
  - "What are the top 5 oldest users by age?"
