# Feature: Generate Natural Language Queries

## Feature Description
Add a new button to the Natural Language SQL Interface that generates interesting natural language queries based on the existing database tables and their structure. When clicked, this button will use the LLM to create contextually relevant query suggestions and automatically populate the query input field with the generated text, overwriting any existing content. This feature helps users discover what questions they can ask about their data and provides a starting point for exploration.

## User Story
As a user
I want a button that generates suggested natural language queries based on my loaded tables
So that I can discover interesting questions to ask about my data without having to think of queries from scratch

## Problem Statement
Users often don't know what questions to ask about their data when they first load it into the application. They may be unfamiliar with the data structure or unsure what insights are possible. This creates friction in the user experience and may lead to underutilization of the application's capabilities.

## Solution Statement
Implement a "Generate Query" button that:
1. Analyzes the current database schema (tables and their column structures)
2. Uses the existing LLM processor to generate contextually relevant natural language queries
3. Limits generated queries to two sentences maximum for simplicity
4. Automatically populates the query input field, overwriting any existing text
5. Follows the existing UI patterns (Upload Data button style) and is positioned with space-between alignment from other primary buttons

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains LLM integration logic with OpenAI and Anthropic that will be extended to generate natural language queries based on schema
- `app/server/core/sql_processor.py` - Contains `get_database_schema()` function that provides table and column information
- `app/server/server.py` - FastAPI server where we'll add a new endpoint `/api/generate-query` to handle query generation requests
- `app/server/core/data_models.py` - Data models where we'll add request/response models for the new endpoint
- `app/client/src/main.ts` - Frontend TypeScript code where we'll add button click handler and API call logic
- `app/client/index.html` - HTML structure where we'll add the new "Generate Query" button
- `app/client/src/style.css` - CSS styling (may need minor adjustments for button positioning)
- `app/client/src/api/client.ts` - API client where we'll add the new endpoint function
- `app/client/src/types.d.ts` - TypeScript type definitions where we'll add types for the new API

### New Files
- `.claude/commands/e2e/test_generate_query.md` - E2E test file to validate the query generation feature works correctly
- `app/server/tests/test_generate_query.py` - Unit tests for the query generation endpoint

## Implementation Plan
### Phase 1: Foundation
Create the backend infrastructure for query generation. This includes adding the new API endpoint, data models, and LLM processing function that analyzes database schema and generates contextually relevant natural language queries.

### Phase 2: Core Implementation
Implement the frontend button and integration logic. Add the "Generate Query" button to the UI with proper styling and positioning, connect it to the backend API, and ensure it properly populates the query input field.

### Phase 3: Integration
Add comprehensive testing (unit tests and E2E tests), ensure error handling works correctly, and validate the feature integrates seamlessly with existing functionality without causing regressions.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Data Models for Query Generation
- Open `app/server/core/data_models.py`
- Add `GenerateQueryRequest` model with optional `llm_provider` field (defaults to "openai")
- Add `GenerateQueryResponse` model with `query` (string), `tables_analyzed` (list of strings), and optional `error` field
- Follow existing patterns in the file for consistency

### Step 2: Implement LLM Query Generation Function
- Open `app/server/core/llm_processor.py`
- Add `generate_natural_language_query()` function that takes schema_info and llm_provider as parameters
- Create a prompt that instructs the LLM to generate an interesting natural language query based on the provided tables and columns
- Specify in the prompt: limit to 2 sentences maximum, make it relevant to the actual data structure, avoid generic queries
- Use the existing `generate_sql_with_openai()` or `generate_sql_with_anthropic()` pattern for LLM routing
- Return only the generated query text (clean up any markdown or extra formatting)
- Add proper error handling with descriptive messages

### Step 3: Create API Endpoint for Query Generation
- Open `app/server/server.py`
- Import the new data models and `generate_natural_language_query` function
- Add new `POST /api/generate-query` endpoint with `GenerateQueryResponse` response model
- Endpoint should: get database schema, check if tables exist (return error if none), call the LLM generation function, and return the result
- Follow existing endpoint patterns (error handling, logging, try-catch structure)
- Log successful query generation with INFO level

### Step 4: Add Frontend API Client Function
- Open `app/client/src/api/client.ts`
- Add `generateQuery()` function that calls `POST /api/generate-query`
- Follow existing patterns in the file (error handling, fetch configuration)
- Return the response data

### Step 5: Add TypeScript Type Definitions
- Open `app/client/src/types.d.ts`
- Add `GenerateQueryResponse` interface matching the backend model
- Ensure it's available globally

### Step 6: Add "Generate Query" Button to UI
- Open `app/client/index.html`
- Locate the query controls section (contains Query button and Upload Data button)
- Add new button with id `generate-query-button` and class `secondary-button`
- Button text should be "Generate Query"
- Update the `.query-controls` CSS to use `justify-content: space-between` to separate primary and secondary buttons visually
- Position: Query button on left, Generate Query and Upload Data buttons on right with spacing

### Step 7: Implement Button Click Handler
- Open `app/client/src/main.ts`
- Add `initializeGenerateQuery()` function
- Get reference to the generate query button and query input field
- On button click: disable button, show loading state, call `api.generateQuery()`, populate query input with result (overwriting existing content), handle errors by displaying them
- Ensure button is re-enabled after success or failure
- Call `initializeGenerateQuery()` in the DOMContentLoaded event listener

### Step 8: Add Unit Tests
- Create `app/server/tests/test_generate_query.py`
- Test successful query generation with mock schema
- Test error handling when no tables exist
- Test error handling when LLM API fails
- Test that query length is reasonable (not empty, not too long)
- Mock LLM API calls to avoid actual API usage during tests
- Follow existing test patterns in the test directory

### Step 9: Create E2E Test Specification
- Create `.claude/commands/e2e/test_generate_query.md`
- Follow the format from `.claude/commands/e2e/test_basic_query.md`
- User Story: As a user, I want to generate natural language queries based on my data, so that I can discover interesting questions to ask
- Test Steps: Navigate to app, verify Generate Query button is present, upload sample data (users.json), click Generate Query button, verify query input is populated with text (2 sentences or less), verify button shows loading state, take screenshots
- Success Criteria: Button exists, button triggers query generation, query field is populated with generated text, no errors occur
- Include screenshots: initial state, after clicking Generate Query, populated query field

### Step 10: Update CSS Styling (if needed)
- Open `app/client/src/style.css`
- Verify `.query-controls` uses `justify-content: space-between` for proper button spacing
- Verify `.secondary-button` styling matches Upload Data button
- Make any minor adjustments needed for visual consistency

### Step 11: Run Validation Commands
- Execute all validation commands listed in the Validation Commands section
- Ensure zero errors and zero regressions
- Fix any issues that arise before marking the feature complete

## Testing Strategy
### Unit Tests
- Test query generation endpoint with valid schema
- Test query generation endpoint with empty database (no tables)
- Test LLM routing logic (OpenAI vs Anthropic)
- Test error handling for LLM API failures
- Mock LLM API calls to ensure tests run without external dependencies
- Verify generated queries are not empty and are reasonable length

### Edge Cases
- No tables loaded in database (should return error message)
- LLM API key not configured (should return appropriate error)
- Network timeout when calling LLM API (should handle gracefully)
- User clicks Generate Query button multiple times rapidly (should handle with proper state management)
- Generated query is empty or malformed (should handle and retry or show error)
- Query input field already has text (should overwrite as specified)

## Acceptance Criteria
- A "Generate Query" button is visible in the UI next to the Upload Data button
- Button follows the Upload Data button style (secondary-button class)
- Button is positioned with `justify-content: space-between` to visually separate from primary Query button
- Clicking the button disables it and shows a loading state
- After successful generation, the query input field is populated with an interesting natural language query
- Generated query is limited to two sentences maximum
- Any existing text in the query input field is overwritten
- If no tables are loaded, an appropriate error message is displayed
- Button re-enables after generation completes (success or failure)
- Query generation uses the existing LLM processor with OpenAI or Anthropic
- Query is contextually relevant to the actual tables and columns in the database
- All existing functionality continues to work without regression
- Unit tests pass with 100% coverage of new code
- E2E test validates the feature works end-to-end

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/test_generate_query.py -v` - Run new unit tests for query generation endpoint
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript type checking
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test file `.claude/commands/e2e/test_generate_query.md` to validate the query generation feature works end-to-end

## Notes
- The generated queries should be interesting and demonstrate the capabilities of the data (e.g., "Show me users who signed up in the last week" or "What are the top 5 most expensive products in the inventory?")
- Avoid generic queries like "Show me all data from the table" - make them specific to the column types and relationships
- The LLM prompt should encourage questions that showcase aggregations, filtering, or time-based queries when appropriate columns exist
- Consider suggesting multi-table queries when multiple tables are loaded with potential relationships
- The feature should work with both OpenAI and Anthropic LLM providers based on available API keys
- Error messages should be user-friendly and actionable (e.g., "Please upload data first before generating queries")
- The loading state should provide clear feedback that generation is in progress
- Future enhancement idea: Allow users to click Generate Query multiple times to get different suggestions
