# Feature: Random Natural Language Query Generator

## Feature Description
This feature adds a "Generate Random Query" button that automatically creates interesting natural language queries based on the existing database tables and their structure. When clicked, the button uses the LLM processor to analyze available tables and columns, then generates a creative, two-sentence maximum query that showcases the data. The generated query automatically overwrites the query input field, allowing users to execute it manually. This feature helps users discover query possibilities and provides inspiration for interacting with their data.

## User Story
As a user
I want to generate random natural language queries based on my existing tables
So that I can discover interesting ways to query my data and get inspiration for data exploration without having to think of queries myself

## Problem Statement
Users may not always know what questions to ask about their data, especially when working with new datasets. They need inspiration and examples of meaningful queries that work with their specific table structures. Currently, users must manually type every query, which can be tedious during data exploration and doesn't help users understand what types of questions they can ask.

## Solution Statement
Implement a "Generate Random Query" button that leverages the existing `llm_processor.py` module to create contextual natural language queries. The system will:
1. Retrieve the current database schema (tables, columns, types, row counts)
2. Send this schema information to the LLM with a specialized prompt to generate interesting queries
3. Generate diverse query types (aggregations, filters, joins, time-based, comparisons)
4. Limit query text to two sentences maximum for clarity
5. Populate the query input field, overwriting any existing content
6. Style the button using the existing "Upload Data" button pattern with appropriate spacing

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains LLM integration functions for OpenAI and Anthropic. Will be extended with a new `generate_random_query()` function that creates natural language queries based on schema information.

- `app/server/core/sql_processor.py` - Contains `get_database_schema()` function that retrieves table and column information. This will be used to provide context to the LLM for query generation.

- `app/server/core/data_models.py` - Contains Pydantic models for API requests/responses. Will need new `RandomQueryRequest` and `RandomQueryResponse` models.

- `app/server/server.py` - FastAPI server with endpoint definitions. Will need a new `POST /api/generate-query` endpoint to handle random query generation requests.

- `app/client/src/main.ts` - Main TypeScript file with UI initialization and event handlers. Will need to add initialization for the new "Generate Random Query" button and its click handler.

- `app/client/src/api/client.ts` - API client with typed request methods. Will need a new `generateRandomQuery()` method to call the backend endpoint.

- `app/client/index.html` - HTML structure with UI elements. Will need to add the new button in the query controls section.

- `app/client/src/style.css` - Stylesheet with component styles. May need minor adjustments for button layout and spacing.

- `app/client/src/types.d.ts` - TypeScript type definitions. Will need new type definitions for `RandomQueryRequest` and `RandomQueryResponse`.

- `README.md` - Project documentation. Will need to be updated with information about the new Generate Random Query feature.

### New Files

- `.claude/commands/e2e/test_random_query_generator.md` - E2E test file to validate the random query generator feature works end-to-end with browser automation.

- `app/server/tests/core/test_random_query_generator.py` - Unit tests for the random query generation functionality, testing various schema scenarios and edge cases.

## Implementation Plan

### Phase 1: Foundation
First, we'll extend the backend infrastructure to support random query generation:
1. Add new data models (`RandomQueryRequest`, `RandomQueryResponse`) to define the API contract
2. Implement the core `generate_random_query()` function in `llm_processor.py` that uses schema information to create diverse, interesting natural language queries
3. Create a new FastAPI endpoint `/api/generate-query` that retrieves schema and calls the generation function
4. Write comprehensive unit tests to ensure query generation works correctly across various schema scenarios

### Phase 2: Core Implementation
Next, we'll build the frontend integration:
1. Add TypeScript type definitions for the new API request/response models
2. Implement the API client method `generateRandomQuery()` to communicate with the backend
3. Add the "Generate Random Query" button to the HTML with appropriate styling and positioning
4. Implement the click handler that calls the API and populates the input field
5. Add loading states and error handling for a smooth user experience

### Phase 3: Integration
Finally, we'll integrate the feature with existing functionality and validate:
1. Ensure the button layout works responsively with existing buttons (Query, Upload Data)
2. Create an E2E test to validate the feature works correctly in a real browser environment
3. Update project documentation (README.md) to describe the new feature
4. Run all validation commands to ensure zero regressions
5. Test with various database schemas to ensure query variety and quality

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Backend Data Models
- Open `app/server/core/data_models.py`
- Add `RandomQueryRequest` model (empty model, no input parameters needed)
- Add `RandomQueryResponse` model with fields: `query` (str), `error` (Optional[str])
- Ensure models follow existing Pydantic patterns in the file

### 2. Backend Query Generation Logic
- Open `app/server/core/llm_processor.py`
- Create new function `generate_random_query(schema_info: Dict[str, Any]) -> str`
- Implement logic to route to OpenAI or Anthropic based on available API keys (same pattern as `generate_sql()`)
- Create `generate_random_query_with_openai()` function that:
  - Formats schema information into a clear prompt
  - Asks the LLM to generate an interesting natural language query
  - Emphasizes variety (aggregations, filters, joins, time-based queries)
  - Limits output to two sentences maximum
  - Returns only the natural language query text
- Create `generate_random_query_with_anthropic()` function with equivalent logic
- Use temperature=0.9 for creative variety in query generation
- Handle errors gracefully with meaningful error messages

### 3. Backend Unit Tests
- Create `app/server/tests/core/test_random_query_generator.py`
- Test `generate_random_query()` with:
  - Empty schema (no tables)
  - Single table with various column types
  - Multiple tables for join opportunities
  - Tables with date/time columns for temporal queries
  - Tables with numeric columns for aggregation queries
- Verify queries are limited to two sentences maximum
- Mock LLM responses to avoid actual API calls in tests
- Test error handling when API keys are missing

### 4. Backend API Endpoint
- Open `app/server/server.py`
- Create new endpoint `POST /api/generate-query` with response model `RandomQueryResponse`
- Implement endpoint logic:
  - Get database schema using `get_database_schema()`
  - Check if any tables exist (return error if database is empty)
  - Call `generate_random_query()` with schema information
  - Return `RandomQueryResponse` with generated query
  - Handle exceptions and return error messages
  - Add logging for success and failure cases
- Follow existing endpoint patterns for consistency

### 5. Frontend Type Definitions
- Open `app/client/src/types.d.ts`
- Add `RandomQueryRequest` interface (empty interface, no fields)
- Add `RandomQueryResponse` interface matching backend model
- Ensure types match the Pydantic models exactly

### 6. Frontend API Client Method
- Open `app/client/src/api/client.ts`
- Add `generateRandomQuery()` method to the `api` object
- Implement method to call `POST /api/generate-query`
- Return typed `Promise<RandomQueryResponse>`
- Follow existing API method patterns

### 7. Frontend HTML Structure
- Open `app/client/index.html`
- Locate the `.query-controls` div (contains Query and Upload Data buttons)
- Add new button after the Query button:
  - ID: `generate-query-button`
  - Class: `secondary-button`
  - Text: "Generate Random Query"
- Use `justify-content: space-between` or similar to space the Generate button apart from primary buttons

### 8. Frontend CSS Styling
- Open `app/client/src/style.css`
- Verify `.secondary-button` style matches Upload Data button
- Update `.query-controls` styling if needed to properly space three buttons
- Consider using flexbox with `justify-content: space-between` or gap adjustment
- Ensure responsive layout works on smaller screens

### 9. Frontend Event Handler
- Open `app/client/src/main.ts`
- In `initializeQueryInput()` function, add event listener for `generate-query-button`
- Implement click handler that:
  - Disables the button and shows loading state
  - Calls `api.generateRandomQuery()`
  - On success: overwrites `queryInput.value` with the generated query
  - On error: displays error message using existing `displayError()` function
  - Re-enables button in finally block
- Add appropriate loading indicator (spinner) like other buttons

### 10. Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand E2E test structure
- Read `.claude/commands/e2e/test_basic_query.md` for reference
- Create `.claude/commands/e2e/test_random_query_generator.md`
- Define test that:
  - Navigates to the application
  - Uploads sample data (users.json)
  - Verifies "Generate Random Query" button is visible
  - Clicks the button
  - Verifies the query input field is populated with text
  - Verifies the query is relevant to the uploaded tables
  - Takes 3 screenshots: initial state, after button click, populated input field
- Follow the same format as existing E2E test files

### 11. Update Documentation
- Open `README.md`
- Add bullet point to Features section: "🎲 Random query generation for data exploration inspiration"
- Add description in Usage section explaining the Generate Random Query button
- Note that it generates contextual queries based on current database tables

### 12. Run Validation Commands
- Execute all validation commands listed below to ensure the feature works correctly with zero regressions
- Fix any issues that arise before considering the feature complete

## Testing Strategy

### Unit Tests
- **Empty Database Test**: Verify appropriate error message when no tables exist
- **Single Table Test**: Generate queries for a table with mixed column types (text, integer, date)
- **Multiple Tables Test**: Generate queries that might include JOINs when related tables exist
- **Numeric Columns Test**: Verify queries include aggregations (SUM, AVG, COUNT, MAX, MIN) when appropriate
- **Date Columns Test**: Verify queries include temporal filters ("last week", "this month") when date columns exist
- **Query Length Test**: Verify all generated queries are limited to two sentences maximum
- **Error Handling Test**: Test behavior when LLM API calls fail
- **Provider Routing Test**: Verify correct routing between OpenAI and Anthropic based on API key availability

### Edge Cases
- Database with no tables (should return helpful error message)
- Database with only one table and one column (should still generate a simple query)
- Table with unusual but valid column names (spaces, special characters)
- Very large schemas (many tables and columns) - ensure prompt doesn't exceed token limits
- API key not configured (should return clear error message)
- LLM returns a query longer than two sentences (should truncate or regenerate)
- Multiple rapid clicks on the Generate button (should handle gracefully with button disabling)
- Generated query contains SQL instead of natural language (should validate and regenerate)

## Acceptance Criteria
- Generate Random Query button is visible and styled like Upload Data button
- Button is positioned with space-between layout, separated from Query and Upload Data buttons
- Clicking the button calls the backend API to generate a query
- Generated queries are based on actual database table structures and columns
- Generated queries are limited to two sentences maximum
- Generated query overwrites any existing text in the query input field
- Loading state is shown while generating (button disabled, spinner visible)
- Errors are displayed clearly to the user if generation fails
- Button works correctly when database is empty (shows error message)
- Generated queries are varied and interesting (not the same query every time)
- All existing functionality remains working (zero regressions)
- E2E test validates the feature works in a real browser environment
- Unit tests cover all major scenarios and edge cases
- Documentation is updated to reflect the new feature

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

1. Read `.claude/commands/test_e2e.md` to understand how to run E2E tests
2. Read and execute `.claude/commands/e2e/test_random_query_generator.md` to validate the feature works end-to-end
3. `cd app/server && uv run pytest tests/core/test_random_query_generator.py -v` - Run new unit tests
4. `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
5. `cd app/client && bun run build` - Run frontend build to validate no TypeScript errors
6. `cd app/client && bun tsc --noEmit` - Run TypeScript compiler to validate type safety
7. Manual testing:
   - Start the application with `./scripts/start.sh`
   - Upload sample data (users.json)
   - Click "Generate Random Query" button multiple times
   - Verify each query is different and contextually relevant
   - Verify query input field is populated correctly each time
   - Test with empty database and verify error handling
   - Test with multiple tables and verify join queries are generated

## Notes

### LLM Provider Considerations
- Follow the same routing logic as `generate_sql()` in `llm_processor.py`
- Priority: OpenAI API key exists first, then Anthropic, then request preference
- Use appropriate models: `gpt-4-turbo-preview` for OpenAI, `claude-3-haiku-20240307` for Anthropic
- Use higher temperature (0.9) for creative variety in query generation vs SQL generation (0.1)

### Query Generation Strategy
The prompt to the LLM should encourage variety by:
- Requesting different query types: aggregations, filters, comparisons, joins, time-based
- Providing context about data types to suggest appropriate operations
- Asking for "interesting" or "insightful" queries rather than generic ones
- Specifying two-sentence maximum constraint clearly
- Avoiding overly complex queries that would confuse users

### UI/UX Considerations
- Button should be clearly labeled to indicate it generates queries, not executes them
- Loading state is important since LLM calls can take 1-3 seconds
- Overwriting the input field is intentional (as specified) but consider UX feedback
- Consider adding a tooltip or help text to explain the feature
- The "justify-content: space-between" layout keeps Generate button visually distinct from action buttons

### Future Enhancements (Out of Scope)
- Add a "history" of generated queries for users to browse
- Allow users to specify query type (e.g., "generate an aggregation query")
- Add a "refine query" button to iterate on a generated query
- Integrate query suggestions directly into the input field as autocomplete
- Generate multiple queries and let users choose their favorite

### Testing Notes
- Mock LLM API calls in unit tests to avoid actual API usage and costs
- E2E test should use real API to validate end-to-end integration
- Test with various schema complexities to ensure robust query generation
- Verify queries are actually executable by optionally running them through the query endpoint

### Dependencies
- No new Python packages needed (reuses existing OpenAI and Anthropic clients)
- No new frontend packages needed (vanilla TypeScript and existing API client)
- Leverages existing `llm_processor.py` patterns for consistency
