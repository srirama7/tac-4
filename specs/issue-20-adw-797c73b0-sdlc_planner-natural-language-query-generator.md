# Feature: Natural Language Query Generator Button

## Feature Description
A new button that automatically generates interesting natural language queries based on the existing database tables and their structures. When clicked, it uses the LLM to create creative, contextually relevant queries that demonstrate the capabilities of the data, then automatically populates the query input field with the generated text (overwriting any existing content). This feature helps users discover query possibilities and get started with their data exploration without needing to think of queries themselves.

The button will be styled similarly to the "Upload Data" button and positioned with space-between justification alongside the existing primary buttons, creating a clean, balanced button layout.

## User Story
As a user
I want to automatically generate interesting natural language queries based on my database structure
So that I can quickly explore my data without having to think of queries myself and see what kinds of questions I can ask

## Problem Statement
Users who upload data to the Natural Language SQL Interface may not immediately know what questions to ask or how to phrase their queries. This creates a barrier to entry and prevents users from quickly experiencing the value of the application. Without example queries tailored to their specific dataset, users must either:
1. Spend time understanding their data structure before asking questions
2. Come up with generic queries that may not showcase interesting aspects of their data
3. Struggle with query formulation, especially if they're new to data exploration

This leads to a slower onboarding experience and reduces the likelihood that users will discover the full capabilities of their uploaded datasets.

## Solution Statement
Implement a "Generate Query" button that leverages the existing `llm_processor.py` module to create contextually relevant, interesting natural language queries based on the current database schema and table structures. The button will:

1. Analyze all available tables and their columns using the existing schema endpoint
2. Send a carefully crafted prompt to the LLM (using the same routing logic as query processing) requesting creative, interesting queries limited to two sentences maximum
3. Receive a natural language query suggestion from the LLM
4. Automatically populate the query input field, overwriting any existing content
5. Allow users to immediately execute the generated query or edit it as needed

The button will be visually distinct with the same styling as "Upload Data" button (secondary-button class), and positioned using `justify-content: space-between` to create proper spacing between the primary "Query" button and the secondary buttons.

This solution reuses existing infrastructure (LLM routing, schema retrieval, input field handling) while providing a low-friction way for users to start exploring their data.

## Relevant Files
Use these files to implement the feature:

- **app/server/core/llm_processor.py** - Contains the LLM integration logic for OpenAI and Anthropic. We'll add a new function `generate_query_suggestion()` that creates interesting queries based on schema information. This module already handles LLM routing and prompt formatting.

- **app/server/core/data_models.py** - Contains Pydantic models for API requests/responses. We'll add new models `QuerySuggestionRequest` and `QuerySuggestionResponse` to handle the query generation endpoint.

- **app/server/server.py** - The FastAPI backend server. We'll add a new endpoint `POST /api/suggest-query` that accepts the current database schema and returns a generated query suggestion.

- **app/server/core/sql_processor.py** - Contains `get_database_schema()` function which we'll use to retrieve current table structures for context when generating queries.

- **app/client/index.html** - The main HTML structure. We'll add the new "Generate Query" button to the `.query-controls` section and update the flex layout to use `justify-content: space-between`.

- **app/client/src/main.ts** - The main TypeScript file handling UI interactions. We'll add:
  - Event handler for the new "Generate Query" button
  - Function to call the new API endpoint
  - Logic to populate the query input field with the generated query

- **app/client/src/api/client.ts** - API client module. We'll add a new method `generateQuerySuggestion()` to call the backend endpoint.

- **app/client/src/types.d.ts** - TypeScript type definitions. We'll add interfaces for `QuerySuggestionRequest` and `QuerySuggestionResponse`.

- **app/client/src/style.css** - Styling for the UI. We'll update `.query-controls` to use `justify-content: space-between` for proper button spacing.

### New Files

- **app/server/tests/core/test_query_generator.py** - New test file for the query generation functionality, testing various scenarios including empty databases, single tables, multiple tables, and error handling.

- **.claude/commands/e2e/test_query_generator.md** - E2E test specification for validating the query generator button works correctly in the UI, including button presence, click interaction, input field population, and query execution.

## Implementation Plan

### Phase 1: Foundation
Establish the backend infrastructure for query generation by creating the LLM prompt logic and API models. This phase focuses on the server-side components that will analyze database schemas and generate contextually relevant queries using the existing LLM integration.

Key activities:
- Define data models for query suggestion requests and responses
- Create LLM prompt engineering logic that generates interesting queries based on schema
- Set up proper error handling for cases where no tables exist or LLM calls fail

### Phase 2: Core Implementation
Build the complete end-to-end functionality including the FastAPI endpoint, frontend button, and API client integration. This phase brings together backend and frontend to create a working feature.

Key activities:
- Implement FastAPI endpoint that retrieves schema and calls LLM
- Add frontend button with proper styling and positioning
- Wire up event handlers and API calls to connect UI to backend
- Implement input field population logic that overwrites existing content

### Phase 3: Integration
Ensure the new feature integrates seamlessly with existing functionality and is properly tested. This phase focuses on quality assurance, edge case handling, and documentation.

Key activities:
- Create unit tests for backend query generation logic
- Create E2E tests to validate the complete user workflow
- Handle edge cases (no tables, API errors, loading states)
- Ensure button styling matches design requirements
- Validate that generated queries can be successfully executed

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create Backend Data Models
- Open `app/server/core/data_models.py`
- Add `QuerySuggestionRequest` model with optional `llm_provider` field (defaults to "openai")
- Add `QuerySuggestionResponse` model with fields: `suggested_query` (str), `table_count` (int), `error` (Optional[str])
- These models will handle the API request/response for query generation

### 2. Implement LLM Query Generation Logic
- Open `app/server/core/llm_processor.py`
- Create new function `generate_query_suggestion(schema_info: Dict[str, Any], llm_provider: str = "openai") -> str`
- The function should:
  - Format the schema information into a readable prompt
  - Create a prompt asking the LLM to generate ONE interesting natural language query (max 2 sentences) based on the available tables
  - Use the existing `generate_sql_with_openai()` or `generate_sql_with_anthropic()` pattern but with a different prompt
  - Return the generated natural language query text
  - Handle errors gracefully
- The prompt should encourage creative, interesting queries that showcase the data

### 3. Create Query Generation API Endpoint
- Open `app/server/server.py`
- Add new endpoint `POST /api/suggest-query` with response model `QuerySuggestionResponse`
- The endpoint should:
  - Get the current database schema using `get_database_schema()`
  - Check if there are any tables available (return error if none)
  - Call `generate_query_suggestion()` with the schema
  - Return the suggested query with metadata
  - Handle all errors and return appropriate error messages

### 4. Write Backend Unit Tests
- Create new file `app/server/tests/core/test_query_generator.py`
- Add test for `generate_query_suggestion()` function with valid schema
- Add test for handling empty/no tables scenario
- Add test for LLM provider routing (OpenAI vs Anthropic)
- Add test for error handling when LLM API fails
- Run tests to verify backend logic works correctly: `cd app/server && uv run pytest tests/core/test_query_generator.py -v`

### 5. Add TypeScript Type Definitions
- Open `app/client/src/types.d.ts`
- Add `QuerySuggestionRequest` interface matching the backend model
- Add `QuerySuggestionResponse` interface matching the backend model
- Ensure types are properly exported for use in API client

### 6. Extend API Client
- Open `app/client/src/api/client.ts`
- Add new method `generateQuerySuggestion()` to the `api` object
- The method should:
  - Accept optional request parameters (llm_provider)
  - Call `POST /api/suggest-query`
  - Return typed `QuerySuggestionResponse`
  - Handle errors appropriately

### 7. Update HTML Structure
- Open `app/client/index.html`
- Find the `.query-controls` div (contains Query and Upload Data buttons)
- Add new button with id `generate-query-button` and class `secondary-button`
- Button text: "Generate Query"
- Position it between the Query button and Upload Data button in the HTML

### 8. Update CSS Styling
- Open `app/client/src/style.css`
- Update `.query-controls` to use `justify-content: space-between` instead of `gap: 1rem`
- Ensure proper spacing and alignment for three buttons
- Verify the secondary-button styling already exists and looks good

### 9. Implement Frontend Button Logic
- Open `app/client/src/main.ts`
- Create new function `initializeQueryGenerator()`
- The function should:
  - Get reference to `generate-query-button` element
  - Add click event listener
  - On click: disable button, show loading state
  - Call `api.generateQuerySuggestion()`
  - If successful: populate `query-input` textarea with suggested query (overwrite existing content)
  - If error: call `displayError()` with error message
  - Re-enable button and restore text after completion
- Call `initializeQueryGenerator()` from the DOMContentLoaded event listener

### 10. Handle Loading States
- In the button click handler, update button to show loading spinner while waiting for API response
- Use the same loading pattern as the Query button: `button.innerHTML = '<span class="loading"></span>'`
- Restore button text after API call completes (success or failure)
- Ensure button is disabled during API call to prevent duplicate requests

### 11. Create E2E Test Specification
- Create new file `.claude/commands/e2e/test_query_generator.md`
- Follow the pattern from `test_basic_query.md` and `test_complex_query.md`
- Include User Story describing what we're testing
- Define Test Steps:
  1. Navigate to application
  2. Take screenshot of initial state
  3. Verify Generate Query button is present
  4. Click Generate Query button
  5. Wait for query input to be populated
  6. Take screenshot of populated query
  7. Verify query input field contains text
  8. Verify query is no longer than 2 sentences
  9. Click Query button to execute the generated query
  10. Verify results appear successfully
  11. Take screenshot of results
- Include Success Criteria: button works, query is generated, query can be executed, screenshots captured

### 12. Test the Feature Manually
- Start the backend server: `cd app/server && uv run python server.py`
- Start the frontend dev server: `cd app/client && bun run dev`
- Navigate to http://localhost:5173
- Upload sample data (users, products, or events)
- Click "Generate Query" button multiple times
- Verify each time:
  - Button shows loading state
  - Query input field is populated with a new query
  - Existing content is overwritten
  - Generated query is relevant to the uploaded tables
  - Query can be executed successfully
- Test with no tables uploaded (should show error)
- Test error handling with invalid scenarios

### 13. Run All Validation Commands
Execute the validation commands specified in the "Validation Commands" section below to ensure:
- All backend tests pass with zero failures
- Frontend builds without errors
- TypeScript compilation succeeds
- E2E test validates the complete feature workflow
- No regressions in existing functionality

## Testing Strategy

### Unit Tests
1. **Backend LLM Query Generation Tests** (`test_query_generator.py`):
   - Test `generate_query_suggestion()` with valid schema containing multiple tables
   - Test with single table schema
   - Test with empty schema (no tables)
   - Test LLM provider routing (OpenAI vs Anthropic)
   - Test error handling when API keys are missing
   - Test error handling when LLM API call fails
   - Verify generated queries are non-empty strings
   - Verify queries are limited to reasonable length

2. **API Endpoint Tests**:
   - Test `POST /api/suggest-query` returns valid response structure
   - Test endpoint with no tables in database returns appropriate error
   - Test endpoint handles LLM failures gracefully
   - Verify response includes suggested_query and table_count

3. **Frontend Unit Tests** (manual testing):
   - Verify button click triggers API call
   - Verify loading state is shown during API call
   - Verify input field is populated with response
   - Verify existing input content is overwritten
   - Verify error messages are displayed on failure

### Edge Cases
1. **No Tables Scenario**: When database has no tables uploaded yet, button should show error message "Please upload data first before generating queries"

2. **API Failure**: When LLM API fails (network error, timeout, invalid API key), display user-friendly error message without exposing technical details

3. **Empty Response**: If LLM returns empty string, show error "Failed to generate query suggestion. Please try again."

4. **Very Long Queries**: If LLM generates query longer than 2 sentences despite prompt instructions, truncate or show full query anyway (system should handle gracefully)

5. **Rapid Clicking**: Button should be disabled during API call to prevent duplicate requests

6. **Schema Changes**: When user uploads new tables or removes tables, subsequent query generation should reflect the updated schema

7. **Special Characters**: Generated queries may contain quotes, special characters - ensure these are properly handled in the input field

8. **Concurrent Operations**: User can still manually type in query field, upload data, or perform other actions while query generation is happening

## Acceptance Criteria
1. ✅ A "Generate Query" button appears in the query controls section between "Query" and "Upload Data" buttons
2. ✅ Button styling matches the "Upload Data" button (uses secondary-button class)
3. ✅ Buttons are spaced with justify-content: space-between for clean visual separation
4. ✅ Clicking the button shows a loading state (spinner) while waiting for response
5. ✅ Generated query automatically populates the query input field, overwriting any existing content
6. ✅ Generated queries are contextually relevant to the uploaded table structures
7. ✅ Generated queries are limited to a maximum of two sentences
8. ✅ Feature works with both OpenAI and Anthropic LLM providers
9. ✅ Appropriate error message displays when no tables are available
10. ✅ Appropriate error message displays when LLM API fails
11. ✅ Button is disabled during API call to prevent duplicate requests
12. ✅ Generated queries can be successfully executed by clicking the Query button
13. ✅ All existing functionality continues to work (no regressions)
14. ✅ Backend unit tests pass for query generation logic
15. ✅ E2E test validates the complete user workflow

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_query_generator.md` to validate the query generator functionality works end-to-end
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run new query generator tests to validate backend logic
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript compilation to validate frontend code has no type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature builds correctly with zero errors

## Notes

### Implementation Details
- The feature leverages the existing `llm_processor.py` module and LLM routing logic, ensuring consistency with how the application already handles AI queries
- Generated queries are "interesting" and "creative" - the prompt encourages the LLM to suggest queries that showcase different aspects of the data, not just basic "SELECT * FROM table" queries
- The two-sentence limit keeps queries concise and focused, improving readability and reducing the chance of overly complex suggestions

### Design Decisions
- **Button Placement**: Positioned between Query and Upload Data buttons using `justify-content: space-between` provides clear visual hierarchy - primary action (Query) on left, secondary actions (Generate/Upload) on right with proper spacing
- **Overwrite Behavior**: Always overwrites existing content rather than appending to ensure clean, predictable behavior
- **Secondary Button Style**: Matches Upload Data button styling to indicate this is a secondary/supporting action, not the primary workflow

### Future Enhancements
Consider these enhancements for future iterations:
1. **Query History**: Store generated queries so users can browse previous suggestions
2. **Multiple Suggestions**: Generate 3-5 query options and let user choose
3. **Query Categories**: Allow users to request specific types of queries (aggregations, joins, filters, etc.)
4. **Smart Context**: Remember which queries user has already run to avoid duplicate suggestions
5. **Sample Results Preview**: Show a preview of what the query would return before execution
6. **Difficulty Levels**: Offer simple, intermediate, and advanced query suggestions

### Technical Considerations
- The feature requires at least one of OPENAI_API_KEY or ANTHROPIC_API_KEY to be configured in the environment
- LLM responses are non-deterministic, so generated queries will vary between calls even with the same schema
- Rate limiting: Consider adding rate limiting if users excessively click the button (not implemented in v1)
- Cost: Each button click makes an LLM API call, which incurs cost. Monitor usage if deployed to production
