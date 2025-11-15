# Feature: Natural Language Query Generator Button

## Feature Description
A new UI button that automatically generates interesting natural language queries based on existing database tables and their structure. When clicked, the button uses the LLM processor to analyze the current database schema and generate contextually relevant, two-sentence maximum queries that demonstrate the capabilities of the natural language SQL interface. The generated query overwrites any existing text in the input field, allowing users to immediately execute it and see results.

This feature enhances user experience by:
- Providing query inspiration when users are unsure what to ask
- Demonstrating the interface's capabilities through concrete examples
- Helping users understand their data structure through suggested questions
- Reducing the learning curve for new users

## User Story
As a user of the Natural Language SQL Interface
I want to generate sample queries based on my uploaded data
So that I can quickly explore my database without having to think of queries myself and better understand what questions I can ask

## Problem Statement
Currently, users must manually think of and type natural language queries to interact with their data. This can be challenging when:
- Users are new to the application and don't know what types of questions to ask
- Users have uploaded data but aren't sure what interesting insights they can extract
- Users want to quickly test the interface capabilities without effort
- Users need inspiration for query patterns that work well with the system

This creates friction in the user experience and may prevent users from fully exploring their data's potential.

## Solution Statement
Implement a "Generate Query" button positioned alongside existing primary buttons (Query and Upload Data) that:
1. Retrieves the current database schema including table names, column names, column types, and row counts
2. Sends this schema information to the LLM processor (via llm_processor.py)
3. Generates an interesting, contextually relevant natural language query (max 2 sentences)
4. Automatically populates the query input field, overwriting any existing content
5. Allows users to immediately execute the generated query with the existing Query button

The button will be styled consistently with the "Upload Data" button and positioned with space-between justification to maintain visual balance in the interface.

## Relevant Files
Use these files to implement the feature:

- **app/server/core/llm_processor.py** - Contains LLM integration functions (generate_sql_with_openai, generate_sql_with_anthropic, format_schema_for_prompt). We'll add a new function `generate_natural_language_query()` to create queries based on database schema.

- **app/server/core/sql_processor.py** - Contains `get_database_schema()` function that retrieves current database schema information including tables, columns, types, and row counts. This will be used to provide context to the LLM.

- **app/server/core/data_models.py** - Contains Pydantic models for request/response validation. We'll add `GenerateQueryRequest` and `GenerateQueryResponse` models.

- **app/server/server.py** - FastAPI server with route definitions. We'll add a new POST endpoint `/api/generate-query` to handle query generation requests.

- **app/client/src/main.ts** - Main TypeScript file containing UI initialization and event handlers. We'll add the "Generate Query" button initialization, click handler, and logic to populate the input field.

- **app/client/src/api/client.ts** - API client functions for communicating with the backend. We'll add a `generateQuery()` function to call the new endpoint.

- **app/client/src/types.d.ts** - TypeScript type definitions matching backend models. We'll add `GenerateQueryRequest` and `GenerateQueryResponse` interfaces.

- **app/client/index.html** - HTML structure for the application. We'll add the new "Generate Query" button in the query-controls section.

- **app/client/src/style.css** - CSS styling for the application. We may need to adjust button layout to ensure proper spacing with justify-content: space-between.

- **.claude/commands/test_e2e.md** - Documentation on how E2E tests work in this project. Read this to understand the E2E testing framework.

- **.claude/commands/e2e/test_basic_query.md** - Example E2E test showing how to test query functionality. Use this as a reference for creating the new E2E test.

### New Files

- **.claude/commands/e2e/test_query_generator.md** - New E2E test file to validate the query generator feature works correctly. This test will verify the button exists, generates queries, populates the input field, and the generated queries can be executed successfully.

- **app/server/tests/core/test_query_generator.py** - Unit tests for the new `generate_natural_language_query()` function in llm_processor.py. Tests will verify query generation with different schema configurations, error handling, and output format validation.

## Implementation Plan

### Phase 1: Foundation
**Backend Data Models & API Endpoint Setup**

Create the necessary data structures and API endpoint to support query generation. This includes:
- Adding Pydantic models for the request/response contract
- Implementing the core LLM function to generate natural language queries based on schema
- Creating a new FastAPI endpoint that orchestrates schema retrieval and query generation
- Writing unit tests to ensure the generation logic works correctly

### Phase 2: Core Implementation
**Frontend UI Integration**

Build the user-facing components that trigger and display query generation:
- Add the "Generate Query" button to the HTML with proper styling
- Implement the TypeScript click handler that calls the backend API
- Populate the query input field with the generated query
- Add visual feedback during query generation (loading state)
- Write frontend API client function to communicate with the backend

### Phase 3: Integration
**End-to-End Testing & Validation**

Ensure the complete feature works seamlessly across the full stack:
- Create comprehensive E2E test to validate the feature from user perspective
- Test with various database schemas (empty, single table, multiple tables)
- Verify integration with existing query execution flow
- Run all existing tests to ensure zero regressions
- Validate error handling and edge cases

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Task 1: Add Backend Data Models
- Open `app/server/core/data_models.py`
- Add `GenerateQueryRequest` model (empty since no parameters needed - schema retrieved server-side)
- Add `GenerateQueryResponse` model with fields: `query` (str), `generated_at` (datetime), `error` (Optional[str])
- Ensure models follow existing patterns in the file

### Task 2: Implement Query Generation Function
- Open `app/server/core/llm_processor.py`
- Create new function `generate_natural_language_query(schema_info: Dict[str, Any]) -> str`
- Use existing `format_schema_for_prompt()` to format schema
- Create a prompt that asks the LLM to generate an interesting 1-2 sentence natural language query
- Support both OpenAI and Anthropic providers using the existing routing logic pattern
- Include instructions in prompt: query should be specific, interesting, and demonstrate data exploration
- Limit generation to max 2 sentences
- Clean up the response (remove any markdown or extra formatting)
- Handle errors gracefully with meaningful error messages

### Task 3: Write Unit Tests for Query Generator
- Create `app/server/tests/core/test_query_generator.py`
- Test `generate_natural_language_query()` with sample schema
- Test with empty schema (should handle gracefully)
- Test with single table schema
- Test with multiple tables schema
- Verify generated queries are reasonable length (not too long)
- Mock LLM API calls to avoid actual API usage in tests
- Run tests: `cd app/server && uv run pytest tests/core/test_query_generator.py -v`

### Task 4: Create API Endpoint
- Open `app/server/server.py`
- Add new POST endpoint `/api/generate-query` with response model `GenerateQueryResponse`
- Import new models from `core.data_models`
- Import new function from `core.llm_processor`
- Retrieve database schema using `get_database_schema()`
- Call `generate_natural_language_query()` with schema
- Return `GenerateQueryResponse` with generated query and timestamp
- Handle errors and return error in response model (don't raise exceptions)
- Add logging for success/failure similar to existing endpoints
- Test endpoint manually or with curl after implementation

### Task 5: Add Frontend Type Definitions
- Open `app/client/src/types.d.ts`
- Add `GenerateQueryRequest` interface (empty object for consistency)
- Add `GenerateQueryResponse` interface with fields: `query: string`, `generated_at: string`, `error?: string`
- Ensure types match backend Pydantic models exactly

### Task 6: Add Frontend API Client Function
- Open `app/client/src/api/client.ts`
- Add `generateQuery()` method to the `api` object
- Use `apiRequest<GenerateQueryResponse>` to call `/generate-query` endpoint
- Use POST method with empty body or no body
- Follow existing patterns in the file for consistency

### Task 7: Add Generate Query Button to HTML
- Open `app/client/index.html`
- Find the `.query-controls` div (contains Query and Upload Data buttons)
- Add new button with id `generate-query-button` and class `secondary-button`
- Button text: "Generate Query"
- Position between "Query" and "Upload Data" buttons
- Ensure proper spacing with existing CSS (justify-content: space-between)

### Task 8: Implement Button Click Handler
- Open `app/client/src/main.ts`
- Create new function `initializeQueryGenerator()`
- Get reference to `generate-query-button` and `query-input` elements
- Add click event listener to the button
- On click: disable button, show loading state (spinner or "Generating...")
- Call `api.generateQuery()`
- On success: populate `query-input.value` with `response.query` (overwrite existing content)
- On error: display error using existing `displayError()` function
- Re-enable button and restore button text after completion
- Call `initializeQueryGenerator()` from the `DOMContentLoaded` event listener

### Task 9: Update CSS for Button Layout (if needed)
- Open `app/client/src/style.css`
- Find `.query-controls` styles
- Verify `display: flex` and `justify-content: space-between` are set
- Adjust if needed to ensure proper spacing between all three buttons
- Ensure secondary-button style is consistent with Upload Data button
- Test responsive layout if necessary

### Task 10: Create E2E Test for Query Generator
- Read `.claude/commands/test_e2e.md` to understand E2E test structure
- Read `.claude/commands/e2e/test_basic_query.md` for reference
- Create `.claude/commands/e2e/test_query_generator.md`
- Include User Story describing what we're testing
- Add Test Steps:
  1. Navigate to application URL
  2. Take screenshot of initial state
  3. Verify "Generate Query" button exists
  4. Take screenshot showing the button
  5. Click "Generate Query" button
  6. Wait for query to populate in input field
  7. Verify input field contains generated text (not empty, max ~2 sentences)
  8. Take screenshot of populated query
  9. Click "Query" button to execute the generated query
  10. Verify results appear without errors
  11. Take screenshot of successful execution
  12. Click "Hide" to close results
  13. Click "Generate Query" again to verify it overwrites the previous query
  14. Take screenshot showing new query replaced old one
- Add Success Criteria: button exists, generates queries, overwrites field, queries execute successfully, 5+ screenshots captured

### Task 11: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Review results and fix any issues
- Ensure all tests pass before considering feature complete

## Testing Strategy

### Unit Tests
**Query Generation Function Tests** (`app/server/tests/core/test_query_generator.py`):
- Test successful query generation with realistic multi-table schema
- Test handling of empty database (no tables)
- Test handling of single table with various column types
- Test query length constraints (should be ≤ 2 sentences)
- Test LLM provider routing (OpenAI vs Anthropic)
- Test error handling when LLM API fails
- Mock all external API calls to avoid actual LLM usage

**API Endpoint Tests** (can be added to existing test files):
- Test `/api/generate-query` returns valid response structure
- Test endpoint handles errors gracefully
- Test response includes timestamp
- Test with database containing tables
- Test with empty database

### Edge Cases
1. **Empty Database**: When no tables exist, the query generator should handle gracefully (return helpful message or generic query suggestion)

2. **Single Table**: Should generate relevant queries for just one table

3. **Many Tables**: Should generate queries that potentially use multiple tables or focus on the most interesting table

4. **LLM API Failure**: Should return error in response.error field, not crash

5. **Long Column Names**: Should handle tables with many columns or complex column names

6. **Rapid Clicking**: User clicks "Generate Query" button multiple times quickly - should handle gracefully without duplicate requests

7. **Query Input Already Has Content**: Generated query should overwrite existing content (intended behavior)

8. **No API Keys Configured**: Should return meaningful error message when neither OpenAI nor Anthropic API keys are available

## Acceptance Criteria
1. A "Generate Query" button is visible in the UI, styled consistently with the "Upload Data" button
2. The button is positioned with proper spacing using justify-content: space-between layout
3. Clicking the button retrieves the current database schema and generates a natural language query
4. The generated query appears in the query input field, overwriting any existing content
5. Generated queries are limited to a maximum of 2 sentences
6. Generated queries are contextually relevant to the tables and columns in the database
7. The button shows loading state while query is being generated
8. Errors are handled gracefully with user-friendly messages
9. Users can immediately execute the generated query using the existing "Query" button
10. The feature works with both OpenAI and Anthropic LLM providers
11. E2E test validates the complete user flow from button click to query execution
12. All existing tests pass with zero regressions
13. Generated queries execute successfully without SQL errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md` to understand how to run E2E tests
- Read and execute `.claude/commands/e2e/test_query_generator.md` to validate the query generator feature works end-to-end
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run new query generator unit tests
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript compiler to validate no type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### LLM Prompt Design
The prompt for query generation should instruct the LLM to:
- Generate only 1-2 sentences maximum (enforce brevity)
- Create queries that demonstrate interesting data exploration (aggregations, filters, joins)
- Use natural, conversational language
- Focus on tables with meaningful data (avoid empty or system tables)
- Vary query types (avoid repetitive suggestions)

### API Key Handling
The feature reuses the existing LLM provider routing logic in `llm_processor.py`:
- Priority: OpenAI > Anthropic > request preference
- Falls back gracefully when keys are missing
- Uses the same models as SQL generation (gpt-4.1-mini for OpenAI, claude-3-haiku for Anthropic)

### UI/UX Considerations
- The button should be non-intrusive but easily discoverable
- Loading state is important to provide feedback during generation (can take 1-2 seconds)
- Overwriting input field is intentional - makes it clear this is a suggestion the user can modify or re-generate
- Position with "Upload Data" button creates visual balance and groups action buttons together

### Future Enhancements
(Not part of this implementation, but noted for future consideration):
- Query history/favorites
- Multiple query suggestions to choose from
- Query categories (aggregations, filters, joins, etc.)
- Smart suggestions based on recently uploaded data
- Query templates based on common patterns
