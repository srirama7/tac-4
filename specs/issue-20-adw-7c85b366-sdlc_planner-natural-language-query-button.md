# Feature: Natural Language Query Button

## Feature Description
Add a new button to the Natural Language SQL Interface that generates interesting natural language queries based on the existing database tables and their structure. When clicked, the button will automatically populate the query input field with an AI-generated natural language query that users can execute manually. The generated queries will be limited to two sentences maximum and will be based on the actual table schemas in the database, providing users with useful query examples and inspiration for exploring their data.

## User Story
As a user of the Natural Language SQL Interface
I want to generate interesting natural language queries automatically based on my uploaded data
So that I can discover useful ways to query my data and learn by example without having to think of queries myself

## Problem Statement
Users often struggle to come up with meaningful natural language queries when starting to explore their data. They may not know what kinds of questions are possible or interesting to ask. This creates a barrier to entry and reduces the value users get from the application, especially for new users or those working with unfamiliar datasets. The lack of query examples makes it harder for users to understand the capabilities of the natural language SQL interface.

## Solution Statement
Implement a "Generate Query" button that leverages the existing LLM integration (`llm_processor.py`) to automatically create interesting, contextual natural language queries based on the current database schema. The button will:
1. Analyze the available tables and their column structures
2. Use the LLM to generate a relevant natural language query (max 2 sentences)
3. Automatically populate the query input field with the generated query
4. Always overwrite any existing content in the input field
5. Position the button separately from the primary action buttons using the Upload Data button's styling
6. Provide users with immediate, actionable query examples

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains LLM integration logic that will be extended to generate natural language queries based on schema
- `app/server/server.py` - FastAPI server where we'll add the new `/api/generate-query` endpoint
- `app/server/core/data_models.py` - Contains Pydantic models; will add request/response models for query generation
- `app/server/core/sql_processor.py` - Contains the `get_database_schema()` function used to retrieve table structures
- `app/client/index.html` - Contains the UI structure; will add the Generate Query button
- `app/client/src/main.ts` - Contains frontend logic; will add event handlers for the new button
- `app/client/src/api/client.ts` - API client module; will add the API call for query generation
- `app/client/src/style.css` - Contains styling; will add styles for the new button
- `app/client/src/types.d.ts` - TypeScript type definitions; will add types for the new API endpoint
- `.claude/commands/test_e2e.md` - E2E test runner documentation to understand how to create E2E tests
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test to follow as a pattern

### New Files
- `app/server/tests/core/test_query_generator.py` - Unit tests for the query generation functionality
- `.claude/commands/e2e/test_query_generator.md` - E2E test file to validate the Generate Query button functionality

## Implementation Plan
### Phase 1: Foundation
Create the backend infrastructure for query generation. This includes adding a new function to `llm_processor.py` that accepts database schema information and returns interesting natural language queries using either OpenAI or Anthropic. Add the necessary data models and API endpoint to support this functionality.

### Phase 2: Core Implementation
Implement the API endpoint in the FastAPI server that accepts requests to generate queries, retrieves the current database schema, and returns AI-generated natural language queries. Add comprehensive unit tests to validate the query generation logic works correctly with various schema configurations.

### Phase 3: Integration
Update the frontend to add the Generate Query button, connect it to the backend API, and ensure it populates the query input field correctly. Create an E2E test to validate the complete user flow. Style the button to match the Upload Data button and position it appropriately in the UI.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Data Models for Query Generation
- Open `app/server/core/data_models.py`
- Add `GenerateQueryRequest` Pydantic model (empty request body or optional parameters for preferences)
- Add `GenerateQueryResponse` Pydantic model with fields: `query` (str), `error` (optional str)
- Follow existing model patterns in the file
- Ensure proper type hints and documentation

### Step 2: Implement Query Generation Function
- Open `app/server/core/llm_processor.py`
- Add `generate_natural_language_query()` function that accepts `schema_info: Dict[str, Any]`
- Create a prompt that describes the available tables and columns
- Request the LLM to generate an interesting natural language query (max 2 sentences)
- The function should use the existing routing logic (OpenAI priority, then Anthropic)
- Return only the generated query text without any explanations
- Handle both OpenAI and Anthropic API formats
- Clean up any markdown formatting from the response

### Step 3: Create API Endpoint for Query Generation
- Open `app/server/server.py`
- Add new POST endpoint `/api/generate-query` with response model `GenerateQueryResponse`
- Import the new data models from `core.data_models`
- Get the current database schema using `get_database_schema()`
- Check if any tables exist; return error if database is empty
- Call `generate_natural_language_query()` from `llm_processor.py`
- Return the generated query in the response
- Add proper error handling and logging following existing patterns
- Handle case where no LLM API keys are configured

### Step 4: Add TypeScript Type Definitions
- Open `app/client/src/types.d.ts`
- Add `GenerateQueryRequest` interface (empty object or with optional parameters)
- Add `GenerateQueryResponse` interface matching the Pydantic model
- Ensure types match the backend models exactly

### Step 5: Add API Client Function
- Open `app/client/src/api/client.ts`
- Add `generateQuery()` function that calls `/api/generate-query` endpoint
- Use POST method with empty body or optional parameters
- Return the `GenerateQueryResponse`
- Follow existing API patterns in the file

### Step 6: Update HTML Structure
- Open `app/client/index.html`
- Locate the query controls div (`.query-controls`)
- Add a new button with id `generate-query-button` and class `secondary-button`
- Set button text to "Generate Query"
- Position the button using CSS flexbox to justify it apart from the primary buttons
- Ensure the button is visually distinct but consistent with the Upload Data button style

### Step 7: Implement Frontend Logic
- Open `app/client/src/main.ts`
- Add `initializeQueryGenerator()` function
- Get references to `generate-query-button` and `query-input` elements
- Add click event listener to the button
- On click: disable button, show loading state
- Call `api.generateQuery()` from the API client
- On success: populate the query input field (overwrite any existing content)
- On error: display error message using existing `displayError()` function
- Re-enable button and restore text after completion
- Call `initializeQueryGenerator()` from the `DOMContentLoaded` event listener

### Step 8: Add CSS Styling
- Open `app/client/src/style.css`
- Add styles for `.generate-query-button` if needed (should inherit from `secondary-button`)
- Ensure the query controls section uses flexbox with `justify-content: space-between` to separate buttons
- Add any additional styling to make the button visually consistent with Upload Data button
- Ensure responsive design considerations

### Step 9: Create Unit Tests
- Create `app/server/tests/core/test_query_generator.py`
- Import necessary modules and test data
- Test `generate_natural_language_query()` function with mock LLM responses
- Test with various schema configurations (single table, multiple tables, different column types)
- Test error handling when LLM API calls fail
- Test the routing logic between OpenAI and Anthropic
- Mock the LLM API calls to avoid actual API usage in tests
- Follow existing test patterns from `test_llm_processor.py`

### Step 10: Create E2E Test File
- Create `.claude/commands/e2e/test_query_generator.md`
- Follow the structure of `test_basic_query.md` and `test_complex_query.md`
- Include User Story describing the feature from user perspective
- Define Test Steps that verify:
  - Button is visible and clickable
  - Clicking button generates and populates a query
  - Query input field is overwritten with new content
  - Generated query can be executed successfully
  - Results are returned for the generated query
- Define Success Criteria including screenshot requirements
- Ensure the test validates the complete user flow

### Step 11: Manual Integration Testing
- Start the server and client applications
- Upload sample data (users, products, or events)
- Click the Generate Query button
- Verify that a natural language query appears in the input field
- Verify the query is relevant to the uploaded tables
- Execute the generated query and verify results are returned
- Test with different combinations of tables
- Test error handling when no tables are loaded
- Test the button's loading state and re-enabling

### Step 12: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Run unit tests for the new query generation functionality
- Run E2E test to validate the complete feature flow
- Ensure all existing tests continue to pass

## Testing Strategy
### Unit Tests
- Test `generate_natural_language_query()` with various schema structures
- Test with single table and multiple tables
- Test with different column types and configurations
- Test error handling for empty schemas
- Test LLM response parsing and cleanup
- Test routing logic between OpenAI and Anthropic providers
- Mock LLM API calls to avoid external dependencies
- Test the API endpoint with valid and invalid requests

### E2E Tests
- Test complete user flow: upload data → click Generate Query → execute query
- Verify button visibility and accessibility
- Verify query input population and overwrite behavior
- Verify generated queries are executable and return results
- Test loading states and error handling
- Capture screenshots at key interaction points

### Edge Cases
- Empty database (no tables uploaded) - should show appropriate error
- Database with single table - should generate relevant query
- Database with multiple related tables - should potentially generate join queries
- Very large schemas with many tables and columns
- LLM API timeout or failure - should show error message
- Missing API keys - should return error response
- Query generation returning more than 2 sentences - should be truncated or regenerated
- Special characters in table/column names

## Acceptance Criteria
- A "Generate Query" button is visible in the UI, styled consistently with the Upload Data button
- Button is positioned separately from primary action buttons (justify-apart layout)
- Clicking the button calls the backend API to generate a query
- Generated queries are based on actual database table schemas
- Queries are limited to maximum 2 sentences
- The generated query automatically populates the query input field
- Any existing content in the input field is overwritten
- The button shows a loading state while generating
- Error messages are displayed if generation fails (no tables, API error, etc.)
- Generated queries are relevant and interesting based on the available data
- The feature works with both OpenAI and Anthropic LLM providers
- Unit tests validate the query generation logic
- E2E test validates the complete user interaction flow
- All existing functionality continues to work without regression

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_query_generator.md` test file to validate this functionality works.

- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run new query generator unit tests
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate zero errors
- `cd app/client && bun run build` - Run frontend build to validate zero errors

## Notes
- The LLM prompt should encourage diverse and interesting queries that showcase the capabilities of the natural language interface
- Consider including examples in the prompt like: "Show me users who signed up in the last month", "What are the top 5 most expensive products?", "Count events by type"
- The query generation should be deterministic enough to be useful but random enough to provide variety on repeated clicks
- Consider adding temperature parameter to LLM calls for more creative query generation
- The button should be disabled when no tables are loaded (optional enhancement)
- Future enhancement: Allow users to specify query preferences (complexity, table focus, etc.)
- The 2-sentence limit ensures queries are concise and focused
- Consider caching recent generated queries to avoid duplicates in rapid succession (optional enhancement)
- Ensure generated queries respect SQL injection protection by only suggesting valid natural language queries, not raw SQL
