# Feature: Natural Language Query Generator Button

## Feature Description
Add a "Generate Query" button to the Natural Language SQL Interface that automatically creates interesting natural language queries based on the existing database tables and their structure. When clicked, the button will use the LLM processor to analyze the available tables and columns, generate a contextually relevant natural language query (limited to two sentences), and populate the query input field with the generated text, overwriting any existing content. The button will be styled similarly to the "Upload Data" button and positioned with space-between justification to separate it from the primary query button, providing users with an easy way to explore their data through AI-generated query suggestions.

## User Story
As a user
I want to click a button that generates natural language queries based on my database structure
So that I can discover interesting insights and learn how to query my data without having to think of queries myself

## Problem Statement
Users who upload data to the Natural Language SQL Interface may not immediately know what questions to ask about their data. This can lead to an empty query input field and uncertainty about how to begin exploring their dataset. New users especially may struggle to understand what kinds of questions are possible or relevant for their specific data structure. There is currently no way for users to get query suggestions or examples based on their actual database schema.

## Solution Statement
Implement a "Generate Query" button that:
1. Analyzes the current database schema including table names, column names, column types, and row counts
2. Uses the existing LLM processor infrastructure to generate contextually relevant natural language queries
3. Creates interesting queries that leverage the actual structure and relationships in the user's data
4. Populates the query input field with the generated text (maximum two sentences), overwriting any existing content
5. Provides a seamless user experience with appropriate loading states and error handling
6. Is positioned separately from the primary "Query" button using space-between justification
7. Uses the secondary button style (matching "Upload Data") for visual consistency

## Relevant Files
Use these files to implement the feature:

- `app/client/index.html` - Contains the query section HTML where the new "Generate Query" button needs to be added with proper styling and positioning
- `app/client/src/main.ts` - Contains the frontend JavaScript logic where we'll add event handlers for the new button and implement the query generation flow
- `app/client/src/api/client.ts` - Contains API client methods; needs a new method to call the query generation endpoint
- `app/client/src/types.d.ts` - Contains TypeScript type definitions; needs types for the new query generation request and response
- `app/server/server.py` - Main FastAPI server file; needs a new POST endpoint `/api/generate-query` to handle query generation requests
- `app/server/core/llm_processor.py` - Contains LLM processing logic; needs a new function to generate natural language queries based on schema information
- `app/server/core/data_models.py` - Contains Pydantic models; needs request and response models for the query generation endpoint
- `app/server/core/sql_processor.py` - Contains database schema retrieval logic that will be used to provide context for query generation
- `app/client/src/style.css` - Contains CSS styles; may need updates to ensure proper button styling and spacing
- `.claude/commands/test_e2e.md` - Instructions for running E2E tests
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test structure to understand testing patterns

### New Files
- `app/server/tests/test_generate_query.py` - Unit tests for the new query generation functionality
- `.claude/commands/e2e/test_query_generator.md` - E2E test file to validate the query generator button works correctly in the UI

## Implementation Plan
### Phase 1: Foundation
Set up the backend infrastructure for query generation by creating the necessary data models, implementing the core LLM prompt logic to generate interesting queries based on database schemas, and establishing the API endpoint. This foundational work will enable the frontend to request and receive generated queries.

### Phase 2: Core Implementation
Implement the backend query generation function that analyzes table structures, column types, and relationships to create contextually relevant natural language queries. The function will use the existing LLM processor infrastructure but with a specialized prompt designed to generate exploration-focused questions. Implement proper error handling and ensure the generated queries are limited to two sentences maximum.

### Phase 3: Integration
Connect the backend functionality to the frontend by adding the "Generate Query" button to the UI, implementing the click handler, adding loading states, and ensuring the generated query properly populates the input field. Style the button to match the "Upload Data" button and position it with appropriate spacing using flexbox justify-content: space-between. Create comprehensive E2E tests to validate the complete user experience.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Backend Data Models
- Add `GenerateQueryRequest` model to `app/server/core/data_models.py` with no required fields (uses current schema)
- Add `GenerateQueryResponse` model with fields: `query` (str), `tables_analyzed` (List[str]), `error` (Optional[str])
- Follow existing Pydantic model patterns used in the file
- Add proper type hints and Field descriptions

### Step 2: Implement Query Generation Function
- Add `generate_natural_language_query()` function to `app/server/core/llm_processor.py`
- Function should accept schema_info (Dict[str, Any]) parameter
- Create a specialized prompt that instructs the LLM to generate interesting exploratory questions
- Prompt should emphasize: relevance to the actual schema, two sentence maximum, interesting insights
- Use the existing `format_schema_for_prompt()` function to format schema information
- Follow the routing logic pattern from `generate_sql()` to support both OpenAI and Anthropic
- Return a concise natural language query string (two sentences max)

### Step 3: Create API Endpoint
- Add POST `/api/generate-query` endpoint to `app/server/server.py`
- Endpoint should call `get_database_schema()` to retrieve current schema
- Call the new `generate_natural_language_query()` function with schema info
- Return `GenerateQueryResponse` with the generated query and list of tables analyzed
- Include proper error handling and logging following existing endpoint patterns
- Handle edge case when no tables are loaded (return helpful error message)

### Step 4: Add Unit Tests for Backend
- Create `app/server/tests/test_generate_query.py` test file
- Test query generation with various schema structures (single table, multiple tables, different column types)
- Test error handling when no tables exist
- Test LLM provider routing (OpenAI vs Anthropic)
- Mock LLM API calls following patterns from `test_llm_processor.py`
- Test that generated queries are properly formatted and within length limits

### Step 5: Add Frontend TypeScript Types
- Add `GenerateQueryRequest` interface to `app/client/src/types.d.ts` (empty object)
- Add `GenerateQueryResponse` interface with fields: query (string), tables_analyzed (string[]), error (optional string)
- Ensure types match backend Pydantic models exactly

### Step 6: Add API Client Method
- Add `generateQuery()` method to the api object in `app/client/src/api/client.ts`
- Method should make POST request to `/generate-query` endpoint
- Return Promise<GenerateQueryResponse>
- Follow existing API method patterns in the file

### Step 7: Add Generate Query Button to UI
- Add new button to `app/client/index.html` in the `query-controls` div
- Button id: `generate-query-button`
- Button text: "Generate Query"
- Button class: `secondary-button` (matches Upload Data button style)
- Position after the "Upload Data" button
- Update `.query-controls` CSS in `style.css` to use `justify-content: space-between` for proper spacing
- Create a visual grouping with "Query" button on the left and "Upload Data" + "Generate Query" buttons on the right

### Step 8: Implement Frontend Logic
- Add `initializeGenerateQuery()` function to `app/client/src/main.ts`
- Call this function in the DOMContentLoaded event handler
- Add click event handler for the generate query button
- Implement loading state: disable button and show loading spinner during generation
- Call `api.generateQuery()` and handle response
- Populate the query input field with the generated query, overwriting any existing content
- Handle errors with appropriate user feedback using existing `displayError()` function
- Re-enable button after completion or error

### Step 9: Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand E2E test structure
- Read `.claude/commands/e2e/test_basic_query.md` to understand test format
- Create `.claude/commands/e2e/test_query_generator.md` file
- Include User Story describing the query generation feature
- Define Test Steps that:
  1. Navigate to application
  2. Upload sample data (users.json)
  3. Verify "Generate Query" button is present
  4. Click "Generate Query" button
  5. Verify loading state appears
  6. Verify query input is populated with generated text
  7. Verify generated query is not empty and ≤ 2 sentences
  8. Click "Query" button to execute the generated query
  9. Verify results are displayed successfully
  10. Take screenshots at key steps
- Define Success Criteria with specific validations
- Follow the exact format from existing E2E test files

### Step 10: Test Backend Functionality
- Run unit tests for the new query generation function
- Test with different database schemas manually
- Verify error handling when no tables exist
- Ensure generated queries are relevant and well-formed

### Step 11: Test Frontend Integration
- Manually test the button appears in correct position
- Verify spacing between buttons looks correct
- Test loading states and error handling
- Test that generated query properly overwrites input field
- Test with multiple tables and verify query relevance

### Step 12: Run Validation Commands
- Execute all validation commands listed below
- Ensure zero regressions in existing functionality
- Run the new E2E test to validate end-to-end functionality
- Fix any issues that arise during validation

## Testing Strategy
### Unit Tests
- Test `generate_natural_language_query()` with various schema structures
- Test query generation with single table containing different column types
- Test query generation with multiple related tables
- Test error handling when schema is empty or invalid
- Test that generated queries are within two sentence limit
- Test LLM provider routing (OpenAI vs Anthropic fallback)
- Mock LLM API responses to ensure consistent test results
- Test API endpoint response format and error cases

### Integration Tests
- Test complete flow from button click to query population
- Test that generated queries can be successfully executed
- Test loading states and UI feedback
- Test error handling when API fails
- Test button positioning and styling
- Test with various database schemas (empty, single table, multiple tables)

### Edge Cases
- No tables loaded in database (should show helpful error)
- Database with single table and single column
- Database with many tables (10+)
- LLM API timeout or failure
- Generated query exceeds two sentences (should be truncated)
- Rapid clicking of generate button (should prevent duplicate requests)
- Network failure during generation
- Special characters in table/column names

## Acceptance Criteria
- "Generate Query" button appears in the UI next to "Upload Data" button
- Button uses secondary button styling matching "Upload Data" button
- Buttons are properly spaced using justify-content: space-between layout
- Clicking the button triggers query generation based on current database schema
- Generated queries are contextually relevant to the actual tables and columns
- Generated queries are limited to maximum two sentences
- Query input field is populated with generated text, overwriting any existing content
- Button shows loading state during query generation
- Appropriate error messages are displayed if generation fails
- Feature works with both OpenAI and Anthropic LLM providers
- No regressions in existing query or upload functionality
- Backend unit tests achieve >90% code coverage for new code
- E2E test successfully validates the complete user workflow
- Generated queries can be successfully executed by clicking the "Query" button

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/test_generate_query.py -v` - Run new query generation unit tests
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_query_generator.md` to validate the query generator button functionality works end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes
- The query generation function should use the existing LLM processor infrastructure to maintain consistency
- Consider using a temperature parameter of 0.7-0.8 for more creative query suggestions (higher than the 0.1 used for SQL generation)
- The prompt should encourage queries that showcase interesting data relationships, not just simple "SELECT *" queries
- Limit generated queries to two sentences maximum to ensure they fit well in the input field
- The button should always overwrite the input field content to prevent confusion about what query will be executed
- Consider adding a max_tokens limit to the LLM call to enforce brevity (e.g., 100 tokens)
- Follow existing security patterns - the generated queries will still go through SQL injection protection when executed
- The feature works best when tables have meaningful names and diverse column types
- Future enhancement: Could add a "regenerate" feature to get different query suggestions
- Future enhancement: Could analyze sample data values to make queries more specific
- Make sure the button is accessible (proper ARIA labels, keyboard navigation)
- Test with both empty databases and databases with multiple tables
- Consider caching schema info to avoid repeated database queries during generation
