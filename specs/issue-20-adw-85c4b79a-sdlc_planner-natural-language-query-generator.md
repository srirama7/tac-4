# Feature: Natural Language Query Generator Button

## Feature Description
This feature adds a new button to the main interface that automatically generates interesting natural language queries based on the existing database tables and their structures. When clicked, the button uses the LLM processor to create contextually relevant queries that showcase the capabilities of the application. The generated query will overwrite the current content in the query input field, allowing users to execute it manually. The generated queries will be limited to two sentences maximum for clarity and brevity.

## User Story
As a user
I want a button that generates sample natural language queries based on my uploaded data
So that I can quickly explore my data without having to think of queries myself

## Problem Statement
Users often face a "blank slate" problem when first using the Natural Language SQL Interface. After uploading their data, they may not know what kinds of questions to ask or how to phrase their queries effectively. This creates friction in the user experience and reduces engagement with the application. Users need inspiration and examples of what types of queries are possible with their specific dataset.

## Solution Statement
Introduce a "Generate Query" button positioned alongside the existing primary buttons in the query controls section. This button will:
1. Analyze the current database schema (tables, columns, data types, row counts)
2. Use the existing LLM processor infrastructure to generate contextually relevant natural language queries
3. Populate the query input field with the generated query, overwriting any existing content
4. Provide users with immediate, actionable examples tailored to their data

The solution leverages the existing `llm_processor.py` module and schema retrieval functionality, requiring minimal new infrastructure while providing significant value to the user experience.

## Relevant Files
Use these files to implement the feature:

- **app/server/core/llm_processor.py** - Contains the LLM processing logic that will be extended to support query generation. Currently handles SQL generation from natural language; will be enhanced to generate natural language queries from schema.

- **app/server/server.py** - FastAPI server where the new API endpoint `/api/generate-query` will be added to handle query generation requests. Follows existing patterns for health checks, schema retrieval, and query processing.

- **app/server/core/data_models.py** - Pydantic models where new request/response models (`GenerateQueryRequest` and `GenerateQueryResponse`) will be defined to ensure type safety and validation.

- **app/server/core/sql_processor.py** - Contains `get_database_schema()` function that will be used to retrieve table structures and column information for the query generation logic.

- **app/client/src/main.ts** - Main TypeScript file where the button click handler and query generation logic will be implemented. Will add event listener and integrate with the new API endpoint.

- **app/client/src/api/client.ts** - API client module where the new `generateQuery()` method will be added to communicate with the backend endpoint.

- **app/client/src/types.d.ts** - TypeScript type definitions where `GenerateQueryRequest` and `GenerateQueryResponse` types will be declared for frontend type safety.

- **app/client/index.html** - HTML template where the new "Generate Query" button will be added to the `.query-controls` section, positioned alongside existing buttons.

- **app/client/src/style.css** - Stylesheet where the button will be styled to match the "Upload Data" button's secondary style as specified in requirements.

### New Files

- **.claude/commands/e2e/test_query_generator.md** - E2E test file that validates the query generator button functionality, including button presence, click interaction, query population, and successful execution. Will follow the pattern established in `test_basic_query.md` and `test_complex_query.md`.

- **app/server/tests/core/test_query_generator.py** - Unit tests for the backend query generation logic, including tests for schema parsing, LLM interaction, query validation, and edge cases (empty database, single table, multiple tables).

## Implementation Plan

### Phase 1: Foundation
First, establish the backend infrastructure to support query generation. This includes:
1. Creating new Pydantic data models for request/response handling
2. Implementing the core query generation logic in `llm_processor.py` that analyzes database schema and generates contextually relevant natural language queries
3. Adding a new FastAPI endpoint to expose the query generation functionality
4. Writing comprehensive unit tests to validate the backend logic

### Phase 2: Core Implementation
With the backend in place, build the frontend components:
1. Add TypeScript type definitions for the new API models
2. Extend the API client with a method to call the query generation endpoint
3. Add the "Generate Query" button to the HTML interface in the appropriate location
4. Implement the button click handler that calls the API and populates the input field
5. Style the button to match the existing design system (secondary button style)

### Phase 3: Integration
Integrate and validate the complete feature:
1. Create an E2E test file that validates the end-to-end user flow
2. Test the feature with various database states (no tables, single table, multiple tables)
3. Ensure the generated queries are executable and produce meaningful results
4. Validate that the feature works with both OpenAI and Anthropic LLM providers
5. Run all validation commands to ensure zero regressions

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Task 1: Create Backend Data Models
- Add `GenerateQueryRequest` model to `app/server/core/data_models.py` (empty or minimal fields)
- Add `GenerateQueryResponse` model with fields: `query` (str), `tables_analyzed` (List[str]), and optional `error` (str)
- Follow existing Pydantic model patterns in the file
- Import necessary types from `typing` module

### Task 2: Implement Query Generation Logic in LLM Processor
- Add `generate_natural_language_query()` function to `app/server/core/llm_processor.py`
- Function should accept schema information (Dict[str, Any]) as input
- Create a prompt that asks the LLM to generate an interesting natural language query based on table structures
- Implement logic to format schema information into a concise, LLM-friendly prompt
- Add constraint to limit generated queries to two sentences maximum
- Support both OpenAI and Anthropic providers using existing routing logic
- Return the generated natural language query as a string
- Handle edge cases: empty database (no tables), single table, multiple tables
- Add appropriate error handling and logging

### Task 3: Create Unit Tests for Query Generator
- Create `app/server/tests/core/test_query_generator.py`
- Test `generate_natural_language_query()` with mock schema data
- Test with empty schema (no tables) - should return helpful error
- Test with single table schema
- Test with multiple table schema
- Test query length constraint (max two sentences)
- Mock LLM API calls to avoid actual API usage during tests
- Validate response format and structure

### Task 4: Add API Endpoint
- Add `/api/generate-query` POST endpoint to `app/server/server.py`
- Endpoint should accept `GenerateQueryRequest` and return `GenerateQueryResponse`
- Call `get_database_schema()` to retrieve current schema
- Call `generate_natural_language_query()` with schema information
- Include error handling and logging following existing patterns
- Return appropriate error messages if database is empty

### Task 5: Add Frontend Type Definitions
- Add `GenerateQueryRequest` and `GenerateQueryResponse` interfaces to `app/client/src/types.d.ts`
- Ensure types match the backend Pydantic models
- Follow existing type definition patterns in the file

### Task 6: Extend API Client
- Add `generateQuery()` method to `app/client/src/api/client.ts`
- Method should call the `/api/generate-query` endpoint
- Return `Promise<GenerateQueryResponse>`
- Follow existing API method patterns (error handling, type safety)

### Task 7: Add Generate Query Button to HTML
- Add new button element to `app/client/index.html` in the `.query-controls` div
- Button ID: `generate-query-button`
- Button text: "Generate Query"
- Button class: `secondary-button` (to match "Upload Data" style)
- Position button between the "Query" and "Upload Data" buttons using `justify-content: space-between` or similar flex layout

### Task 8: Implement Button Click Handler
- Add `initializeGenerateQuery()` function to `app/client/src/main.ts`
- Add event listener for the "Generate Query" button click
- On click, disable the button and show loading state
- Call `api.generateQuery()` method
- On success, overwrite the content of `query-input` textarea with the generated query
- On error, call `displayError()` with appropriate error message
- Re-enable button after completion
- Call `initializeGenerateQuery()` from the DOMContentLoaded event listener

### Task 9: Style the Generate Query Button
- Verify the button inherits the correct `.secondary-button` styles from `app/client/src/style.css`
- Ensure button is properly positioned with appropriate spacing using flex gap
- Test hover and disabled states
- Ensure visual consistency with "Upload Data" button

### Task 10: Create E2E Test File
- Create `.claude/commands/e2e/test_query_generator.md` following the pattern of `test_basic_query.md`
- Test steps should include:
  1. Navigate to application URL
  2. Take screenshot of initial state
  3. Verify "Generate Query" button is present
  4. Upload sample data (users.json)
  5. Click "Generate Query" button
  6. Verify query input field is populated with generated text
  7. Take screenshot of populated query
  8. Verify generated query is not empty and is 2 sentences or less
  9. Click "Query" button to execute the generated query
  10. Verify results appear without errors
  11. Take screenshot of successful results
- Success criteria: Button exists, generates query, query is valid and executable, results display correctly
- Minimum 3 screenshots required

### Task 11: Manual Testing
- Start the application using `./scripts/start.sh`
- Upload sample data (users.json, products.csv, events.jsonl)
- Click "Generate Query" button multiple times to verify variety
- Execute generated queries to ensure they're valid
- Test with empty database (no tables) to verify error handling
- Test with single table and multiple tables
- Verify button styling matches design requirements

### Task 12: Run Validation Commands
- Execute all validation commands listed in the "Validation Commands" section below
- Ensure all tests pass with zero failures
- Fix any regressions or failures before marking feature as complete

## Testing Strategy

### Unit Tests
- **Test: Empty Database Handling**
  - Given: Database with no tables
  - When: Query generation is requested
  - Then: Should return appropriate error message indicating no tables are available

- **Test: Single Table Query Generation**
  - Given: Database with one table (users)
  - When: Query generation is requested
  - Then: Should generate a query referencing the users table and its columns

- **Test: Multiple Table Query Generation**
  - Given: Database with multiple tables (users, products, events)
  - When: Query generation is requested
  - Then: Should generate a query that may involve joins or focuses on an interesting table

- **Test: Query Length Constraint**
  - Given: Any database schema
  - When: Query is generated
  - Then: Generated query should not exceed two sentences

- **Test: LLM Provider Routing**
  - Given: OpenAI API key is available
  - When: Query generation is requested
  - Then: Should use OpenAI provider (following existing routing logic)

- **Test: Error Handling**
  - Given: LLM API call fails
  - When: Query generation is requested
  - Then: Should return error response with appropriate message

### Edge Cases
1. **No Tables in Database**
   - User clicks "Generate Query" before uploading any data
   - Expected: Friendly error message indicating data needs to be uploaded first

2. **Very Large Schema**
   - Database with many tables (10+) and columns (100+)
   - Expected: LLM should handle gracefully, possibly focusing on a subset of interesting tables

3. **Tables with Complex Column Names**
   - Tables with special characters, long names, or unusual data types
   - Expected: Query generation should handle without errors, properly reference columns

4. **Rapid Button Clicking**
   - User clicks "Generate Query" button multiple times quickly
   - Expected: Button should disable during API call, prevent multiple simultaneous requests

5. **Query Overwriting**
   - User has typed a query in the input field, then clicks "Generate Query"
   - Expected: Input field content should be overwritten (as per requirements)

6. **Missing API Keys**
   - Neither OpenAI nor Anthropic API keys are configured
   - Expected: Graceful error message indicating API key configuration needed

## Acceptance Criteria
1. ✓ "Generate Query" button is visible in the query controls section
2. ✓ Button is styled consistently with "Upload Data" button (secondary style)
3. ✓ Button is positioned with appropriate spacing between "Query" and "Upload Data" buttons
4. ✓ Clicking the button triggers an API call to `/api/generate-query`
5. ✓ Generated query is limited to maximum two sentences
6. ✓ Generated query overwrites existing content in the input field
7. ✓ Generated queries are contextually relevant to uploaded tables and their structures
8. ✓ Button shows loading state while API call is in progress
9. ✓ Button is disabled during API call to prevent duplicate requests
10. ✓ Error messages are displayed appropriately when generation fails
11. ✓ Empty database state is handled gracefully with helpful error message
12. ✓ Feature works with both OpenAI and Anthropic LLM providers
13. ✓ Generated queries are executable and produce valid results
14. ✓ E2E test validates complete user workflow
15. ✓ All unit tests pass
16. ✓ All validation commands pass with zero regressions

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test `.claude/commands/e2e/test_query_generator.md` to validate this functionality works
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run new query generator unit tests
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Implementation Considerations
1. **LLM Prompt Engineering**: The prompt sent to the LLM should be carefully crafted to:
   - Request exactly one natural language query (not multiple)
   - Emphasize the two-sentence maximum constraint
   - Ask for "interesting" or "useful" queries that demonstrate the application's capabilities
   - Provide schema information in a clear, structured format
   - Request queries that are likely to return meaningful results (avoid overly restrictive filters)

2. **Query Variety**: To provide a better user experience, consider adding randomization or variation to the LLM prompt so users get different queries when clicking the button multiple times

3. **Button Placement**: The requirement states "justify apart from our current primary buttons" - this likely means using flexbox with `justify-content: space-between` or similar to create visual separation

4. **Loading State**: Follow the existing pattern in `initializeQueryInput()` where the button is disabled and shows a loading spinner during API calls

5. **Error Messages**: Provide clear, actionable error messages:
   - If no tables exist: "Please upload data first to generate queries"
   - If API call fails: Display the specific error from the backend
   - If API keys missing: "LLM API configuration required"

### Future Enhancements
- Add a "favorites" feature to save generated queries
- Implement query history to track previously generated queries
- Add difficulty levels (simple, moderate, complex) for query generation
- Support generating queries for specific tables (user selects table first)
- Add tooltips explaining what the button does for first-time users
- Implement keyboard shortcuts (e.g., Ctrl+G) to trigger query generation

### Schema Format Reference
The schema returned by `get_database_schema()` has this structure:
```python
{
    'tables': {
        'table_name': {
            'columns': {'col_name': 'col_type', ...},
            'row_count': 123
        },
        ...
    }
}
```

This should be transformed into a prompt that helps the LLM understand the available data and generate relevant queries.
