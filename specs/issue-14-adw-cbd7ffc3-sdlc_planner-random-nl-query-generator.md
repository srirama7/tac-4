# Feature: Random Natural Language Query Generator

## Feature Description
A "Generate Random Query" button that automatically creates interesting natural language queries based on the existing database tables and their structure. When clicked, the button will use the LLM to generate contextually relevant queries (limited to two sentences maximum) and populate the query input field, overwriting any existing content. This feature helps users discover query capabilities and serves as a quick-start tool for exploring their data.

## User Story
As a user
I want to generate random natural language queries based on my loaded tables
So that I can quickly explore query examples and discover what questions I can ask about my data without having to think of queries myself

## Problem Statement
Users may not know what types of questions they can ask about their data, especially when first loading tables into the application. This creates a barrier to entry and reduces engagement with the natural language query feature. Users need inspiration and examples that are contextually relevant to their actual data structure.

## Solution Statement
Add a "Generate Random Query" button positioned with `justify-content: space-between` styling (separate from the primary Query button) that uses the existing `llm_processor.py` module to analyze the current database schema and generate interesting, contextually-aware natural language queries. The generated query (maximum two sentences) will automatically populate the query input field, replacing any existing text, allowing users to immediately execute it or modify it as needed.

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains LLM integration functions for OpenAI and Anthropic. Will be extended with a new function to generate random natural language queries based on table schemas
- `app/server/core/sql_processor.py` - Contains `get_database_schema()` function that retrieves all table information including columns, types, and row counts - will be used to provide context to the LLM
- `app/server/server.py` - FastAPI server with existing endpoints. Will add a new `POST /api/generate-random-query` endpoint
- `app/server/core/data_models.py` - Pydantic models for API requests/responses. Will add `RandomQueryRequest` and `RandomQueryResponse` models
- `app/client/index.html` - Main HTML structure with query input and buttons. Will add the new "Generate Random Query" button with appropriate styling
- `app/client/src/main.ts` - TypeScript application logic with event handlers. Will add event handler for the new button and API call
- `app/client/src/api/client.ts` - API client functions. Will add `generateRandomQuery()` function
- `app/client/src/style.css` - Styling definitions. Will add styling for the new button to match the "Upload Data" button style

### New Files
- `app/server/tests/core/test_random_query_generator.py` - Unit tests for the random query generation logic
- `.claude/commands/e2e/test_random_query_generator.md` - E2E test specification to validate the feature works end-to-end

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for random query generation by adding a new function to the LLM processor that can analyze database schemas and generate contextually relevant natural language queries. This includes creating the appropriate data models and API endpoint to expose this functionality.

### Phase 2: Core Implementation
Implement the frontend button and integrate it with the backend API. Add the button to the UI with appropriate styling (matching the "Upload Data" button), position it correctly using flexbox with space-between, and wire up the event handlers to call the backend and populate the query input field.

### Phase 3: Integration
Ensure the feature integrates seamlessly with existing functionality - the generated query should work with the existing query execution flow, handle edge cases (no tables loaded, API errors), and provide appropriate user feedback during generation.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create Backend Data Models
- Open `app/server/core/data_models.py`
- Add `RandomQueryRequest` model (empty/minimal - no required fields)
- Add `RandomQueryResponse` model with fields: `query` (str), `tables_analyzed` (List[str]), `error` (Optional[str])

### 2. Implement Random Query Generation in LLM Processor
- Open `app/server/core/llm_processor.py`
- Add new function `generate_random_query_with_openai(schema_info: Dict[str, Any]) -> str` that:
  - Takes database schema information
  - Constructs a prompt asking the LLM to generate an interesting natural language query based on the available tables
  - Specifies in the prompt: "Generate ONE interesting natural language question about this data. Limit to two sentences maximum. Make it specific to the actual tables and columns available."
  - Returns the generated query text
- Add new function `generate_random_query_with_anthropic(schema_info: Dict[str, Any]) -> str` with the same logic using Anthropic API
- Add new function `generate_random_query(schema_info: Dict[str, Any]) -> str` that routes to the appropriate provider (similar to the existing `generate_sql()` function)

### 3. Create API Endpoint for Random Query Generation
- Open `app/server/server.py`
- Import the new data models: `RandomQueryRequest`, `RandomQueryResponse`
- Import the new function from `llm_processor`: `generate_random_query`
- Add new endpoint `POST /api/generate-random-query` that:
  - Gets the current database schema using `get_database_schema()`
  - Validates that tables exist (if no tables, return error message)
  - Calls `generate_random_query(schema_info)` to generate the query
  - Returns `RandomQueryResponse` with the generated query and list of table names analyzed
  - Includes error handling with try/except and logging

### 4. Write Backend Unit Tests
- Create `app/server/tests/core/test_random_query_generator.py`
- Add test `test_generate_random_query_with_schema()` - tests successful query generation with sample schema
- Add test `test_generate_random_query_no_tables()` - tests behavior when no tables exist
- Add test `test_generate_random_query_api_error()` - tests error handling when LLM API fails
- Run tests: `cd app/server && uv run pytest tests/core/test_random_query_generator.py -v`

### 5. Add Frontend API Client Function
- Open `app/client/src/api/client.ts`
- Add new function `generateRandomQuery()` that:
  - Makes POST request to `/api/generate-random-query`
  - Returns Promise with the response data
  - Includes error handling

### 6. Add Generate Random Query Button to HTML
- Open `app/client/index.html`
- In the `.query-controls` div (around line 22), add new button after the "Upload Data" button:
  - Button ID: `generate-random-query-button`
  - Class: `secondary-button` (to match Upload Data button style)
  - Text: "Generate Random Query"

### 7. Update Query Controls CSS for Proper Spacing
- Open `app/client/src/style.css`
- Modify `.query-controls` styling to use `justify-content: space-between` to separate the primary button from the secondary buttons
- Ensure the layout groups "Query" button on the left and "Upload Data" + "Generate Random Query" buttons on the right
- Consider wrapping secondary buttons in a flex container if needed for proper grouping

### 8. Implement Frontend Event Handler and Logic
- Open `app/client/src/main.ts`
- Add new function `initializeRandomQueryGenerator()` that:
  - Gets the button element by ID
  - Adds click event listener that:
    - Disables the button and shows loading state
    - Calls `api.generateRandomQuery()`
    - On success: populates `#query-input` with the generated query (overwrites existing content)
    - On error: displays error message using existing error display logic
    - Re-enables the button
- Call `initializeRandomQueryGenerator()` in the main DOMContentLoaded event listener

### 9. Create E2E Test Specification
- Read `.claude/commands/test_e2e.md` to understand the E2E test format
- Read `.claude/commands/e2e/test_basic_query.md` to understand the structure
- Create `.claude/commands/e2e/test_random_query_generator.md` with:
  - User story describing the feature
  - Test steps that validate:
    1. Page loads successfully
    2. "Generate Random Query" button is visible
    3. Load sample data (users table)
    4. Click "Generate Random Query" button
    5. Verify query input field is populated with generated text
    6. Verify the generated query is relevant to the loaded table
    7. Click "Query" button to execute the generated query
    8. Verify results are displayed successfully
    9. Take screenshots at each major step
  - Success criteria listing all expected outcomes

### 10. Manual Testing and Validation
- Start the application using `./scripts/start.sh`
- Upload sample data (users, products, events)
- Click "Generate Random Query" multiple times to verify:
  - Different queries are generated each time
  - Queries are contextually relevant to loaded tables
  - Queries are limited to two sentences maximum
  - The input field is properly populated
  - Generated queries can be executed successfully
- Test edge cases:
  - Click button with no tables loaded (should show error)
  - Click button while previous generation is in progress (should be disabled)
  - Verify button styling matches Upload Data button

### 11. Run All Validation Commands
- Execute all validation commands listed in the "Validation Commands" section below
- Ensure zero regressions and all tests pass
- Fix any issues that arise

## Testing Strategy

### Unit Tests
- **test_generate_random_query_with_schema**: Validates that the LLM processor can generate queries when given a valid schema with multiple tables and columns
- **test_generate_random_query_no_tables**: Ensures graceful handling when database has no tables loaded
- **test_generate_random_query_api_error**: Verifies error handling when LLM API is unavailable or returns errors
- **test_random_query_endpoint**: Tests the FastAPI endpoint returns proper response structure
- **test_random_query_endpoint_no_tables**: Validates endpoint error handling when no tables exist

### Edge Cases
- No tables loaded in database - should return user-friendly error message
- LLM API timeout or failure - should display error without crashing
- Very long generated queries (>2 sentences) - should be truncated or regenerated
- Schema with 10+ tables - should still generate focused, relevant queries
- Clicking button rapidly multiple times - should disable during generation
- Overwriting existing query text in input field - should replace completely
- Generated query execution fails - standard error handling applies

## Acceptance Criteria
- [ ] "Generate Random Query" button is visible and styled to match "Upload Data" button
- [ ] Button is positioned with `justify-content: space-between` (separated from Query button)
- [ ] Clicking the button generates a random natural language query based on current schema
- [ ] Generated queries are limited to maximum two sentences
- [ ] Generated query automatically populates the query input field, overwriting existing content
- [ ] Button shows loading state during generation
- [ ] Error message is displayed if no tables are loaded
- [ ] Error message is displayed if LLM API fails
- [ ] Generated queries are contextually relevant to loaded tables and their structure
- [ ] Generated queries can be successfully executed using the existing Query button
- [ ] Multiple clicks generate different queries each time
- [ ] All existing functionality remains unaffected (zero regressions)
- [ ] Unit tests pass with >80% code coverage for new code
- [ ] E2E test validates the feature works end-to-end

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/core/test_random_query_generator.py -v` - Run new unit tests for random query generator
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript compiler to validate frontend code
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_random_query_generator.md` to validate the feature works end-to-end with screenshots

## Notes

### Implementation Considerations
- Use the existing LLM routing logic (OpenAI priority, fallback to Anthropic) to maintain consistency
- The prompt to the LLM should encourage variety - consider adding instructions like "Generate a different type of query each time (aggregation, filtering, joining, sorting, etc.)"
- Consider caching the schema information client-side to reduce API calls if schema hasn't changed
- The two-sentence limit should be enforced in the prompt, but also validated in the backend before returning

### Future Enhancements
- Add a "query history" feature to show previously generated random queries
- Allow users to favorite generated queries for reuse
- Add query complexity levels (simple, medium, advanced)
- Generate multiple query suggestions at once and let users choose
- Add tooltips explaining what each generated query does

### Design Decisions
- Using `secondary-button` class ensures visual consistency with Upload Data button
- Placing button next to Upload Data (both are "data discovery" features) provides logical grouping
- Overwriting input field content (vs appending) prevents confusion and makes the flow clearer
- Maximum two sentences keeps queries concise and focused
- Using existing `llm_processor.py` module ensures consistency with query generation patterns

### Dependencies
- No new dependencies required - uses existing OpenAI and Anthropic integrations
- Relies on `get_database_schema()` function which is already well-tested
- Frontend uses existing API client patterns and error handling
