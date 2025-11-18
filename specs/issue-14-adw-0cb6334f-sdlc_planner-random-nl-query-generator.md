# Feature: Random Natural Language Query Generator

## Feature Description
This feature adds an intelligent query generator button that automatically creates interesting, contextual natural language queries based on the current database schema and table structure. When clicked, the button generates a random natural language query (maximum two sentences) using the LLM processor to analyze available tables and their columns, then populates the query input field with this generated query. The query overwrites any existing content in the field and is ready for the user to execute manually. This feature helps users explore their data by providing example queries they can run or modify.

## User Story
As a user
I want to generate random natural language queries based on my database tables
So that I can discover interesting ways to query my data without having to think of queries myself

## Problem Statement
Users may not know what questions to ask about their data, especially when working with new or unfamiliar datasets. They need inspiration and examples of the types of queries they can execute against their tables. Currently, users must manually craft their own natural language queries, which can be time-consuming and may not showcase the full capabilities of the system.

## Solution Statement
Implement a "Generate Query" button that leverages the existing LLM processor infrastructure to create contextual, meaningful natural language queries. The button will analyze the current database schema (tables, columns, and data types), send this information to the LLM with a specialized prompt requesting an interesting query, and populate the query input field with the generated result. The button will be styled consistently with the "Upload Data" button and positioned separately from primary action buttons using space-between justification.

## Relevant Files
Use these files to implement the feature:

- **app/server/core/llm_processor.py** - Contains the LLM integration functions (generate_sql_with_openai, generate_sql_with_anthropic, format_schema_for_prompt). Will add a new function `generate_random_query()` to create natural language queries based on schema.

- **app/server/server.py** - FastAPI server with existing endpoints. Will add a new POST endpoint `/api/generate-query` that returns a random natural language query based on the current database schema.

- **app/server/core/data_models.py** - Contains Pydantic models for API requests/responses. Will add `GenerateQueryRequest` and `GenerateQueryResponse` models.

- **app/client/index.html** - Contains the HTML structure including the query controls section. Will add the "Generate Query" button next to the existing buttons with proper styling.

- **app/client/src/main.ts** - Main TypeScript file handling UI interactions and API calls. Will add initialization for the generate query button and handle the click event to call the API and populate the input field.

- **app/client/src/api/client.ts** - API client with methods for backend communication. Will add a `generateRandomQuery()` method to call the new endpoint.

- **app/client/src/types.d.ts** - TypeScript type definitions. Will add types for the generate query request/response.

- **app/client/src/style.css** - Contains all styling. Will add styles for the generate query button to match the Upload Data button style.

### New Files

- **.claude/commands/e2e/test_random_query_generator.md** - E2E test file that validates the random query generation feature works correctly, including button visibility, API call, and input field population.

- **app/server/tests/core/test_generate_query.py** - Unit tests for the random query generation functionality, testing various schema configurations and edge cases.

## Implementation Plan

### Phase 1: Foundation
First, establish the backend infrastructure to support random query generation. This includes creating the LLM processor function that can analyze database schemas and generate contextual natural language queries, defining the data models for the new API endpoint, and implementing the FastAPI endpoint that orchestrates the query generation process. The foundation ensures we have a solid, testable backend before moving to frontend integration.

### Phase 2: Core Implementation
Build the frontend components including the new button UI element, API client integration, and event handling logic. This phase focuses on creating a seamless user experience where clicking the button triggers query generation and populates the input field. The UI will be styled consistently with existing buttons and positioned appropriately in the interface layout.

### Phase 3: Integration
Connect all components together and validate the end-to-end flow works correctly. This includes testing the complete user journey from button click through API call to input field population, ensuring error handling works properly, and verifying the feature integrates smoothly with existing query execution functionality. Create comprehensive E2E tests to validate the feature in a real browser environment.

## Step by Step Tasks

### 1. Backend: Create Data Models
- Open `app/server/core/data_models.py`
- Add `GenerateQueryRequest` model (empty model, no input needed)
- Add `GenerateQueryResponse` model with fields: `query` (str), `tables_used` (List[str]), `error` (Optional[str])
- Ensure imports include List from typing

### 2. Backend: Implement Random Query Generation Function
- Open `app/server/core/llm_processor.py`
- Create new function `generate_random_query(schema_info: Dict[str, Any]) -> str`
- Function should:
  - Format the schema information for the LLM
  - Create a prompt requesting an interesting natural language query (max 2 sentences)
  - Use the same routing logic as `generate_sql()` to choose between OpenAI and Anthropic
  - Call the LLM with temperature ~0.7 for creativity
  - Return the generated natural language query text
- Create separate helper functions `generate_random_query_with_openai()` and `generate_random_query_with_anthropic()`
- Handle edge cases: no tables, single table, multiple tables

### 3. Backend: Add API Endpoint
- Open `app/server/server.py`
- Add new POST endpoint `/api/generate-query` with response model `GenerateQueryResponse`
- Import `GenerateQueryRequest` and `GenerateQueryResponse` from data_models
- Import the new `generate_random_query` function from llm_processor
- Endpoint should:
  - Get current database schema using `get_database_schema()`
  - Check if tables exist (return error if no tables)
  - Call `generate_random_query()` with schema info
  - Return response with generated query and list of tables
  - Handle errors gracefully with appropriate error messages
  - Add logging for success and failure cases

### 4. Backend: Write Unit Tests
- Create `app/server/tests/core/test_generate_query.py`
- Test `generate_random_query()` with mock schema data
- Test cases:
  - Single table with various column types
  - Multiple tables with relationships
  - Empty database (no tables)
  - Edge case: table with single column
  - Verify query length is reasonable (not too long)
  - Test both OpenAI and Anthropic providers (with mocks)

### 5. Frontend: Add TypeScript Types
- Open `app/client/src/types.d.ts`
- Add `GenerateQueryRequest` interface (empty, no fields needed)
- Add `GenerateQueryResponse` interface with: query (string), tables_used (string[]), error (optional string)

### 6. Frontend: Update API Client
- Open `app/client/src/api/client.ts`
- Add new method `generateRandomQuery()` to the api object
- Method should:
  - Make POST request to `/generate-query`
  - Return Promise<GenerateQueryResponse>
  - Use the existing `apiRequest` helper function

### 7. Frontend: Add Button to HTML
- Open `app/client/index.html`
- Locate the `.query-controls` div (around line 22)
- Update the div structure to include a new button:
  - Add a wrapper div with class `button-group-left` for Query and Upload Data buttons
  - Add a wrapper div with class `button-group-right` for the new Generate Query button
  - Use parent flex container with `justify-content: space-between`
- Add button with id `generate-query-button` and class `secondary-button`
- Button text should be "Generate Query"

### 8. Frontend: Add CSS Styling
- Open `app/client/src/style.css`
- Add styles for `.query-controls` to use flexbox with space-between
- Add styles for `.button-group-left` and `.button-group-right`
- Ensure `.secondary-button` style matches the Upload Data button
- Add any loading state styles for the generate button
- Ensure responsive behavior on smaller screens

### 9. Frontend: Implement Button Handler
- Open `app/client/src/main.ts`
- Create new function `initializeGenerateQuery()`
- Function should:
  - Get reference to the generate query button
  - Add click event listener
  - On click: disable button, show loading state
  - Call `api.generateRandomQuery()`
  - On success: populate the query input field (overwrite existing content)
  - On error: display error message to user
  - Re-enable button and restore original text
  - Handle edge case: no tables in database (show helpful message)
- Call `initializeGenerateQuery()` from the DOMContentLoaded listener

### 10. Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand the E2E test format
- Read `.claude/commands/e2e/test_basic_query.md` to understand test structure
- Create `.claude/commands/e2e/test_random_query_generator.md`
- Test should include:
  - **User Story**: Testing random query generation feature
  - **Test Steps**:
    1. Navigate to application URL
    2. Screenshot initial state
    3. Verify Generate Query button is present and visible
    4. Load sample data (users table)
    5. Click Generate Query button
    6. Verify query input field is populated with generated query
    7. Screenshot the populated query
    8. Verify query is not empty and is max 2 sentences
    9. Click Query button to execute the generated query
    10. Verify results are displayed
    11. Screenshot the results
  - **Success Criteria**: Button exists, generates query, populates field, query is executable

### 11. Integration Testing
- Manually test the complete flow:
  - Start server and client
  - Upload sample data
  - Click Generate Query button multiple times
  - Verify different queries are generated
  - Verify queries can be executed successfully
  - Test with no tables loaded (should show error)
  - Test with single table
  - Test with multiple tables

### 12. Run Validation Commands
- Execute all validation commands from the Validation Commands section
- Ensure zero regressions
- Verify all tests pass
- Execute the E2E test and verify it passes

## Testing Strategy

### Unit Tests
- **Backend Query Generation Tests** (`test_generate_query.py`):
  - Test query generation with various schema configurations
  - Test with empty database (no tables)
  - Test with single table and single column
  - Test with multiple tables
  - Test LLM provider routing logic
  - Test error handling for API failures
  - Mock LLM API calls to avoid actual API usage in tests

- **Backend Endpoint Tests**:
  - Test `/api/generate-query` returns valid response
  - Test endpoint with no tables returns appropriate error
  - Test endpoint handles LLM errors gracefully

- **Frontend Integration**:
  - Verify button click triggers API call
  - Verify input field is populated correctly
  - Verify error states display properly

### Edge Cases
- **No tables in database**: Should return error message "No tables available. Please upload data first."
- **Single table with one column**: Should still generate a meaningful query
- **Very long table/column names**: Should handle gracefully
- **LLM API failure**: Should display user-friendly error message
- **Network timeout**: Should handle timeout gracefully
- **Multiple rapid clicks**: Should prevent multiple simultaneous requests (disable button during loading)
- **Query generation returns empty string**: Should handle and show error
- **Query generation returns very long query**: Should truncate or handle appropriately
- **Database connection failure**: Should return error without crashing

## Acceptance Criteria
1. A "Generate Query" button is visible in the UI, styled like the "Upload Data" button
2. The button is positioned separately from primary buttons using space-between justification
3. Clicking the button generates a natural language query based on current database tables
4. The generated query is limited to a maximum of two sentences
5. The generated query overwrites any existing content in the query input field
6. The generated query is contextually relevant to the available tables and columns
7. The button shows a loading state while generating the query
8. If no tables exist, an appropriate error message is displayed to the user
9. The generated query can be successfully executed by clicking the "Query" button
10. The feature works with both OpenAI and Anthropic LLM providers
11. All existing functionality continues to work without regression
12. Unit tests pass with 100% success rate
13. E2E test validates the complete user journey successfully
14. Multiple clicks generate different queries (queries should vary)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

**Backend Tests:**
```bash
cd app/server && uv run pytest tests/core/test_generate_query.py -v
```

**All Server Tests (Regression Check):**
```bash
cd app/server && uv run pytest -v
```

**Frontend Type Check:**
```bash
cd app/client && bun tsc --noEmit
```

**Frontend Build (Production Ready):**
```bash
cd app/client && bun run build
```

**E2E Test Execution:**
- Read `.claude/commands/test_e2e.md` to understand how to run E2E tests
- Read and execute `.claude/commands/e2e/test_random_query_generator.md` to validate the random query generation feature works end-to-end
- Verify all screenshots are captured successfully
- Verify test passes with status "passed"

**Manual Validation:**
1. Start the application: `./scripts/start.sh`
2. Upload sample data (users.json)
3. Click "Generate Query" button
4. Verify query appears in input field
5. Execute the generated query
6. Verify results display correctly
7. Test with multiple tables loaded
8. Test with no tables (should show error)

## Notes

### Design Decisions
- **Two sentence limit**: Keeps queries concise and focused, easier for users to understand
- **Overwrite input field**: Clear intent - user gets a fresh query each time
- **Secondary button style**: Matches "Upload Data" visual hierarchy as a supporting action
- **Space-between layout**: Visually separates exploration (Generate Query) from primary actions (Query, Upload)

### LLM Prompt Strategy
The prompt for generating random queries should:
- Request queries that showcase interesting data relationships
- Vary between aggregations, filters, and joins when multiple tables exist
- Use natural, conversational language
- Consider the data types of columns (e.g., date ranges for date columns)
- Temperature should be higher (~0.7-0.8) to encourage variety across generations

### Future Enhancements
- Add query history/favorites so users can save interesting generated queries
- Support query templates or categories (e.g., "Show me aggregation queries")
- Add tooltips explaining what each generated query does
- Generate multiple query suggestions and let user choose
- Integrate with insights API to generate queries targeting interesting data patterns

### Performance Considerations
- Query generation requires an LLM API call (~1-3 seconds)
- Button should show clear loading state to set user expectations
- Consider caching schema information to reduce database calls
- Rate limiting may be needed if users click rapidly

### Dependencies
- Requires OpenAI or Anthropic API key (already required by existing features)
- Uses existing LLM processor infrastructure
- No new external libraries needed
