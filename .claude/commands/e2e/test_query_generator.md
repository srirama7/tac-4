# E2E Test: Query Generator Button

## User Story
As a user, I want to automatically generate interesting natural language queries based on my database structure so that I can quickly explore my data without having to think of queries myself and see what kinds of questions I can ask.

## Prerequisites
- Backend server is running on port 8000
- Frontend dev server is running on port 5173
- At least one of OPENAI_API_KEY or ANTHROPIC_API_KEY is configured in the environment

## Test Steps

### 1. Start Backend Server
Navigate to the backend directory and start the server:
```bash
cd app/server && uv run python server.py
```

Wait for the server to be ready (listen for "Application startup complete" message).

### 2. Start Frontend Dev Server
In a new terminal, navigate to the frontend directory and start the dev server:
```bash
cd app/client && bun run dev
```

Wait for the dev server to be ready (listen for "Local: http://localhost:5173" message).

### 3. Navigate to Application
Open browser and navigate to http://localhost:5173

### 4. Take Screenshot of Initial State
Take a screenshot showing the initial state of the application with the three buttons visible: "Query", "Generate Query", and "Upload Data".

**Screenshot name:** `01-initial-state.png`

### 5. Upload Sample Data
Click the "Upload Data" button and select a sample dataset (e.g., users.json or products.csv) to populate the database with tables.

Verify that the tables section shows the uploaded data.

**Screenshot name:** `02-data-uploaded.png`

### 6. Verify Generate Query Button is Present
Verify that the "Generate Query" button is visible and positioned between the "Query" button and "Upload Data" button.

Verify the button styling matches the "Upload Data" button (secondary button style).

Verify the buttons are spaced using `justify-content: space-between`.

### 7. Click Generate Query Button
Click the "Generate Query" button.

Verify that:
- The button shows a loading spinner while waiting for the API response
- The button is disabled during the API call

### 8. Wait for Query Input to be Populated
Wait for the query input field to be populated with a generated query suggestion.

Verify that:
- The query input field contains text
- The text is relevant to the uploaded database schema
- Any previous content in the input field has been overwritten

**Screenshot name:** `03-query-generated.png`

### 9. Verify Query is Reasonable
Read the generated query and verify that:
- It is no longer than 2 sentences
- It is contextually relevant to the available tables
- It is an interesting query (not just "show me all records")
- The query makes sense for the data structure

### 10. Click Generate Query Again
Click the "Generate Query" button again to generate a different query.

Verify that:
- A new query is generated and populates the input field
- The previous query is overwritten with the new one

**Screenshot name:** `04-second-query-generated.png`

### 11. Execute the Generated Query
Click the "Query" button to execute the generated query.

Verify that:
- The query executes successfully
- Results are displayed in the results section
- The SQL query is shown along with the natural language query
- The results table contains data

**Screenshot name:** `05-query-executed.png`

### 12. Test with No Tables (Edge Case)
Delete all tables from the database (use the X button on each table in the tables section).

Click the "Generate Query" button.

Verify that:
- An appropriate error message is displayed: "Please upload data first before generating queries"
- The button is re-enabled after the error
- No query is populated in the input field

**Screenshot name:** `06-error-no-tables.png`

### 13. Test Query Overwriting
Upload sample data again.

Manually type some text into the query input field (e.g., "test query").

Click the "Generate Query" button.

Verify that:
- The manually typed text is completely overwritten
- The input field contains only the generated query

**Screenshot name:** `07-overwrite-test.png`

## Success Criteria
- ✅ Generate Query button is visible and positioned correctly between Query and Upload Data buttons
- ✅ Button styling matches Upload Data button (secondary button style)
- ✅ Buttons are spaced with `justify-content: space-between`
- ✅ Clicking the button shows a loading state (spinner)
- ✅ Generated query populates the query input field
- ✅ Generated query overwrites any existing content in the input field
- ✅ Generated queries are contextually relevant to the database schema
- ✅ Generated queries are limited to 2 sentences or less
- ✅ Generated queries can be successfully executed by clicking the Query button
- ✅ Appropriate error message is shown when no tables are available
- ✅ Button is disabled during API call to prevent duplicate requests
- ✅ All screenshots captured successfully

## Cleanup
After testing, stop both servers:
- Press Ctrl+C in the backend terminal
- Press Ctrl+C in the frontend terminal

## Notes
- Generated queries are non-deterministic due to LLM variability, so each run may produce different queries
- If API keys are not configured, the test will fail with appropriate error messages
- The test validates the complete user workflow from button click to query execution
