# Feature: Natural Language Query Generator Button

## Feature Description
This feature adds an intelligent query generator button to the Natural Language SQL Interface that automatically creates interesting natural language queries based on the existing database tables and their structure. When clicked, the button uses the LLM processor to analyze the current database schema and generates contextually relevant questions that users can ask about their data. The generated query is limited to two sentences maximum and automatically overwrites the input field, allowing users to execute it manually. The button is styled similarly to the "Upload Data" button and placed with justified spacing apart from the primary query buttons.

## User Story
As a user of the Natural Language SQL Interface
I want to click a button that generates interesting natural language queries based on my database tables
So that I can discover new ways to query my data and get inspiration for questions I can ask without having to think of queries from scratch

## Problem Statement
Users may not always know what questions to ask about their data, especially when working with new datasets. They need inspiration and examples of interesting queries they can run. Currently, users must manually type every query, which can be challenging when they're unfamiliar with the data structure or don't know what insights are available. This creates a barrier to exploring the data and limits the discoverability of interesting patterns and relationships within their tables.

## Solution Statement
We will add a "Generate Query" button that leverages the existing `llm_processor.py` module to analyze the current database schema (tables, columns, data types, row counts) and automatically generate contextually relevant, interesting natural language queries. The button will be styled as a secondary button (matching the "Upload Data" style) and positioned with justified spacing in the query controls section. When clicked, it will call a new backend endpoint that uses the LLM to generate a query (maximum two sentences), which will be automatically populated into the input field, overwriting any existing content. This provides users with immediate inspiration and demonstrates the types of questions they can ask about their data.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - FastAPI server with all API endpoints. Need to add a new `/api/generate-query` endpoint that uses the LLM processor to generate natural language queries based on the current database schema
- `app/server/core/llm_processor.py` - Contains LLM integration functions (`generate_sql_with_openai`, `generate_sql_with_anthropic`, `format_schema_for_prompt`). Will need to add a new function to generate natural language queries instead of SQL
- `app/server/core/sql_processor.py` - Contains `get_database_schema()` function that retrieves all tables, columns, and metadata. Will be used to get schema information for query generation
- `app/server/core/data_models.py` - Pydantic models for API requests/responses. Need to add new request/response models for the query generation endpoint
- `app/client/index.html` - Main HTML structure with query controls section. Need to add the new "Generate Query" button in the `.query-controls` div
- `app/client/src/main.ts` - TypeScript client logic for handling user interactions. Need to add event handler for the generate query button and API call
- `app/client/src/api/client.ts` - API client wrapper functions. Need to add a function to call the new generate query endpoint
- `app/client/src/style.css` - Contains all styling including button styles (`.primary-button`, `.secondary-button`). May need minor adjustments for button spacing
- `.claude/commands/test_e2e.md` - E2E test runner documentation to understand how to structure E2E tests
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test to understand test structure and format

### New Files
- `app/server/tests/core/test_query_generator.py` - Unit tests for the query generation functionality
- `.claude/commands/e2e/test_query_generator.md` - E2E test to validate the query generator button works end-to-end

## Implementation Plan

### Phase 1: Foundation
First, we'll extend the backend infrastructure to support query generation by adding new data models and a core function in the LLM processor. This involves creating Pydantic models for the request/response, and implementing the LLM prompt logic that generates interesting natural language queries based on database schema. We'll use the existing LLM routing logic (OpenAI/Anthropic) to ensure consistency with the current architecture.

### Phase 2: Core Implementation
Next, we'll implement the API endpoint in the FastAPI server and create comprehensive unit tests. The endpoint will retrieve the current database schema, pass it to the query generator function, and return the generated query. We'll ensure proper error handling, validation, and adherence to the two-sentence maximum constraint. Unit tests will cover various scenarios including empty databases, single tables, multiple tables, and error conditions.

### Phase 3: Integration
Finally, we'll integrate the feature into the frontend by adding the button to the UI, implementing the event handler and API call, and creating an E2E test to validate the complete user workflow. We'll ensure the button styling matches the "Upload Data" button, implement proper spacing using CSS flexbox justify-content, and verify that the generated query correctly overwrites the input field content.

## Step by Step Tasks

### Task 1: Add Backend Data Models
- Open `app/server/core/data_models.py`
- Add `GenerateQueryRequest` model (optional LLM provider preference)
- Add `GenerateQueryResponse` model with fields: `query` (str), `table_count` (int), `error` (Optional[str])
- Ensure models follow existing Pydantic patterns in the file

### Task 2: Implement Query Generation Function
- Open `app/server/core/llm_processor.py`
- Add `generate_natural_language_query_with_openai(schema_info: Dict[str, Any]) -> str` function
- Add `generate_natural_language_query_with_anthropic(schema_info: Dict[str, Any]) -> str` function
- Add `generate_natural_language_query(llm_provider: str, schema_info: Dict[str, Any]) -> str` routing function
- Create prompts that instruct the LLM to generate interesting, contextually relevant queries based on the schema
- Include instructions to: limit to two sentences maximum, make queries specific to the actual tables/columns, generate diverse query types (aggregations, filters, joins)
- Reuse existing helper functions like `format_schema_for_prompt` where applicable
- Handle edge cases: empty database (return helpful message), single table, multiple tables

### Task 3: Create Unit Tests for Query Generator
- Create `app/server/tests/core/test_query_generator.py`
- Test `generate_natural_language_query` with mock schema data
- Test with empty database (no tables)
- Test with single table
- Test with multiple tables
- Test that queries are limited to two sentences maximum
- Test error handling for missing API keys
- Test LLM provider routing logic

### Task 4: Add API Endpoint
- Open `app/server/server.py`
- Add `POST /api/generate-query` endpoint with `GenerateQueryResponse` response model
- Import and use `generate_natural_language_query` from `llm_processor`
- Use `get_database_schema()` to retrieve current schema
- Handle case where database is empty (no tables) - return friendly message like "Upload some data first to generate queries!"
- Add comprehensive error handling and logging
- Follow existing endpoint patterns for consistency

### Task 5: Add Frontend API Client Function
- Open `app/client/src/api/client.ts`
- Review existing API client structure
- Add `generateQuery()` function that calls `POST /api/generate-query`
- Return type should match backend `GenerateQueryResponse`
- Handle errors consistently with other API functions

### Task 6: Add Generate Query Button to HTML
- Open `app/client/index.html`
- Locate the `.query-controls` div (around line 22)
- Add a new button with id `generate-query-button` and class `secondary-button`
- Button text: "Generate Query"
- Position it after the "Upload Data" button
- Update the `.query-controls` CSS to use `justify-content: space-between` for proper spacing

### Task 7: Implement Frontend Event Handler
- Open `app/client/src/main.ts`
- Add `initializeQueryGenerator()` function following the pattern of existing init functions
- Add event listener for `generate-query-button` click
- On click: disable button, show loading state, call `api.generateQuery()`
- On success: populate the query input field with the generated query (overwrite existing content), focus the input field
- On error: display error message using existing `displayError()` function
- Always re-enable button and remove loading state in `finally` block
- Call `initializeQueryGenerator()` from the `DOMContentLoaded` event listener

### Task 8: Update CSS for Button Spacing
- Open `app/client/src/style.css`
- Review `.query-controls` styling (around line 80)
- Ensure buttons are properly spaced using flexbox properties
- Update `justify-content` to `space-between` if needed to create justified spacing
- Verify the `secondary-button` class is properly styled to match the "Upload Data" button

### Task 9: Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand E2E test structure
- Read `.claude/commands/e2e/test_basic_query.md` for example format
- Create `.claude/commands/e2e/test_query_generator.md`
- Include User Story, Test Steps, and Success Criteria
- Test steps should:
  1. Navigate to the application
  2. Upload sample data (users.json)
  3. Verify "Generate Query" button is visible
  4. Click "Generate Query" button
  5. Verify the query input field is populated with generated text
  6. Verify the generated query is non-empty and relevant to the data
  7. Click the "Query" button to execute the generated query
  8. Verify results are displayed successfully
  9. Take screenshots at each major step
- Include specific verification points for: button existence, query population, query execution, results display

### Task 10: Run All Validation Commands
- Execute all validation commands listed in the "Validation Commands" section
- Read `.claude/commands/test_e2e.md`
- Execute the new E2E test file `.claude/commands/e2e/test_query_generator.md`
- Run `cd app/server && uv run pytest` to ensure all server tests pass
- Run `cd app/client && bun tsc --noEmit` to ensure TypeScript compilation succeeds
- Run `cd app/client && bun run build` to ensure frontend builds successfully
- Verify zero regressions and all tests pass

## Testing Strategy

### Unit Tests
- **Test query generation with various schemas**: Create mock schema objects representing different database states (empty, single table, multiple tables with different column types)
- **Test sentence limit enforcement**: Verify that generated queries are limited to two sentences maximum by parsing the output and counting sentences
- **Test LLM provider routing**: Verify that the routing logic correctly selects OpenAI or Anthropic based on API key availability and request preference
- **Test error handling**: Verify graceful handling of missing API keys, LLM API failures, and invalid schema data
- **Test query relevance**: Use assertions to verify that generated queries reference actual table and column names from the schema
- **Test empty database handling**: Verify friendly error message when no tables exist

### Edge Cases
- Empty database (no tables uploaded) - should return a helpful message instructing users to upload data
- Database with single table - should generate queries specific to that table's columns
- Database with multiple related tables - should generate queries that explore relationships and potential joins
- Very large schema (many tables/columns) - should still generate focused, useful queries without being overwhelming
- LLM API timeout or failure - should return user-friendly error message
- Missing or invalid API keys - should provide clear error about configuration
- Query input field already has content - should overwrite it completely when generate button is clicked
- Rapid successive clicks on generate button - should disable button during processing to prevent duplicate requests
- Generated query exceeds two sentences - should be truncated or regenerated to meet the constraint

## Acceptance Criteria
- A "Generate Query" button is visible in the query controls section, styled to match the "Upload Data" button
- The button is positioned with justified spacing (space-between) from the primary query button
- Clicking the button calls the new `/api/generate-query` endpoint
- The endpoint returns a natural language query generated by analyzing the current database schema using LLM
- The generated query is limited to a maximum of two sentences
- The generated query is automatically populated into the query input field, overwriting any existing content
- If the database is empty (no tables), the feature displays a helpful message instead of generating a query
- The button shows a loading state while the query is being generated
- Errors are handled gracefully and displayed to the user
- All existing functionality (query execution, file upload, table management) continues to work without regression
- Unit tests achieve >90% code coverage for the new query generation functions
- E2E test validates the complete user workflow from button click to query population to query execution
- TypeScript compilation succeeds with no errors
- Frontend build completes successfully

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_query_generator.md` to validate the query generator functionality works end-to-end with visual confirmation
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run specific query generator tests to ensure comprehensive coverage
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes
- The feature leverages the existing `llm_processor.py` infrastructure to maintain consistency with the current architecture
- We use the same LLM routing logic (OpenAI/Anthropic) as the existing query-to-SQL conversion feature
- The two-sentence limit ensures queries are concise and focused, improving user experience
- The button placement using `justify-content: space-between` creates visual balance in the UI
- Future enhancements could include: generating multiple query suggestions, saving favorite queries, query history, or categorizing queries by type (aggregation, filtering, joins, etc.)
- Consider rate limiting on the backend if this feature is used frequently to manage API costs
- The generated queries should be diverse and explore different aspects of the data (counts, filters, aggregations, joins) rather than repetitive
- The feature works best with meaningful table and column names - consider adding a note in the documentation encouraging users to use descriptive names when uploading data
