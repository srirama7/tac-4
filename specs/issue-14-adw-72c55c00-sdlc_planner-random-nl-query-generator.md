# Feature: Random Natural Language Query Generator

## Feature Description
This feature adds a new button to the Natural Language SQL Interface that automatically generates interesting, contextual natural language queries based on the current database schema and table structures. When clicked, the button will use the existing LLM processor to create a query (limited to two sentences maximum) and populate it directly into the query input field, replacing any existing content. This helps users discover what questions they can ask about their data and provides inspiration for data exploration.

## User Story
As a user of the Natural Language SQL Interface
I want to click a button that generates example queries based on my data
So that I can discover interesting questions to ask and learn what's possible with my uploaded tables

## Problem Statement
Users often struggle with knowing what questions to ask about their data, especially when first uploading new datasets. They may not understand the full potential of the natural language query interface or be aware of all the relationships and insights available in their tables. This leads to underutilization of the application and missed opportunities for data exploration.

## Solution Statement
We will add a "Generate Random Query" button positioned near the primary action buttons (using the same style as the "Upload Data" button) that leverages the existing LLM processor to analyze the current database schema and generate contextually relevant, interesting natural language queries. The button will call a new backend endpoint that uses either OpenAI or Anthropic (matching the existing routing logic) to create queries based on table structures, column names, data types, and row counts. The generated query will automatically overwrite the input field, allowing users to immediately execute it or use it as a starting point.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - FastAPI server where we'll add the new `/api/generate-query` endpoint to handle random query generation
- `app/server/core/llm_processor.py` - Contains the LLM integration logic; we'll add a new `generate_random_query()` function that uses the existing OpenAI/Anthropic clients to create interesting queries based on schema
- `app/server/core/sql_processor.py` - Provides `get_database_schema()` which we'll use to retrieve table structures for query generation
- `app/server/core/data_models.py` - Pydantic models; we'll add `GenerateQueryRequest` and `GenerateQueryResponse` models for the new endpoint
- `app/client/index.html` - UI structure; we'll add the new "Generate Random Query" button to the query controls section
- `app/client/src/main.ts` - Frontend logic; we'll add the button click handler and API call to populate the query input field
- `app/client/src/api/client.ts` - API client; we'll add the `generateRandomQuery()` method to call the new backend endpoint
- `app/client/src/types.d.ts` - TypeScript types; we'll add type definitions for the generate query API response
- `app/client/src/style.css` - Styling; we'll ensure the new button matches the "Upload Data" button style and is positioned with `justify-content: space-between`

### New Files
- `app/server/tests/core/test_random_query_generator.py` - Unit tests for the random query generation logic including LLM integration tests
- `.claude/commands/e2e/test_random_query_generator.md` - End-to-end test specification to validate the random query button functionality

## Implementation Plan

### Phase 1: Foundation
First, we'll establish the backend infrastructure by creating the data models and adding the core LLM logic to generate contextual queries. This includes defining the API contract (request/response models) and implementing the query generation function that analyzes database schema and creates interesting natural language questions. We'll ensure the function respects the two-sentence maximum constraint and follows the existing LLM provider routing logic (OpenAI priority, then Anthropic).

### Phase 2: Core Implementation
Next, we'll implement the backend endpoint and frontend functionality. On the backend, we'll add the `/api/generate-query` endpoint to the FastAPI server that calls the query generation function. On the frontend, we'll add the new button to the UI (positioned with space-between layout), implement the click handler to call the API, and ensure it overwrites the query input field with the generated query. We'll also add comprehensive unit tests for the backend logic.

### Phase 3: Integration
Finally, we'll integrate the feature with the existing application flow, ensuring it works seamlessly with the current schema loading and query execution features. We'll create an end-to-end test to validate the complete user flow (click button → API call → input field populated → query executable). We'll also ensure proper error handling, loading states, and that the feature gracefully handles edge cases like no tables loaded or API failures.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Backend Data Models
- Read `app/server/core/data_models.py` to understand the existing model structure
- Add `GenerateQueryRequest` model (empty or with optional parameters for future extensibility)
- Add `GenerateQueryResponse` model with fields: `query` (str), `error` (Optional[str])
- Follow existing patterns in the file for consistency

### Step 2: Implement Random Query Generation Logic
- Read `app/server/core/llm_processor.py` to understand the existing LLM integration patterns
- Add `generate_random_query(schema_info: Dict[str, Any]) -> str` function
- Implement `generate_random_query_with_openai()` function that:
  - Takes schema_info and formats it using the existing `format_schema_for_prompt()` function
  - Creates a prompt that asks the LLM to generate an interesting natural language query based on the schema
  - Specifies constraints: maximum two sentences, should be specific to the actual tables/columns, should be executable
  - Returns the generated query text
- Implement `generate_random_query_with_anthropic()` function with the same logic but using Anthropic API
- Follow the existing routing pattern (OpenAI priority, then Anthropic) in the main `generate_random_query()` function
- Ensure the prompt encourages diverse, interesting queries that showcase different SQL capabilities (aggregations, filters, joins if multiple tables exist, date queries, etc.)

### Step 3: Add Backend API Endpoint
- Read `app/server/server.py` to understand the existing endpoint structure
- Add new POST endpoint `/api/generate-query` with response model `GenerateQueryResponse`
- Implement endpoint logic:
  - Get current database schema using `get_database_schema()`
  - Call `generate_random_query()` with the schema info
  - Return the generated query in the response
  - Handle errors gracefully with proper error messages
  - Add structured logging following the existing pattern
- Follow existing error handling patterns from other endpoints

### Step 4: Add Backend Unit Tests
- Create `app/server/tests/core/test_random_query_generator.py`
- Write unit tests for:
  - `generate_random_query_with_openai()` function (mock OpenAI API response)
  - `generate_random_query_with_anthropic()` function (mock Anthropic API response)
  - `generate_random_query()` routing logic (test OpenAI priority, Anthropic fallback)
  - Edge case: no tables in schema (should handle gracefully)
  - Edge case: API errors (should raise appropriate exceptions)
- Follow the testing patterns in `app/server/tests/core/test_llm_processor.py`
- Ensure all tests pass with `cd app/server && uv run pytest`

### Step 5: Add Frontend TypeScript Types
- Read `app/client/src/types.d.ts` to understand the existing type definitions
- Add `GenerateQueryResponse` interface matching the backend response model
- Ensure types align with the backend data models

### Step 6: Add Frontend API Client Method
- Read `app/client/src/api/client.ts` to understand the existing API client structure
- Add `generateRandomQuery()` method to the `api` object
- Method should:
  - Make a POST request to `/api/generate-query`
  - Return the typed `GenerateQueryResponse`
  - Follow the existing error handling patterns

### Step 7: Update Frontend UI
- Read `app/client/index.html` to understand the current button layout
- Add a new button element with id `generate-query-button` in the query-controls div
- Button text should be "Generate Random Query"
- Button class should be `secondary-button` (same as Upload Data button)
- Update the `.query-controls` div to use `justify-content: space-between` to position the Query button on one side and the two secondary buttons on the other
- Ensure the HTML structure supports the space-between layout (e.g., wrap the two secondary buttons in a container div if needed)

### Step 8: Implement Frontend Button Logic
- Read `app/client/src/main.ts` to understand the existing initialization patterns
- Add `initializeGenerateQuery()` function that:
  - Gets references to the generate query button and query input elements
  - Adds click event listener to the button
  - On click: disables button, shows loading state (spinner or "Generating..." text)
  - Calls `api.generateRandomQuery()`
  - On success: overwrites `queryInput.value` with the generated query
  - On error: displays error message using existing `displayError()` function
  - Re-enables button after completion
- Call `initializeGenerateQuery()` from the DOMContentLoaded event listener
- Ensure the button is disabled when no tables are loaded (check schema on load)

### Step 9: Update Frontend Styling
- Read `app/client/src/style.css` to understand the existing button styles
- Verify that `.secondary-button` style exists and matches the Upload Data button
- Update `.query-controls` to use `display: flex; justify-content: space-between; align-items: center;`
- Add a wrapper class for the secondary buttons if needed to group them together
- Ensure responsive layout works on different screen sizes
- Verify visual consistency with the existing Upload Data button

### Step 10: Create E2E Test Specification
- Read `.claude/commands/test_e2e.md` to understand the E2E test framework
- Read `.claude/commands/e2e/test_basic_query.md` to understand the test format
- Create `.claude/commands/e2e/test_random_query_generator.md` with:
  - User story describing the feature
  - Test steps that:
    1. Load sample data (users table)
    2. Verify the "Generate Random Query" button exists and is enabled
    3. Click the button
    4. Verify loading state appears
    5. Verify the query input field is populated with a query (non-empty, max 2 sentences)
    6. Verify the query is relevant to the loaded tables (contains "users" or column names)
    7. Click the Query button to execute the generated query
    8. Verify results are returned successfully
    9. Take screenshots at key points
  - Success criteria
- Follow the exact format from the example E2E test files

### Step 11: Run Validation Commands
- Execute all validation commands as specified in the "Validation Commands" section below
- Ensure all tests pass with zero errors
- Verify the E2E test completes successfully with screenshots
- Confirm zero regressions in existing functionality

## Testing Strategy

### Unit Tests
- **LLM Integration Tests**: Mock OpenAI and Anthropic API calls to test query generation logic without making actual API requests
- **Routing Logic Tests**: Verify that the function correctly prioritizes OpenAI over Anthropic based on API key availability
- **Schema Processing Tests**: Test query generation with different schema configurations (single table, multiple tables, various column types)
- **Error Handling Tests**: Verify graceful handling of API failures, missing schema, and malformed responses
- **Constraint Tests**: Ensure generated queries respect the two-sentence maximum constraint

### Edge Cases
- **No tables loaded**: Button should be disabled or show appropriate message when no schema exists
- **API key missing**: Should handle gracefully and show error message to user
- **LLM returns invalid response**: Should validate and potentially retry or show error
- **Very large schema**: Should handle schemas with many tables/columns without timeout
- **Empty tables**: Should generate queries even for tables with 0 rows
- **Schema with unusual column names**: Should properly handle special characters in column names
- **Multiple rapid clicks**: Should prevent multiple simultaneous API calls (disable button during request)
- **Network failure**: Should display user-friendly error message and re-enable button

## Acceptance Criteria
- [ ] A new "Generate Random Query" button exists in the UI, positioned with space-between layout alongside the Upload Data button
- [ ] The button uses the same style as the Upload Data button (secondary-button class)
- [ ] Clicking the button calls the `/api/generate-query` endpoint
- [ ] The backend endpoint successfully generates a contextual natural language query based on the current database schema
- [ ] The generated query is limited to a maximum of two sentences
- [ ] The generated query is relevant to the loaded tables (mentions actual table/column names)
- [ ] The query input field is overwritten (not appended to) with the generated query
- [ ] The button shows a loading state while the API request is in progress
- [ ] The button is disabled when no tables are loaded in the database
- [ ] Errors are handled gracefully with user-friendly messages
- [ ] The generated query can be successfully executed using the existing Query button
- [ ] All existing functionality continues to work without regression
- [ ] Unit tests cover the new query generation logic with >80% coverage
- [ ] E2E test validates the complete user flow from button click to query execution
- [ ] The feature works with both OpenAI and Anthropic API providers

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test `.claude/commands/e2e/test_random_query_generator.md` to validate this functionality works end-to-end
- `cd app/server && uv run pytest tests/core/test_random_query_generator.py -v` - Run new unit tests for random query generation
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript compilation to validate type safety
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Future Enhancements
- Add a "Regenerate" action if the user doesn't like the first generated query
- Add query history/favorites to save interesting queries
- Allow users to provide hints or preferences for query generation (e.g., "focus on aggregations", "show me joins")
- Add analytics to track which generated queries are most commonly executed
- Support generating multiple query suggestions at once for the user to choose from

### Implementation Considerations
- The LLM prompt should encourage variety in query types (filters, aggregations, joins, date ranges, sorting, limits, etc.)
- Consider caching recent queries to avoid generating the same query multiple times in a row
- The two-sentence limit should be enforced in the LLM prompt and validated in the backend
- Ensure the generated queries are safe and don't include any malicious SQL patterns
- The feature should respect the existing LLM provider routing logic (OpenAI priority)
- Consider rate limiting if users spam the button to avoid excessive API costs

### Dependencies
- No new libraries required - uses existing `openai` and `anthropic` packages already in the project
- All functionality leverages existing infrastructure (LLM processor, schema retrieval, API client patterns)

### UX Considerations
- The button should be easily discoverable but not overshadow the primary Query button
- Loading state should be clear to prevent users from clicking multiple times
- The generated query should appear natural and help users understand what's possible
- Consider adding a subtle animation when the query is populated into the input field
- The button should provide visual feedback (hover, active, disabled states)
