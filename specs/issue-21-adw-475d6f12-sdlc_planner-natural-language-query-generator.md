# Feature: Natural Language Query Generator Button

## Feature Description
This feature adds a "Generate Query" button to the Natural Language SQL Interface that generates creative, interesting natural language queries based on existing database tables and their structure. When clicked, the button analyzes the current database schema (tables, columns, and data types), sends this information to an LLM provider (Gemini with highest priority, then OpenAI, then Anthropic), and receives a creative query suggestion limited to two sentences maximum. The generated query automatically populates and overwrites the query input field, allowing users to either execute it immediately or modify it before running. The button is styled as a secondary button (matching the "Upload Data" button) and positioned between the primary "Query" button and "Upload Data" button with justified spacing for clear visual hierarchy.

## User Story
As a user of the Natural Language SQL Interface
I want to click a button that generates interesting natural language query suggestions based on my uploaded data
So that I can discover valuable insights and analytical possibilities without having to think of queries myself

## Problem Statement
Users often struggle to formulate interesting queries when first encountering a new dataset, especially when unfamiliar with the data structure or analytical possibilities. Without guidance or query examples, users may:
- Ask only basic questions like "show me all data"
- Miss opportunities to discover valuable insights, patterns, and trends
- Feel overwhelmed by the blank query input field
- Not fully utilize the capabilities of the natural language SQL interface

The current interface provides no assistance in query formulation, requiring users to have domain expertise and creativity to ask meaningful questions about their data.

## Solution Statement
We will implement a "Generate Query" button that leverages LLM capabilities (via the existing `llm_processor.py` module) to automatically generate creative, insightful natural language queries. The solution works as follows:

1. **Schema Analysis**: Fetch the current database schema including table names, column names, column types, and row counts
2. **LLM Generation**: Send the schema to the LLM with a specialized prompt that instructs it to generate interesting queries focusing on insights, patterns, trends, or relationships (not generic queries)
3. **Query Population**: Automatically populate the query input field with the generated suggestion, overwriting any existing content
4. **User Control**: Allow users to immediately execute the query or edit it before running

The implementation follows existing codebase patterns for API communication, error handling, loading states, and UI/UX consistency. The LLM provider selection follows a priority system: Gemini (highest priority if API key exists) → OpenAI → Anthropic.

## Relevant Files
Use these files to implement the feature:

- **`app/server/core/llm_processor.py`** - Contains LLM integration functions for SQL generation and query suggestions
  - Will add `generate_query_suggestion_with_openai()` function to generate suggestions using OpenAI API
  - Will add `generate_query_suggestion_with_anthropic()` function to generate suggestions using Anthropic API
  - Will add `generate_query_suggestion_with_gemini()` function to generate suggestions using Gemini API
  - Will add `generate_query_suggestion()` routing function with priority: Gemini → OpenAI → Anthropic
  - Uses existing `format_schema_for_prompt()` function to format database schema

- **`app/server/core/data_models.py`** - Contains Pydantic models for API request/response validation
  - Will add `QuerySuggestionRequest` model with `llm_provider` field
  - Will add `QuerySuggestionResponse` model with `suggested_query`, `table_count`, and `error` fields

- **`app/server/server.py`** - FastAPI server with endpoint definitions
  - Will add `/api/suggest-query` POST endpoint (lines 243-282) that handles query suggestion requests
  - Uses existing `get_database_schema()` function from `core.sql_processor`
  - Implements error handling for empty databases and API failures

- **`app/client/index.html`** - HTML structure for the user interface
  - Will add "Generate Query" button with id `generate-query-button` in the query controls section (line 24)
  - Button positioned between "Query" and "Upload Data" buttons using flexbox with `justify-content: space-between`

- **`app/client/src/main.ts`** - TypeScript client-side logic
  - Will add `initializeQueryGenerator()` function (lines 53-80) to handle button clicks
  - Implements loading state during query generation
  - Populates query input field and sets focus after generation
  - Handles errors gracefully with user-friendly messages

- **`app/client/src/api/client.ts`** - API client for backend communication
  - Will add `generateQuerySuggestion()` method (lines 80-89) to call `/api/suggest-query` endpoint
  - Follows existing API client patterns for error handling and response typing

- **`app/client/src/types.d.ts`** - TypeScript type definitions
  - Will add `QuerySuggestionRequest` and `QuerySuggestionResponse` interface definitions
  - Ensures type safety across frontend code

- **`app/client/src/style.css`** - CSS styles for the interface
  - Uses existing `.secondary-button` class for the Generate Query button
  - Maintains consistent styling with "Upload Data" button
  - Uses existing `.query-controls` flexbox layout for button positioning

### New Files

- **`.claude/commands/e2e/test_query_generator.md`** - E2E test specification for the query generator feature
  - Validates the complete user flow from button click to query population
  - Tests error handling when no tables are uploaded
  - Verifies loading states and UI interactions
  - Captures screenshots at key steps for visual validation
  - Follows the format established by `test_basic_query.md`

- **`app/server/tests/core/test_query_generator.py`** - Unit tests for query generator functions
  - Tests OpenAI, Anthropic, and Gemini query suggestion generation
  - Tests LLM provider routing logic with different API key configurations
  - Tests error handling for missing API keys and API failures
  - Tests query length validation (2 sentences maximum)
  - Uses mocking to avoid actual API calls during testing

## Implementation Plan

### Phase 1: Foundation
Establish the backend foundation for query suggestion generation:

1. **Extend LLM Processor Module**
   - Add three new functions to `app/server/core/llm_processor.py`:
     - `generate_query_suggestion_with_openai()`: Generate suggestions using OpenAI GPT-4.1-mini
     - `generate_query_suggestion_with_anthropic()`: Generate suggestions using Anthropic Claude-3-haiku
     - `generate_query_suggestion_with_gemini()`: Generate suggestions using Google Gemini Flash
   - Each function accepts `schema_info` dictionary and returns a string query suggestion
   - Implement specialized prompts that emphasize creativity and insights over generic queries
   - Include query length constraint (2 sentences maximum) in prompts
   - Handle markdown cleanup (remove quotes, backticks) from LLM responses

2. **Add LLM Routing Logic**
   - Implement `generate_query_suggestion()` function with provider selection priority:
     1. Check if `GEMINI_API_KEY` exists → use Gemini
     2. Check if `OPENAI_API_KEY` exists → use OpenAI
     3. Check if `ANTHROPIC_API_KEY` exists → use Anthropic
     4. Fall back to `llm_provider` parameter if no keys available
   - Reuse existing `format_schema_for_prompt()` function for schema formatting

3. **Define Data Models**
   - Add `QuerySuggestionRequest` model to `app/server/core/data_models.py`:
     - `llm_provider`: Literal["openai", "anthropic", "gemini"] with default "openai"
   - Add `QuerySuggestionResponse` model:
     - `suggested_query`: str (the generated query)
     - `table_count`: int (number of tables analyzed)
     - `error`: Optional[str] (error message if generation fails)

4. **Create Backend Endpoint**
   - Add `/api/suggest-query` POST endpoint to `app/server/server.py`
   - Endpoint logic:
     1. Get database schema using existing `get_database_schema()`
     2. Validate that tables exist (return error if empty database)
     3. Call `generate_query_suggestion()` with schema and LLM provider
     4. Validate non-empty response
     5. Return `QuerySuggestionResponse` with success or error
   - Include comprehensive logging for success and failure cases

### Phase 2: Core Implementation
Build the frontend user interface and interaction logic:

1. **Add UI Button**
   - Update `app/client/index.html` to add "Generate Query" button
   - Button attributes:
     - `id="generate-query-button"`
     - `class="secondary-button"`
     - Text: "Generate Query"
   - Position in `.query-controls` div between "Query" and "Upload Data" buttons
   - Use existing flexbox layout with `justify-content: space-between` for spacing

2. **Implement Frontend API Client**
   - Add `generateQuerySuggestion()` method to `app/client/src/api/client.ts`
   - Method signature: `async generateQuerySuggestion(request: QuerySuggestionRequest): Promise<QuerySuggestionResponse>`
   - HTTP: POST to `/api/suggest-query` with JSON body
   - Handle network errors and non-200 responses
   - Parse and return typed response

3. **Add TypeScript Types**
   - Define `QuerySuggestionRequest` interface in `app/client/src/types.d.ts`:
     ```typescript
     interface QuerySuggestionRequest {
       llm_provider: 'openai' | 'anthropic' | 'gemini';
     }
     ```
   - Define `QuerySuggestionResponse` interface:
     ```typescript
     interface QuerySuggestionResponse {
       suggested_query: string;
       table_count: number;
       error?: string;
     }
     ```

4. **Implement Button Click Handler**
   - Add `initializeQueryGenerator()` function to `app/client/src/main.ts`
   - Event handler logic:
     1. Disable button and show loading spinner
     2. Call `api.generateQuerySuggestion({ llm_provider: 'openai' })`
     3. If response has error, display error message
     4. If successful, populate `query-input` textarea with `suggested_query`
     5. Set focus to query input field
     6. Re-enable button and restore original text
   - Use try-catch for error handling
   - Store original button text before showing loading state

5. **Initialize on Page Load**
   - Call `initializeQueryGenerator()` in the `DOMContentLoaded` event listener in `main.ts`
   - Ensure initialization happens after DOM elements are available

### Phase 3: Integration
Integrate the feature with existing functionality and add comprehensive testing:

1. **Error Handling Integration**
   - **No tables scenario**: Backend returns error "Please upload data first before generating queries"
   - **API key missing**: LLM functions raise `ValueError` with appropriate message
   - **API failure**: Catch exceptions and return error in `QuerySuggestionResponse`
   - **Frontend error display**: Use existing `displayError()` function to show user-friendly messages
   - **Empty query response**: Backend validates non-empty suggestions and returns error if blank

2. **Loading State Integration**
   - Button disabled during query generation (prevent duplicate requests)
   - Button text replaced with loading spinner: `<span class="loading"></span>`
   - Original button text restored after completion/failure
   - Uses existing `.loading` CSS class from `style.css`

3. **UI/UX Integration**
   - Button styled with existing `.secondary-button` class (matches Upload Data button)
   - Query input field receives focus after query population (guides user to next action)
   - Query overwrites existing input content (consistent with feature requirements)
   - Button positioned with `justify-content: space-between` (clear visual separation)

4. **Unit Testing**
   - Create `app/server/tests/core/test_query_generator.py` with pytest tests:
     - `test_generate_query_suggestion_with_openai()`: Mock OpenAI API, verify non-empty suggestion
     - `test_generate_query_suggestion_with_anthropic()`: Mock Anthropic API, verify non-empty suggestion
     - `test_generate_query_suggestion_with_gemini()`: Mock Gemini API, verify non-empty suggestion
     - `test_generate_query_suggestion_routing()`: Test LLM provider priority logic
     - `test_generate_query_suggestion_no_api_key()`: Verify error when no API keys configured
     - `test_generate_query_suggestion_api_failure()`: Test error handling for API failures
     - `test_query_length_constraint()`: Verify queries are approximately 2 sentences
   - Use `unittest.mock` for API mocking to avoid actual API calls

5. **End-to-End Testing**
   - Create `.claude/commands/e2e/test_query_generator.md` following the E2E test format
   - Test steps:
     1. Navigate to application and verify initial state
     2. Upload sample data (users.json)
     3. Verify "Generate Query" button is visible and enabled
     4. Click "Generate Query" button
     5. Verify loading state appears (button disabled, spinner visible)
     6. Wait for query to populate in input field
     7. Verify query is non-empty and different from placeholder text
     8. Verify query is 2 sentences or less
     9. Verify input field has focus
     10. Test error handling: reset database, click button, verify error message
   - Capture screenshots: initial state, loading state, populated query, error state
   - Follow format from `.claude/commands/e2e/test_basic_query.md`

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Backend Implementation - LLM Functions
- Read `app/server/core/llm_processor.py` to understand existing LLM integration patterns
- Add `generate_query_suggestion_with_openai()` function:
  - Accept `schema_info: Dict[str, Any]` parameter
  - Create specialized prompt emphasizing creative, insightful queries (not generic)
  - Include "Maximum 2 sentences" constraint in prompt
  - Call OpenAI API with `gpt-4.1-mini` model, temperature 0.7, max_tokens 100
  - Clean up markdown and quotes from response
  - Return query string
- Add `generate_query_suggestion_with_anthropic()` function:
  - Same logic as OpenAI but using Anthropic client and `claude-3-haiku-20240307` model
- Add `generate_query_suggestion_with_gemini()` function:
  - Same logic but using Gemini client and `gemini-flash-latest` model
- Add `generate_query_suggestion()` routing function:
  - Check API keys in priority order: Gemini → OpenAI → Anthropic
  - Call appropriate provider function based on availability
  - Fall back to `llm_provider` parameter if no keys available

### 2. Backend Implementation - Data Models
- Read `app/server/core/data_models.py` to understand existing model patterns
- Add `QuerySuggestionRequest` Pydantic model:
  - `llm_provider: Literal["openai", "anthropic", "gemini"] = "openai"`
- Add `QuerySuggestionResponse` Pydantic model:
  - `suggested_query: str`
  - `table_count: int`
  - `error: Optional[str] = None`

### 3. Backend Implementation - API Endpoint
- Read `app/server/server.py` to understand existing endpoint patterns
- Import new models: `QuerySuggestionRequest`, `QuerySuggestionResponse`
- Import `generate_query_suggestion` from `core.llm_processor`
- Add `/api/suggest-query` POST endpoint after the `/api/insights` endpoint:
  - Accept `QuerySuggestionRequest` as request body
  - Get database schema using `get_database_schema()`
  - Check if `schema_info.get('tables')` is empty, return error if no tables
  - Call `generate_query_suggestion(schema_info, request.llm_provider)`
  - Validate non-empty response
  - Return `QuerySuggestionResponse` with suggestion or error
  - Include logging for success/failure

### 4. Frontend Implementation - TypeScript Types
- Read `app/client/src/types.d.ts` to understand existing type patterns
- Add `QuerySuggestionRequest` interface with `llm_provider` field
- Add `QuerySuggestionResponse` interface with `suggested_query`, `table_count`, and optional `error` fields

### 5. Frontend Implementation - API Client
- Read `app/client/src/api/client.ts` to understand existing API methods
- Add `generateQuerySuggestion()` method to the `api` object:
  - Accept `QuerySuggestionRequest` parameter
  - POST to `/api/suggest-query` with JSON body
  - Parse response as `QuerySuggestionResponse`
  - Handle errors and throw with descriptive messages

### 6. Frontend Implementation - HTML Button
- Read `app/client/index.html` to understand the structure
- Add "Generate Query" button in the `.query-controls` div:
  - `id="generate-query-button"`
  - `class="secondary-button"`
  - Text: "Generate Query"
  - Position between "Query" and "Upload Data" buttons

### 7. Frontend Implementation - Button Handler
- Read `app/client/src/main.ts` to understand existing initialization patterns
- Add `initializeQueryGenerator()` function:
  - Get references to `query-input` and `generate-query-button` elements
  - Add click event listener to button
  - In event handler:
    - Disable button
    - Save original button text
    - Show loading spinner: `button.innerHTML = '<span class="loading"></span>'`
    - Call `api.generateQuerySuggestion({ llm_provider: 'openai' })`
    - If response has error, call `displayError(response.error)`
    - If successful, set `queryInput.value = response.suggested_query` and `queryInput.focus()`
    - Re-enable button and restore original text
    - Wrap in try-catch for error handling
- Call `initializeQueryGenerator()` in the `DOMContentLoaded` event listener

### 8. Unit Testing - Create Test File
- Read `app/server/tests/core/test_llm_processor.py` to understand existing test patterns
- Create `app/server/tests/core/test_query_generator.py` with pytest tests:
  - `test_generate_query_suggestion_with_openai()`: Mock OpenAI, verify non-empty response
  - `test_generate_query_suggestion_with_anthropic()`: Mock Anthropic, verify non-empty response
  - `test_generate_query_suggestion_with_gemini()`: Mock Gemini, verify non-empty response
  - `test_query_suggestion_routing_gemini_priority()`: Mock all APIs, verify Gemini is called when all keys present
  - `test_query_suggestion_routing_openai_fallback()`: Verify OpenAI is called when Gemini key missing
  - `test_query_suggestion_routing_anthropic_fallback()`: Verify Anthropic is called when Gemini and OpenAI keys missing
  - `test_query_suggestion_no_api_key()`: Verify error when no API keys configured
  - `test_query_suggestion_markdown_cleanup()`: Verify quotes and backticks are removed
- Use `unittest.mock.patch` to mock API clients
- Use sample schema data for testing

### 9. Unit Testing - Run Tests
- Run the new unit tests: `cd app/server && uv run pytest tests/core/test_query_generator.py -v`
- Verify all tests pass
- Fix any failures before proceeding

### 10. E2E Testing - Create Test File
- Read `.claude/commands/test_e2e.md` to understand the E2E test framework
- Read `.claude/commands/e2e/test_basic_query.md` to see an example E2E test
- Create `.claude/commands/e2e/test_query_generator.md` with the following structure:
  - **User Story**: As a user, I want to generate query suggestions, so that I can discover insights
  - **Test Steps**:
    1. Navigate to application URL
    2. Take screenshot of initial state
    3. Verify "Generate Query" button is visible
    4. Upload sample data (users.json) to populate database
    5. Take screenshot after data upload
    6. Click "Generate Query" button
    7. Verify button shows loading state (disabled, spinner visible)
    8. Wait for query to populate in input field (max 10 seconds)
    9. Take screenshot of populated query
    10. Verify query is non-empty
    11. Verify query is different from placeholder text
    12. Verify query length is 2 sentences or less
    13. Verify input field has focus
    14. Clear database (reset)
    15. Click "Generate Query" button again
    16. Verify error message appears about no tables
    17. Take screenshot of error state
  - **Success Criteria**:
    - Button is visible and clickable
    - Loading state appears during generation
    - Query is populated automatically
    - Query is creative and non-empty
    - Query is 2 sentences maximum
    - Error handling works when no tables exist
    - Input field receives focus after population
    - 4 screenshots are captured

### 11. Integration Testing - Manual Validation
- Start the backend server: `cd app/server && uv run python server.py`
- Start the frontend dev server: `cd app/client && bun run dev`
- Open browser to `http://localhost:5173`
- Upload sample data (users.json)
- Click "Generate Query" button
- Verify:
  - Loading state appears
  - Query populates in input field
  - Query is creative and interesting
  - Input field has focus
  - Query is 2 sentences or less
- Clear database (remove tables)
- Click "Generate Query" button again
- Verify error message appears
- Test with different LLM providers if multiple API keys are configured

### 12. Run All Validation Commands
- Execute every validation command listed in the "Validation Commands" section below
- Ensure all tests pass with zero regressions
- Fix any failures before considering the feature complete

## Testing Strategy

### Unit Tests
- **Test query suggestion generation with OpenAI**: Mock OpenAI API, verify `generate_query_suggestion_with_openai()` returns a non-empty string when given valid schema
- **Test query suggestion generation with Anthropic**: Mock Anthropic API, verify `generate_query_suggestion_with_anthropic()` returns a non-empty string
- **Test query suggestion generation with Gemini**: Mock Gemini API, verify `generate_query_suggestion_with_gemini()` returns a non-empty string
- **Test LLM provider routing with all keys**: Mock all three APIs, verify Gemini is called (highest priority)
- **Test LLM provider routing without Gemini key**: Mock OpenAI and Anthropic, verify OpenAI is called
- **Test LLM provider routing without Gemini and OpenAI keys**: Mock Anthropic only, verify Anthropic is called
- **Test error handling for missing API keys**: Verify `ValueError` is raised with appropriate message
- **Test error handling for API failures**: Mock API to raise exception, verify error is caught and returned
- **Test markdown cleanup**: Verify quotes, backticks, and code fences are removed from responses
- **Test query length**: Use real prompts with mocked responses to verify 2-sentence constraint is communicated

### Edge Cases
- **No tables in database**: Endpoint should return `QuerySuggestionResponse` with error "Please upload data first before generating queries"
- **Empty schema (tables exist but no columns)**: Should handle gracefully and generate appropriate error
- **Single table with one column**: Should generate creative queries within constraints
- **Multiple tables with complex relationships**: Should generate queries showcasing cross-table insights
- **API key not configured**: Should return error indicating which API key is needed
- **Network timeout**: Should handle gracefully with user-friendly error message
- **API rate limiting**: Should catch API errors and display meaningful message to user
- **Rapid button clicks**: Button disabled during processing prevents duplicate requests
- **Very long query returned by LLM**: Backend should return it, but prompt constrains to 2 sentences
- **Empty string returned by LLM**: Backend validates and returns error "Failed to generate query suggestion"
- **Markdown in LLM response**: Should be cleaned (remove backticks, quotes, code fences)

## Acceptance Criteria
- [ ] "Generate Query" button is visible in the UI with id `generate-query-button`
- [ ] Button is styled as `.secondary-button` matching the "Upload Data" button
- [ ] Button is positioned between "Query" and "Upload Data" buttons with justified spacing
- [ ] Clicking button sends request to `/api/suggest-query` endpoint
- [ ] Backend fetches database schema using `get_database_schema()`
- [ ] Backend calls appropriate LLM provider based on API key priority: Gemini → OpenAI → Anthropic
- [ ] LLM receives specialized prompt emphasizing creative, insightful queries
- [ ] LLM prompt includes "Maximum 2 sentences" constraint
- [ ] Generated query is cleaned of markdown (backticks, quotes, code fences)
- [ ] Generated query populates query input field, overwriting existing content
- [ ] Query input field receives focus after query is populated
- [ ] Button shows loading state during generation (disabled, spinner visible)
- [ ] Button is re-enabled after query generation completes or fails
- [ ] Error handling works when no tables are uploaded (user-friendly message)
- [ ] Error handling works when API key is not configured (indicates which key needed)
- [ ] Error handling works when LLM API call fails (network error, timeout, etc.)
- [ ] Error handling works when LLM returns empty response
- [ ] Generated queries are creative and interesting (not generic like "show me all data")
- [ ] Generated queries focus on insights, patterns, trends, or relationships
- [ ] Unit tests pass for all query generator functions with 100% coverage
- [ ] E2E test validates complete user flow with screenshots
- [ ] All existing backend tests continue to pass (zero regressions)
- [ ] All existing frontend type checks pass (zero regressions)
- [ ] Frontend build completes successfully (zero regressions)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md` to understand how to run E2E tests
- Read and execute the new E2E test file `.claude/commands/e2e/test_query_generator.md` to validate this functionality works end-to-end
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run query generator unit tests
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### LLM Provider Priority
The implementation uses a priority system for LLM provider selection:
1. **Gemini** (highest priority) - If `GEMINI_API_KEY` environment variable exists
2. **OpenAI** (second priority) - If `OPENAI_API_KEY` environment variable exists
3. **Anthropic** (lowest priority) - If `ANTHROPIC_API_KEY` environment variable exists
4. **Fallback** - Uses `llm_provider` parameter from request if no keys are configured

This ensures the application automatically uses the best available LLM without requiring users to manually select providers.

### Query Quality Guidelines
The LLM prompts are designed to generate high-quality queries that:
- **Showcase insights**: Focus on patterns, trends, aggregations, and relationships
- **Avoid generic queries**: Specifically instructed to avoid "show me all data" or "list all records"
- **Stay concise**: Limited to 2 sentences maximum for readability
- **Be creative**: Temperature set to 0.7 to allow for variety and creativity
- **Be executable**: Generate valid natural language that can be converted to SQL

Example good queries:
- "What are the top 5 most expensive products by category?"
- "Show me users who signed up last month and made more than 3 purchases."
- "Compare average order values between different customer segments."

Example bad queries (that prompts are designed to avoid):
- "Show me all data"
- "List all records"
- "Select everything from the table"

### Button Styling and Positioning
The "Generate Query" button uses:
- **CSS class**: `.secondary-button` for consistent styling with "Upload Data" button
- **Position**: Between "Query" (primary button) and "Upload Data" (secondary button)
- **Layout**: Uses existing `.query-controls` flexbox with `justify-content: space-between`
- **Visual hierarchy**: Clear separation from primary action ("Query") to avoid confusion

### Error Handling Strategy
Comprehensive error handling covers multiple failure scenarios:

1. **No tables uploaded**: Backend checks if `schema_info['tables']` is empty and returns friendly error
2. **API key missing**: LLM functions raise `ValueError` with message indicating which key is needed
3. **API call failure**: Exceptions caught and returned in `QuerySuggestionResponse.error` field
4. **Empty LLM response**: Backend validates non-empty response and returns error if blank
5. **Frontend display**: All errors shown using existing `displayError()` function for consistency

### Testing Approach
The testing strategy uses three layers:

1. **Unit Tests** (`test_query_generator.py`):
   - Test individual LLM provider functions in isolation
   - Test routing logic with different API key configurations
   - Test error handling for various failure scenarios
   - Use mocking to avoid actual API calls (fast, deterministic)

2. **E2E Tests** (`.claude/commands/e2e/test_query_generator.md`):
   - Test complete user flow in real browser
   - Validate UI interactions and visual states
   - Capture screenshots for manual review
   - Test error handling with actual UI feedback

3. **Integration Tests** (manual validation):
   - Test with real LLM APIs to verify prompt quality
   - Validate generated queries are actually interesting and creative
   - Test with different database schemas and table structures

### Future Enhancements
Potential improvements for future iterations:

- **Multiple suggestions**: Generate 3-5 query options for users to choose from
- **Query categories**: Organize suggestions by type (aggregations, filters, joins, time-series)
- **Difficulty levels**: Offer simple, intermediate, and advanced query suggestions
- **Query history**: Remember previously generated queries for quick access
- **Favorites**: Allow users to save useful query patterns
- **Personalization**: Learn from user's query patterns to tailor suggestions
- **Query templates**: Pre-defined templates for common analytical patterns
- **Natural language explanations**: Include brief explanations of what each query reveals

### Security Considerations
- **SQL injection**: Generated natural language queries go through existing SQL generation pipeline which includes SQL injection protection
- **API key security**: API keys stored in environment variables, never exposed to frontend
- **Rate limiting**: Consider implementing rate limiting on `/api/suggest-query` endpoint to prevent abuse
- **Input validation**: Database schema validated before sending to LLM to prevent prompt injection

### Performance Considerations
- **Caching**: Consider caching query suggestions for identical schemas to reduce API costs
- **Timeouts**: LLM API calls should have reasonable timeouts (5-10 seconds) to prevent long waits
- **Button state**: Button disabled during generation prevents duplicate requests and API costs
- **Schema size**: Large schemas (100+ tables) may need truncation before sending to LLM

### Accessibility
- **Keyboard navigation**: Button is keyboard accessible (tab navigation, enter to activate)
- **Screen readers**: Button has descriptive text "Generate Query" for screen reader users
- **Loading state**: Loading spinner provides visual feedback during wait time
- **Focus management**: Input field receives focus after query population, guiding next action

### Browser Compatibility
The feature uses standard web APIs and should work across all modern browsers:
- Chrome/Edge (Chromium-based)
- Firefox
- Safari
- No Internet Explorer support needed (application uses modern JavaScript/TypeScript)
