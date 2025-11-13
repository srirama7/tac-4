# Feature: Natural Language Query Generator Button

## Feature Description
Add a new button to the UI that automatically generates interesting natural language queries based on the existing database tables and their structure. When clicked, the button will use the LLM to analyze the available tables and columns, create a compelling natural language query suggestion (limited to two sentences), and populate the query input field, overwriting any existing content. This feature helps users explore their data by providing contextual query suggestions.

## User Story
As a user
I want to click a button that generates interesting query suggestions based on my uploaded data
So that I can quickly explore my data without thinking of queries myself

## Problem Statement
Users may not know what questions to ask about their uploaded data, especially when working with new datasets. They need inspiration and guidance to discover insights within their data. Currently, users must come up with their own natural language queries, which can be challenging when they're unfamiliar with the dataset structure or don't know what questions would yield interesting results.

## Solution Statement
Create a "Generate Query" button positioned alongside existing primary buttons that leverages the existing `llm_processor.py` module to analyze the current database schema (tables, columns, and row counts) and generate contextually relevant, interesting natural language queries. The generated query will be automatically inserted into the query input field, replacing any existing text, allowing users to execute it immediately or modify it as needed. The query suggestions will be limited to two sentences maximum for clarity and conciseness.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - Main FastAPI server file where we'll add a new `/api/generate-query` endpoint to handle query generation requests
- `app/server/core/llm_processor.py` - Contains the LLM integration logic; we'll add a new function to generate natural language queries based on database schema
- `app/server/core/data_models.py` - Define new Pydantic models for the generate query request/response
- `app/server/core/sql_processor.py` - Contains `get_database_schema()` function which we'll use to fetch current table information
- `app/client/src/main.ts` - Main frontend TypeScript file where we'll add the button, event handler, and API call
- `app/client/src/api/client.ts` - API client where we'll add the new API call method
- `app/client/src/style.css` - Styles where we'll ensure the button matches the "Upload Data" button style
- `app/client/index.html` - HTML structure where we'll add the new button to the query controls section
- `app/server/tests/core/test_llm_processor.py` - Existing test file where we'll add unit tests for the new query generation function
- `.claude/commands/test_e2e.md` - E2E test runner documentation for understanding test creation
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test for reference

### New Files

- `app/server/tests/test_generate_query_api.py` - New test file for testing the generate query API endpoint
- `.claude/commands/e2e/test_generate_query.md` - New E2E test file to validate the query generation button works end-to-end

## Implementation Plan

### Phase 1: Foundation
First, we'll establish the backend infrastructure by creating new data models for the query generation feature and adding a utility function to the LLM processor that can analyze database schemas and generate interesting natural language queries. This includes setting up proper error handling and validation.

### Phase 2: Core Implementation
Implement the core functionality including:
1. A new FastAPI endpoint (`/api/generate-query`) that retrieves the current database schema and calls the LLM to generate a natural language query
2. Frontend button and event handling to trigger the query generation
3. API integration to connect the frontend button to the backend endpoint
4. UI updates to populate the query input field with the generated query

### Phase 3: Integration
Integrate the new button into the existing UI layout, ensuring it follows the same visual style as the "Upload Data" button and is positioned appropriately with the other primary controls. Add comprehensive tests to validate the feature works correctly and create E2E tests to ensure the complete user flow functions as expected.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Backend Data Models
- Add new Pydantic models to `app/server/core/data_models.py`:
  - `GenerateQueryRequest` - Request model (can be empty as it uses current schema)
  - `GenerateQueryResponse` - Response model with fields: `query` (str), `error` (Optional[str])

### Step 2: LLM Processor Query Generation Function
- Add a new function `generate_natural_language_query()` to `app/server/core/llm_processor.py`:
  - Accept `schema_info` parameter (database schema dictionary)
  - Format the schema into a prompt that asks the LLM to generate an interesting natural language query
  - Include prompt instructions to:
    - Generate a query that explores interesting patterns in the data
    - Limit the query to two sentences maximum
    - Make it specific to the available tables and columns
    - Return only the natural language query, no explanations
  - Use the existing routing logic to determine which LLM provider to use (OpenAI or Anthropic)
  - Return the generated query string
  - Handle errors gracefully with descriptive error messages

### Step 3: Backend API Endpoint
- Add new endpoint to `app/server/server.py`:
  - Route: `POST /api/generate-query`
  - Response model: `GenerateQueryResponse`
  - Endpoint should:
    - Get current database schema using `get_database_schema()`
    - Check if tables exist (return error if no tables are available)
    - Call `generate_natural_language_query()` with schema info
    - Return the generated query in the response
    - Log the operation for debugging
    - Handle exceptions and return errors in the response model

### Step 4: Backend Unit Tests
- Add unit tests to `app/server/tests/core/test_llm_processor.py`:
  - Test `generate_natural_language_query()` with valid schema
  - Test with empty schema (should handle gracefully)
  - Test with multiple tables
  - Verify query length constraints
  - Mock LLM API calls to avoid actual API usage in tests
- Create new test file `app/server/tests/test_generate_query_api.py`:
  - Test `/api/generate-query` endpoint success case
  - Test endpoint when no tables exist
  - Test error handling
  - Use FastAPI TestClient for integration testing

### Step 5: Frontend API Client
- Add new API method to `app/client/src/api/client.ts`:
  - Method name: `generateQuery()`
  - HTTP method: POST to `/api/generate-query`
  - Return type: Promise with generated query response
  - Include proper error handling

### Step 6: Frontend Button and UI
- Update `app/client/index.html`:
  - Add new button with id `generate-query-button` to the `.query-controls` section
  - Position it after the "Upload Data" button using CSS
  - Button text: "Generate Query"
  - Apply class `secondary-button` to match "Upload Data" style
- Update `app/client/src/style.css`:
  - Add any necessary styles to ensure proper spacing between buttons
  - Use `justify-content: space-between` or similar to space the buttons apart as requested

### Step 7: Frontend Button Functionality
- Update `app/client/src/main.ts`:
  - Add initialization function `initializeGenerateQuery()`
  - Get reference to the `generate-query-button` element
  - Add click event listener that:
    - Disables the button and shows loading state
    - Calls `api.generateQuery()`
    - On success: populates the query input field with the generated query (using `.value` to overwrite)
    - On error: displays error message using existing `displayError()` function
    - Re-enables the button in finally block
  - Call `initializeGenerateQuery()` in the `DOMContentLoaded` event listener

### Step 8: Create E2E Test File
- Create new E2E test file `.claude/commands/e2e/test_generate_query.md` based on the format from `test_basic_query.md`:
  - User Story: User wants to generate query suggestions
  - Test Steps:
    1. Navigate to application URL
    2. Take screenshot of initial state
    3. Verify "Generate Query" button is present
    4. Click "Generate Query" button
    5. Verify query input field is populated with text
    6. Verify the query is maximum two sentences
    7. Take screenshot of populated query
    8. Click "Query" button to execute the generated query
    9. Verify results appear
    10. Take screenshot of results
  - Success Criteria: Button works, query is generated, query executes successfully, screenshots captured

### Step 9: Run Backend Tests
- Run all backend unit tests to ensure no regressions:
  - `cd app/server && uv run pytest tests/core/test_llm_processor.py -v`
  - `cd app/server && uv run pytest tests/test_generate_query_api.py -v`
  - Verify all new tests pass
  - Verify existing tests still pass

### Step 10: Run Frontend Type Check and Build
- Run TypeScript type checking:
  - `cd app/client && bun tsc --noEmit`
  - Fix any type errors that appear
- Run frontend build:
  - `cd app/client && bun run build`
  - Verify build completes successfully

### Step 11: Manual Testing
- Start both server and client using `./scripts/start.sh`
- Upload sample data using the "Upload Data" button
- Click the "Generate Query" button
- Verify the query input field is populated with an interesting query
- Click "Generate Query" multiple times to see different suggestions
- Execute the generated query to ensure it works
- Test with different datasets (users, products, events)
- Test error case: click "Generate Query" when no tables exist

### Step 12: Run E2E Test
- Read `.claude/commands/test_e2e.md` to understand E2E test execution
- Execute the new E2E test file `.claude/commands/e2e/test_generate_query.md`
- Verify all test steps pass
- Review screenshots to confirm functionality
- If any issues found, fix and re-test

### Step 13: Final Validation
- Run all validation commands from the Validation Commands section below
- Ensure zero errors and zero regressions
- Verify feature works as expected from user perspective

## Testing Strategy

### Unit Tests
1. **LLM Processor Tests** (`test_llm_processor.py`):
   - Test `generate_natural_language_query()` with various schema configurations
   - Mock API calls to avoid dependencies on external services
   - Test query length validation (maximum two sentences)
   - Test with empty/invalid schemas
   - Verify proper error handling

2. **API Endpoint Tests** (`test_generate_query_api.py`):
   - Test successful query generation
   - Test error when no tables exist
   - Test error handling for LLM failures
   - Verify response model structure
   - Test with different LLM providers (OpenAI/Anthropic)

3. **Integration Tests**:
   - Test full flow from API call to response
   - Verify database schema retrieval integration
   - Test with real database state

### Edge Cases
- No tables exist in database (should return friendly error)
- Empty tables (tables with no data)
- Single table with few columns
- Multiple tables with complex schemas
- LLM API failure or timeout
- LLM returns query exceeding two sentences (should truncate or regenerate)
- User clicks button multiple times rapidly (should handle gracefully with disabled state)
- Network failure during API call
- Invalid API keys for LLM providers

## Acceptance Criteria
1. A "Generate Query" button exists in the UI, styled consistently with the "Upload Data" button
2. The button is positioned with appropriate spacing from other primary buttons (justify-content: space-between or similar)
3. Clicking the button triggers an API call to `/api/generate-query`
4. The backend endpoint successfully retrieves the database schema and generates a natural language query using the LLM
5. The generated query is limited to a maximum of two sentences
6. The query input field is populated with the generated query, overwriting any existing content
7. Loading state is shown while generating (button disabled with loading indicator)
8. Error messages are displayed appropriately when generation fails
9. When no tables exist, a user-friendly error message is shown
10. The generated queries are contextually relevant to the uploaded data
11. Users can click the button multiple times to get different query suggestions
12. All existing functionality continues to work without regression
13. All unit tests pass
14. All E2E tests pass
15. TypeScript compilation succeeds without errors
16. Frontend build completes successfully

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_generate_query.md` test file to validate this functionality works
- `cd app/server && uv run pytest tests/core/test_llm_processor.py -v` - Verify new LLM processor tests pass
- `cd app/server && uv run pytest tests/test_generate_query_api.py -v` - Verify new API endpoint tests pass
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Implementation Details
- The feature leverages the existing `llm_processor.py` architecture, maintaining consistency with the current codebase patterns
- Uses the same LLM routing logic as query processing (OpenAI priority, then Anthropic)
- The two-sentence limit should be enforced in the prompt to the LLM, with fallback truncation if needed
- Consider caching or rate limiting if users click the button repeatedly

### Future Enhancements
- Add a dropdown to generate queries for specific tables (currently generates for all tables)
- Provide multiple query suggestions at once for users to choose from
- Remember previously generated queries to avoid duplicates
- Add query categories (aggregations, filters, joins, etc.)
- Implement query favorites/bookmarking
- Add "Surprise Me" mode that also executes the query automatically

### UI/UX Considerations
- The button should be clearly labeled and discoverable
- Loading state is important since LLM calls can take a few seconds
- Consider adding a tooltip explaining what the button does
- The generated query should be immediately editable by the user
- Button should be disabled when no tables are loaded (optional enhancement)

### Security Notes
- API endpoint should use the same SQL injection protection as query processing
- Rate limiting should be considered to prevent API abuse
- LLM prompt should be carefully crafted to avoid prompt injection
- No sensitive data should be included in LLM prompts (only schema info, not actual data)
