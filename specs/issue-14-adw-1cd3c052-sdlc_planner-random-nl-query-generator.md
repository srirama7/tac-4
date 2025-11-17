# Feature: Random Natural Language Query Generator

## Feature Description
This feature adds a new button to the Natural Language SQL Interface that generates interesting, contextually-relevant natural language queries based on the current database tables and their structure. When clicked, the button uses the LLM processor to analyze existing table schemas and generate a compelling query suggestion that is automatically populated into the input field, overwriting any existing content. This helps users explore their data by providing query inspiration and demonstrates the capabilities of the natural language SQL interface.

## User Story
As a user of the Natural Language SQL Interface
I want to generate random natural language queries based on my uploaded data
So that I can explore my data without having to think of queries myself and discover interesting insights

## Problem Statement
Users may not always know what questions to ask about their data, especially when first uploading new datasets. This creates a barrier to entry and reduces engagement with the application. Users need inspiration and examples of what kinds of questions they can ask about their specific data structure. Additionally, users may want to quickly test the system's capabilities without manually typing queries.

## Solution Statement
We will implement a "Generate Query" button positioned alongside the existing "Upload Data" button using the same visual styling. This button will trigger a backend API endpoint that introspects the current database schema (tables, columns, data types, and relationships), uses the LLM processor to generate a contextually-relevant natural language query limited to two sentences maximum, and returns it to the frontend where it automatically populates the query input field, overwriting any existing content.

## Relevant Files
Use these files to implement the feature:

- **app/server/server.py** (lines 1-280) - Main FastAPI server with API endpoints. We'll add a new `/api/generate-query` POST endpoint here to handle query generation requests
- **app/server/core/llm_processor.py** (lines 1-162) - Contains LLM integration functions for OpenAI and Anthropic. We'll add a new `generate_random_nl_query()` function that takes schema information and generates interesting natural language queries
- **app/server/core/sql_processor.py** (lines 61-117) - Contains `get_database_schema()` function that we'll reuse to get current table structures for query generation
- **app/server/core/data_models.py** (lines 1-82) - Pydantic models for API requests/responses. We'll add new `GenerateQueryRequest` and `GenerateQueryResponse` models
- **app/client/src/main.ts** (lines 1-423) - Main TypeScript file with frontend logic. We'll add a new "Generate Query" button initialization, event handler, and API call
- **app/client/index.html** (lines 1-99) - HTML structure. We'll add the new button element in the query-controls section (around line 24)
- **app/client/src/style.css** (lines 1-150+) - CSS styles. The button will reuse existing `.secondary-button` styles matching the "Upload Data" button
- **app/client/src/api/client.ts** - API client functions. We'll add a new `generateQuery()` function to call the backend endpoint
- **.claude/commands/test_e2e.md** (lines 1-64) - E2E test runner instructions to understand how to create E2E tests
- **.claude/commands/e2e/test_basic_query.md** (lines 1-39) - Example E2E test structure to model our new test after

### New Files

- **app/server/tests/core/test_query_generator.py** - Unit tests for the query generation logic including schema introspection and LLM integration
- **.claude/commands/e2e/test_query_generator.md** - E2E test file to validate the Generate Query button functionality works end-to-end

## Implementation Plan

### Phase 1: Foundation
First, we need to establish the backend infrastructure for query generation:
1. Create new data models for the generate query API endpoint (request/response)
2. Implement the core query generation logic in the LLM processor that analyzes database schema
3. Add database schema introspection capabilities to gather context about tables, columns, data types, and row counts
4. Create the API endpoint in the FastAPI server that connects everything together

### Phase 2: Core Implementation
Next, implement the frontend UI and integration:
1. Add the "Generate Query" button to the HTML with proper positioning and styling
2. Implement the frontend JavaScript/TypeScript logic to handle button clicks
3. Create the API client function to communicate with the backend endpoint
4. Add logic to populate the query input field and overwrite existing content
5. Handle loading states and error scenarios gracefully

### Phase 3: Integration
Finally, ensure quality and integration:
1. Create comprehensive unit tests for the backend query generation logic
2. Create an E2E test to validate the complete user flow
3. Test with multiple table configurations (single table, multiple tables, various column types)
4. Validate the query generation respects the two-sentence maximum constraint
5. Ensure the feature works with both OpenAI and Anthropic providers
6. Run full test suite to ensure zero regressions

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Task 1: Create Data Models
- Open `app/server/core/data_models.py`
- Add `GenerateQueryRequest` model with optional parameters for customization
- Add `GenerateQueryResponse` model with `query` field and optional `error` field
- Ensure models follow existing patterns and use Pydantic validation

### Task 2: Implement Core Query Generation Logic
- Open `app/server/core/llm_processor.py`
- Create `generate_random_nl_query(schema_info: Dict[str, Any]) -> str` function
- This function should analyze the schema (tables, columns, types, row counts)
- Use either OpenAI or Anthropic (following existing routing logic) to generate interesting queries
- Prompt should instruct the LLM to:
  - Generate a natural language query that would be interesting to execute
  - Base the query on actual table and column names in the schema
  - Create queries that demonstrate different SQL capabilities (aggregations, filters, joins, etc.)
  - Limit output to maximum two sentences
  - Return only the natural language query without explanations
- Handle edge cases: no tables, single table, multiple tables
- Follow existing code patterns for error handling and API calls

### Task 3: Create Backend API Endpoint
- Open `app/server/server.py`
- Add new POST endpoint `/api/generate-query` with response model `GenerateQueryResponse`
- Import necessary functions and models
- In the endpoint handler:
  - Get current database schema using `get_database_schema()`
  - Check if there are any tables (return helpful error if none)
  - Call `generate_random_nl_query()` with schema information
  - Return the generated query in the response
  - Handle errors gracefully with appropriate error messages
- Follow existing endpoint patterns for logging and error handling

### Task 4: Create Unit Tests for Query Generation
- Create new file `app/server/tests/core/test_query_generator.py`
- Import necessary modules including pytest, the query generator function, and mocking utilities
- Write test cases:
  - `test_generate_query_with_single_table()` - Verify query generation with one table
  - `test_generate_query_with_multiple_tables()` - Verify query generation with multiple tables
  - `test_generate_query_no_tables()` - Verify proper error handling when no tables exist
  - `test_generate_query_sentence_limit()` - Verify output is maximum two sentences
  - `test_generate_query_uses_actual_schema()` - Verify generated query references real table/column names
- Mock LLM API calls to avoid external dependencies
- Follow existing test patterns in the codebase

### Task 5: Add Frontend Button to HTML
- Open `app/client/index.html`
- Locate the `.query-controls` div (around line 22)
- Add a new button element: `<button id="generate-query-button" class="secondary-button">Generate Query</button>`
- Position it after the "Query" button but maintain the `justify-content: space-between` layout by wrapping primary buttons together
- Update the structure to use flexbox with `justify-content: space-between` to separate the "Query" button group from the "Generate Query" and "Upload Data" buttons

### Task 6: Add API Client Function
- Open `app/client/src/api/client.ts`
- Add new function `generateQuery()` that:
  - Makes a POST request to `/api/generate-query`
  - Returns the response typed as `{ query: string; error?: string }`
  - Follows existing API client patterns for error handling
- Export the function for use in main.ts

### Task 7: Implement Frontend Logic
- Open `app/client/src/main.ts`
- Add new function `initializeGenerateQuery()` that:
  - Gets references to the generate query button and query input elements
  - Adds click event listener to the button
  - Shows loading state while generating (disable button, show loading spinner)
  - Calls `api.generateQuery()`
  - On success: populates the query input field, overwriting existing content
  - On error: displays error message using existing `displayError()` function
  - Restores button state when complete
- Call `initializeGenerateQuery()` in the DOMContentLoaded event handler
- Follow existing code patterns for consistency

### Task 8: Add CSS Styling (if needed)
- Open `app/client/src/style.css`
- Verify the existing `.secondary-button` styles work well for the new button
- Adjust `.query-controls` layout if needed to properly use `justify-content: space-between`
- Consider adding a left-side wrapper div for primary actions and right-side wrapper for secondary actions
- Ensure responsive behavior on smaller screens

### Task 9: Create E2E Test File
- Create new file `.claude/commands/e2e/test_query_generator.md`
- Follow the structure of `.claude/commands/e2e/test_basic_query.md`
- Define the User Story: "As a user, I want to generate random queries so that I can explore my data"
- Write Test Steps:
  1. Navigate to application URL
  2. Take screenshot of initial state
  3. Verify "Generate Query" button is visible
  4. Upload sample data (users.json)
  5. Click "Generate Query" button
  6. Verify query input field is populated with text
  7. Take screenshot of generated query
  8. Verify the query text is not empty and is maximum two sentences
  9. Verify the query references actual table/column names from the schema
  10. Click "Query" button to execute the generated query
  11. Verify results are displayed successfully
  12. Take screenshot of query results
  13. Click "Generate Query" button again
  14. Verify the query input field is overwritten with new query
  15. Take screenshot of second generated query
- Define Success Criteria:
  - Button is visible and clickable
  - Query is generated and populated into input field
  - Query is contextually relevant to uploaded data
  - Generated query can be successfully executed
  - Subsequent clicks overwrite the previous query
  - At least 3 screenshots are captured

### Task 10: Run Backend Unit Tests
- Run unit tests to ensure new query generation logic works correctly
- Execute: `cd app/server && uv run pytest tests/core/test_query_generator.py -v`
- Fix any failures before proceeding
- Ensure all assertions pass

### Task 11: Run Full Test Suite
- Execute all validation commands listed below to ensure zero regressions
- Fix any issues that arise
- Verify the feature works end-to-end

## Testing Strategy

### Unit Tests
- **Backend Query Generation**: Test the `generate_random_nl_query()` function with various schema configurations
  - Single table with few columns
  - Multiple tables with relationships
  - Empty database (no tables)
  - Tables with various data types (text, integer, real, date)
- **API Endpoint**: Test the `/api/generate-query` endpoint
  - Successful query generation
  - Error handling when no tables exist
  - Response format validation
- **Sentence Limit**: Verify all generated queries are maximum two sentences
- **Schema Relevance**: Verify generated queries reference actual table and column names from the schema

### Edge Cases
- **No tables uploaded**: Should return a helpful error message like "Please upload data first to generate queries"
- **Single simple table**: Should generate relevant queries for basic operations (SELECT, WHERE, ORDER BY)
- **Multiple related tables**: Should generate queries that could use JOINs based on common column names
- **Very large schemas**: Should handle databases with many tables and columns without overwhelming the LLM
- **Special characters in table/column names**: Should properly escape or quote identifiers in generated queries
- **Empty tables**: Should handle tables with zero rows gracefully
- **Repeated clicks**: Each click should generate a fresh, different query
- **Network failures**: Should display user-friendly error messages
- **LLM API failures**: Should catch and display appropriate error messages

## Acceptance Criteria
- A "Generate Query" button is visible in the UI, styled identically to the "Upload Data" button
- The button is positioned with proper spacing using flexbox justify-apart layout
- Clicking the button generates a natural language query based on current database tables
- The generated query is automatically populated into the query input field
- Any existing text in the input field is overwritten when a new query is generated
- Generated queries are limited to a maximum of two sentences
- Generated queries are contextually relevant to the actual database schema (reference real tables and columns)
- The button shows appropriate loading states during generation
- Error messages are displayed if query generation fails or no tables exist
- The generated query can be successfully executed by clicking the "Query" button
- All existing functionality continues to work without regressions
- Backend unit tests pass with 100% success rate
- E2E test validates the complete user flow successfully
- The feature works with both OpenAI and Anthropic LLM providers

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md` to understand E2E test execution
- Read and execute `.claude/commands/e2e/test_query_generator.md` to validate the Generate Query button functionality works end-to-end
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run query generator unit tests to validate core logic
- `cd app/server && uv run python -m py_compile server.py main.py core/*.py` - Validate Python syntax
- `cd app/server && uv run ruff check .` - Run linter to validate code quality
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate TypeScript code
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Manual test: Start the application, upload sample data, click "Generate Query" multiple times, verify queries are populated and can be executed successfully

## Notes

### LLM Provider Configuration
- The query generation will follow the existing LLM routing logic in `llm_processor.py`
- Priority: OpenAI API key if available, then Anthropic API key
- Use the same temperature and model settings as the existing `generate_sql()` functions for consistency

### Query Generation Prompt Engineering
The prompt for query generation should be carefully crafted to:
- Encourage variety in query types (simple filters, aggregations, grouping, sorting, multi-table if applicable)
- Request queries that would produce interesting results, not just "SELECT *"
- Ensure queries are natural language, not SQL
- Examples: "Show me the top 5 users who signed up most recently", "What's the average price of products by category?"

### UI/UX Considerations
- Consider adding a tooltip or help text explaining what the button does
- The button should be disabled if no tables are loaded (optional enhancement)
- Loading spinner should match existing patterns in the codebase
- Consider adding a subtle animation when the query is populated

### Future Enhancements (Not in Scope)
- Query history/favorites to save generated queries
- Ability to regenerate similar queries with slight variations
- Query difficulty levels (simple, intermediate, complex)
- Query categories (aggregations, filters, joins, etc.)
- User feedback mechanism (thumbs up/down on generated queries)

### Performance Considerations
- Query generation may take 1-3 seconds depending on LLM API response time
- Consider caching schema information to avoid repeated database introspection
- Ensure the UI remains responsive during generation (async/await patterns)

### Security Considerations
- The generated natural language queries will be processed through the existing SQL generation pipeline
- All existing SQL injection protections remain in place
- No direct SQL is generated or executed by this feature - only natural language
- Ensure the schema introspection doesn't expose sensitive system tables
