# Feature: Natural Language Query Generator Button

## Feature Description
Add a new button to the Natural Language SQL Interface that generates contextually relevant natural language queries based on the existing database schema and table structures. The button will use the LLM processor to create interesting, realistic queries that showcase the data relationships and analytical possibilities. Generated queries will be limited to two sentences maximum and will automatically populate (overwrite) the query input field for users to execute manually.

This feature enhances user experience by:
- Providing query inspiration for users unfamiliar with their data
- Demonstrating the types of questions they can ask
- Reducing friction in getting started with the interface
- Showcasing the analytical capabilities of the application

## User Story
As a user of the Natural Language SQL Interface
I want to generate example natural language queries based on my uploaded tables
So that I can quickly explore my data without having to think of queries myself

## Problem Statement
Users often face the "blank page problem" when interacting with the Natural Language SQL Interface. Even though they have uploaded data, they may not know what questions to ask or how to phrase their queries. This creates friction in the user experience and prevents users from discovering the full analytical potential of their data. Users need inspiration and examples to get started, especially when exploring new datasets.

## Solution Statement
Implement a "Generate Query" button that leverages the existing LLM processor infrastructure to create contextually relevant natural language queries based on the current database schema. The button will:

1. Analyze the available tables, columns, and data types in the database
2. Use OpenAI or Anthropic APIs (with the same routing logic as the main query processor) to generate interesting queries
3. Automatically populate the query input field with the generated query
4. Provide immediate visual feedback through loading states
5. Handle edge cases (no tables, API errors) gracefully

The solution follows existing application patterns and reuses the LLM processor architecture for consistency.

## Relevant Files
Use these files to implement the feature:

### Backend Files

- **app/server/core/llm_processor.py** - Contains LLM integration logic
  - Already has functions for OpenAI and Anthropic SQL generation
  - Need to add new functions: `generate_natural_language_query_with_openai()`, `generate_natural_language_query_with_anthropic()`, and `generate_natural_language_query()`
  - Reuse existing `format_schema_for_prompt()` helper
  - Follow the same API key routing logic as `generate_sql()`

- **app/server/server.py** - Main FastAPI server
  - Need to add new endpoint: `POST /api/generate-query`
  - Import and use the new `generate_natural_language_query()` function
  - Follow existing error handling and logging patterns
  - Use the existing `get_database_schema()` function

- **app/server/core/data_models.py** - Pydantic data models
  - Need to add `QueryGenerationRequest` model (empty, uses schema)
  - Need to add `QueryGenerationResponse` model with `query` and optional `error` fields
  - Follow existing model naming conventions and structure

- **app/server/core/sql_processor.py** - SQL processing utilities
  - Reference `get_database_schema()` function (already exists)
  - Used to provide schema information to LLM

### Frontend Files

- **app/client/src/main.ts** - Main TypeScript application logic
  - Need to add `initializeGenerateQueryButton()` function
  - Wire up click handler to call API and update input field
  - Implement loading state management (disable button, show spinner)
  - Handle errors with `displayError()` function
  - Follow existing patterns from `initializeQueryInput()` and `initializeFileUpload()`

- **app/client/src/api/client.ts** - API client
  - Need to add `generateQuery()` method to the `api` object
  - Call `POST /api/generate-query` endpoint
  - Return `QueryGenerationResponse` type
  - Follow existing API request patterns

- **app/client/src/types.d.ts** - TypeScript type definitions
  - Need to add `QueryGenerationRequest` interface (empty object)
  - Need to add `QueryGenerationResponse` interface with `query: string` and `error?: string`
  - Must match Pydantic models exactly

- **app/client/index.html** - HTML structure
  - Need to add new button `<button id="generate-query-button">` in the query controls section
  - Position it with `justify-content: space-between` to separate from primary action buttons
  - Use `secondary-button` class for consistent styling with "Upload Data" button
  - Place in `.query-controls` div alongside existing buttons

- **app/client/src/style.css** - CSS styles
  - The `secondary-button` class already exists and will be reused
  - The `.query-controls` already has flex layout with `justify-content: space-between`
  - May need to adjust `.primary-actions` to group Query and Upload Data buttons together
  - Verify loading state styles (`.loading` spinner) work with the new button

### New Files

#### Test Files

- **app/server/tests/core/test_query_generator.py** - Unit tests for query generation
  - Test `generate_natural_language_query_with_openai()` function
  - Test `generate_natural_language_query_with_anthropic()` function
  - Test `generate_natural_language_query()` routing logic
  - Test schema validation (no tables error handling)
  - Test sentence limit enforcement (max 2 sentences)
  - Mock LLM API calls to avoid external dependencies
  - Test API key priority logic (OpenAI > Anthropic)

- **.claude/commands/e2e/test_nl_query_generator.md** - End-to-end test specification
  - Follow the format from `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_complex_query.md`
  - Define user story, test steps, and success criteria
  - Include steps to verify button presence, styling, and positioning
  - Test happy path: click button, verify query generation, verify overwrite behavior
  - Test edge cases: no tables available, loading state, multiple clicks
  - Test query execution: verify generated queries can be executed successfully
  - Capture screenshots at key points
  - Verify two-sentence maximum constraint
  - Read `.claude/commands/test_e2e.md` for E2E test execution instructions

### Configuration Files

- **.env.sample** - Environment variable template
  - Already contains `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`
  - No changes needed (same keys used for query generation)

- **README.md** - Project documentation
  - May need minor update to document new button functionality
  - Add to features list if applicable

## Implementation Plan

### Phase 1: Foundation
Set up the backend infrastructure for query generation by extending the existing LLM processor with new functions that generate natural language queries instead of SQL. This phase establishes the data models and API contract between frontend and backend.

**Key activities:**
1. Define Pydantic data models for request/response
2. Create TypeScript type definitions to match backend models
3. Implement core LLM query generation functions with proper error handling
4. Add unit tests with mocked LLM responses

### Phase 2: Core Implementation
Build the API endpoint and frontend components that enable users to generate queries with a single button click. This phase connects the backend logic to the user interface.

**Key activities:**
1. Create FastAPI endpoint that integrates with LLM processor
2. Add API client method in frontend
3. Implement button UI in HTML with proper positioning
4. Wire up button click handler with loading states and error handling
5. Ensure generated query overwrites existing input field content

### Phase 3: Integration
Integrate the feature with the existing application flow, add comprehensive testing, and validate the feature works end-to-end with zero regressions.

**Key activities:**
1. Create E2E test specification following existing patterns
2. Test query generation with different schema configurations
3. Verify loading states and error handling
4. Validate generated queries can be executed successfully
5. Run full test suite to ensure no regressions

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Set up backend data models
- Open `app/server/core/data_models.py`
- Add `QueryGenerationRequest` model (empty class, no fields needed)
- Add `QueryGenerationResponse` model with fields: `query: str` and `error: Optional[str] = None`
- Follow existing model patterns (use Pydantic `BaseModel`, proper imports)
- These models define the API contract between frontend and backend

### Step 2: Add TypeScript type definitions
- Open `app/client/src/types.d.ts`
- Add `QueryGenerationRequest` interface (empty object)
- Add `QueryGenerationResponse` interface with `query: string` and `error?: string`
- Ensure types match the Pydantic models exactly
- Add comment: `// These must match the Pydantic models exactly`

### Step 3: Implement OpenAI query generation function
- Open `app/server/core/llm_processor.py`
- Add function `generate_natural_language_query_with_openai(schema_info: Dict[str, Any]) -> str`
- Use `format_schema_for_prompt()` to prepare schema description
- Create prompt that instructs the LLM to generate an interesting natural language query
- Specify requirements in prompt: TWO SENTENCES MAXIMUM, realistic, natural, contextually relevant
- Use model `gpt-4.1-mini` with temperature `0.7` (higher for variety)
- Set max_tokens to `100` (sufficient for 2 sentences)
- Clean up response (remove any markdown formatting)
- Enforce two-sentence limit by splitting on `. ` and truncating
- Handle API errors with descriptive error messages
- Follow existing function patterns in the file

### Step 4: Implement Anthropic query generation function
- In `app/server/core/llm_processor.py`
- Add function `generate_natural_language_query_with_anthropic(schema_info: Dict[str, Any]) -> str`
- Use same prompt structure as OpenAI version
- Use model `claude-3-haiku-20240307` with temperature `0.7`
- Set max_tokens to `100`
- Clean up response and enforce two-sentence limit
- Handle API errors consistently with OpenAI version
- Ensure both functions have identical behavior except for API client

### Step 5: Implement routing logic for query generation
- In `app/server/core/llm_processor.py`
- Add function `generate_natural_language_query(schema_info: Dict[str, Any]) -> str`
- Check if `schema_info.get('tables')` is empty or None
- If no tables, raise `ValueError` with message: "No tables available in database. Please upload data first."
- Route to OpenAI if `OPENAI_API_KEY` environment variable exists
- Route to Anthropic if `ANTHROPIC_API_KEY` environment variable exists
- If neither API key exists, raise `ValueError` with message: "No LLM API keys configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable."
- Follow the same routing priority as `generate_sql()` function

### Step 6: Create FastAPI endpoint
- Open `app/server/server.py`
- Import `QueryGenerationRequest` and `QueryGenerationResponse` from `core.data_models`
- Import `generate_natural_language_query` from `core.llm_processor`
- Add endpoint `@app.post("/api/generate-query", response_model=QueryGenerationResponse)`
- Create function `async def generate_query_endpoint(request: QueryGenerationRequest) -> QueryGenerationResponse`
- Get database schema using `get_database_schema()`
- Call `generate_natural_language_query(schema_info)`
- Return `QueryGenerationResponse(query=query)`
- Wrap in try/except to handle errors and return error response
- Add logging using `logger.info()` for success and `logger.error()` for failures
- Follow existing endpoint patterns (e.g., `/api/query`, `/api/upload`)

### Step 7: Create unit tests for query generation
- Create file `app/server/tests/core/test_query_generator.py`
- Import pytest, unittest.mock, and necessary modules
- Test `generate_natural_language_query_with_openai()`:
  - Mock `OpenAI` client and its `chat.completions.create()` method
  - Provide sample schema with tables and columns
  - Verify correct model, temperature, and max_tokens are used
  - Verify prompt contains schema information
  - Verify function returns generated query
  - Test markdown cleanup (if LLM returns ```...```)
  - Test two-sentence truncation
- Test `generate_natural_language_query_with_anthropic()`:
  - Mock `Anthropic` client and its `messages.create()` method
  - Similar test coverage as OpenAI tests
- Test `generate_natural_language_query()` routing:
  - Mock environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
  - Test OpenAI priority (if both keys exist, use OpenAI)
  - Test Anthropic fallback (if only Anthropic key exists)
  - Test error when no tables exist (should raise ValueError)
  - Test error when no API keys configured (should raise ValueError)
- Follow existing test patterns from `app/server/tests/core/test_llm_processor.py`
- Run tests: `cd app/server && uv run pytest tests/core/test_query_generator.py -v`

### Step 8: Add frontend API client method
- Open `app/client/src/api/client.ts`
- Add method `generateQuery()` to the `api` object
- Make POST request to `/generate-query` endpoint
- Set headers: `Content-Type: application/json`
- Send empty JSON body: `JSON.stringify({})`
- Return type: `Promise<QueryGenerationResponse>`
- Use existing `apiRequest<QueryGenerationResponse>()` helper
- Follow patterns from existing methods like `processQuery()` and `getSchema()`

### Step 9: Update HTML structure with Generate Query button
- Open `app/client/index.html`
- Locate the `.query-controls` div (around line 22-28)
- Wrap the existing "Query" and "Upload Data" buttons in a new `<div class="primary-actions">` container
- Add new button outside the primary-actions div: `<button id="generate-query-button" class="secondary-button">Generate Query</button>`
- Ensure the `.query-controls` div has structure:
  ```html
  <div class="query-controls">
    <div class="primary-actions">
      <button id="query-button">Query</button>
      <button id="upload-data-button">Upload Data</button>
    </div>
    <button id="generate-query-button">Generate Query</button>
  </div>
  ```
- This creates visual separation: primary actions on left, generate query on right

### Step 10: Update CSS for button layout
- Open `app/client/src/style.css`
- Locate `.query-controls` section (around line 80-86)
- Verify it has `display: flex`, `justify-content: space-between`, and `gap: 1rem`
- Add new `.primary-actions` style:
  ```css
  .primary-actions {
    display: flex;
    gap: 1rem;
    align-items: center;
  }
  ```
- This groups Query and Upload Data buttons together on the left
- Verify `.secondary-button` styles exist (should already be defined)
- Verify `.loading` spinner styles exist (should already be defined)
- No other CSS changes needed (reusing existing styles)

### Step 11: Implement Generate Query button handler
- Open `app/client/src/main.ts`
- Create function `initializeGenerateQueryButton()`
- Get button element: `document.getElementById('generate-query-button')`
- Get query input element: `document.getElementById('query-input')`
- Add click event listener to the button
- In the click handler:
  - Disable button: `generateButton.disabled = true`
  - Save original button text
  - Show loading state: `generateButton.innerHTML = '<span class="loading"></span>'`
  - Call `api.generateQuery()` in try block
  - If response has error, call `displayError(response.error)`
  - If successful, set `queryInput.value = response.query` (overwrites existing content)
  - Focus the input field: `queryInput.focus()`
  - In catch block, call `displayError()` with error message
  - In finally block, re-enable button and restore original text
- Follow existing patterns from `initializeQueryInput()` and `initializeFileUpload()`

### Step 12: Initialize button handler on page load
- In `app/client/src/main.ts`
- Locate the `DOMContentLoaded` event listener (around line 7-13)
- Add call to `initializeGenerateQueryButton()` after `initializeQueryInput()`
- Ensure it's called before `loadDatabaseSchema()` so button is ready when page loads

### Step 13: Create E2E test specification
- Create file `.claude/commands/e2e/test_nl_query_generator.md`
- Read `.claude/commands/test_e2e.md` to understand E2E test execution framework
- Read `.claude/commands/e2e/test_basic_query.md` for format reference
- Read `.claude/commands/e2e/test_complex_query.md` for additional examples
- Define User Story:
  - As a user, I want to generate example natural language queries based on my uploaded tables
  - So that I can quickly explore my data without having to think of queries myself
- Define Test Steps:
  - Setup: Navigate to app, upload sample data, verify tables loaded
  - Verify Generate Query button is visible and properly styled
  - Test happy path: click button, verify loading state, verify query populates input field
  - Verify generated query is max 2 sentences
  - Test overwrite behavior: enter text, click button, verify old text is replaced
  - Test generated query execution: click Query button, verify results display
  - Test error handling: remove all tables, click button, verify error message
  - Test loading state: verify button cannot be clicked multiple times while loading
- Define Success Criteria:
  - Button visible and styled correctly
  - Loading state works
  - Query generation overwrites input field
  - Generated queries are ≤ 2 sentences
  - Error handling works when no tables exist
  - Generated queries can be executed successfully
- Specify screenshot captures at each major step
- Follow the exact format from existing E2E test files

### Step 14: Run validation commands to ensure zero regressions
- Read `.claude/commands/test_e2e.md` to understand how to execute E2E tests
- Run backend unit tests: `cd app/server && uv run pytest`
- Verify all tests pass, including new `test_query_generator.py` tests
- Run frontend type checking: `cd app/client && bun tsc --noEmit`
- Verify no TypeScript errors
- Run frontend build: `cd app/client && bun run build`
- Verify build succeeds
- Execute the E2E test file `.claude/commands/e2e/test_nl_query_generator.md` using the E2E test runner
- Verify all E2E test steps pass
- Capture screenshots and verify visual appearance
- Test the feature manually to ensure it works as expected

## Testing Strategy

### Unit Tests

**Backend Tests (app/server/tests/core/test_query_generator.py):**

1. **Test OpenAI Query Generation**
   - Mock OpenAI API client to return a sample query
   - Verify the function calls OpenAI with correct parameters (model, temperature, max_tokens)
   - Verify the prompt includes database schema information
   - Verify markdown cleanup (remove ```sql, ``` markers)
   - Verify two-sentence truncation works correctly
   - Test error handling when API call fails

2. **Test Anthropic Query Generation**
   - Mock Anthropic API client to return a sample query
   - Verify the function calls Anthropic with correct parameters
   - Verify prompt structure matches OpenAI version
   - Verify markdown cleanup and sentence truncation
   - Test error handling when API call fails

3. **Test Routing Logic**
   - Mock environment variables (OPENAI_API_KEY, ANTHROPIC_API_KEY)
   - Test OpenAI priority: when both keys exist, OpenAI should be used
   - Test Anthropic fallback: when only Anthropic key exists, use Anthropic
   - Test error when no tables exist: should raise ValueError with appropriate message
   - Test error when no API keys configured: should raise ValueError
   - Verify error messages are descriptive and user-friendly

4. **Test Schema Validation**
   - Test with empty schema (no tables)
   - Test with single table schema
   - Test with multiple tables schema
   - Verify `format_schema_for_prompt()` is called correctly

**Frontend Tests (manual, via type checking and build):**
- TypeScript compilation should pass with no errors
- Build process should complete successfully
- No console errors when button is clicked

### Edge Cases

1. **No Tables Available**
   - User clicks Generate Query button when no tables are uploaded
   - Expected: Error message displayed: "No tables available in database. Please upload data first."
   - Button returns to normal state after error

2. **API Key Missing**
   - Neither OPENAI_API_KEY nor ANTHROPIC_API_KEY is configured
   - Expected: Error message displayed: "No LLM API keys configured..."
   - Handled gracefully in backend with descriptive error

3. **LLM Returns More Than 2 Sentences**
   - Mock LLM to return a query with 5 sentences
   - Expected: Function truncates to first 2 sentences
   - Verify truncation logic: split on `. `, take first 2, add `.` at end

4. **LLM Returns Markdown**
   - Mock LLM to return query wrapped in ```sql...``` or ```...```
   - Expected: Markdown is stripped, only plain text remains
   - Verify cleanup logic handles various markdown formats

5. **Concurrent Button Clicks**
   - User clicks Generate Query button multiple times rapidly
   - Expected: Button is disabled during first request
   - Second click has no effect until first request completes
   - Only one request is made to the backend

6. **Input Field Overwrite**
   - User has typed text in query input field
   - User clicks Generate Query button
   - Expected: Existing text is completely replaced by generated query
   - No remnants of old text remain

7. **Empty Response from LLM**
   - Mock LLM to return empty string or whitespace
   - Expected: Error is handled gracefully
   - User sees appropriate error message

8. **Long Schema (Many Tables)**
   - Database has 20+ tables with many columns
   - Expected: Schema is formatted correctly in prompt
   - Query generation completes successfully
   - Response time is reasonable

9. **Network Error**
   - API request to `/api/generate-query` fails (network issue)
   - Expected: Error is caught in frontend
   - `displayError()` is called with error message
   - Button returns to normal state

10. **Generated Query Execution**
    - Generated query is populated in input field
    - User clicks Query button to execute it
    - Expected: Query executes successfully
    - Results are displayed
    - SQL translation is shown

## Acceptance Criteria

1. **Button Presence and Styling**
   - Generate Query button is visible in the query controls section
   - Button uses the `secondary-button` class (matching Upload Data button style)
   - Button is positioned with visual separation from Query and Upload Data buttons (justify-content: space-between)
   - Button has proper spacing (gap) from other elements

2. **Loading State**
   - When clicked, button shows loading spinner
   - Button is disabled during query generation
   - Button text is temporarily replaced with spinner
   - Button cannot be clicked again until generation completes
   - Original button text is restored after completion

3. **Query Generation**
   - Clicking the button calls `/api/generate-query` endpoint
   - Backend uses LLM (OpenAI or Anthropic) to generate query
   - Generated query is contextually relevant to database schema
   - Generated query is limited to TWO SENTENCES MAXIMUM
   - Generated query uses natural language, not SQL syntax
   - Generated query is realistic (like a user would actually type)

4. **Input Field Population**
   - Generated query is populated in the query input field
   - Existing content in the input field is completely overwritten
   - Input field is focused after query is generated
   - User can immediately edit the generated query if desired

5. **Error Handling**
   - If no tables exist, error message is displayed: "No tables available in database. Please upload data first."
   - If no API keys configured, appropriate error is shown
   - If API call fails, error is displayed to user
   - Errors use the existing `displayError()` function
   - Button returns to normal state after error

6. **Query Execution**
   - Generated queries can be executed by clicking the Query button
   - Execution follows the same flow as manually entered queries
   - Results are displayed correctly
   - SQL translation is shown

7. **API Key Routing**
   - If OPENAI_API_KEY exists, use OpenAI for generation
   - If only ANTHROPIC_API_KEY exists, use Anthropic
   - Routing logic matches the existing `generate_sql()` function

8. **Unit Tests**
   - All unit tests in `test_query_generator.py` pass
   - Tests cover OpenAI generation, Anthropic generation, and routing logic
   - Tests verify two-sentence limit enforcement
   - Tests verify error handling (no tables, no API keys)
   - Mock LLM API calls to avoid external dependencies

9. **Type Safety**
   - TypeScript types match Pydantic models exactly
   - No TypeScript compilation errors
   - Frontend build succeeds

10. **Zero Regressions**
    - All existing backend tests pass (`cd app/server && uv run pytest`)
    - Frontend type checking passes (`cd app/client && bun tsc --noEmit`)
    - Frontend build succeeds (`cd app/client && bun run build`)
    - Existing functionality is not broken

11. **E2E Validation**
    - E2E test file `.claude/commands/e2e/test_nl_query_generator.md` is created
    - E2E test covers all scenarios: happy path, edge cases, error handling
    - All E2E test steps pass when executed
    - Screenshots are captured and verify visual correctness

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md` to understand E2E test execution
- Read and execute `.claude/commands/e2e/test_nl_query_generator.md` to validate the Generate Query button functionality end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Implementation Considerations

1. **Reuse Existing Infrastructure**
   - The feature leverages the existing LLM processor (`core/llm_processor.py`)
   - Uses the same API key routing logic as SQL generation (OpenAI priority)
   - Uses the same error handling patterns
   - Follows existing frontend patterns for button initialization and API calls

2. **Temperature for Variety**
   - Use temperature `0.7` for query generation (higher than SQL generation's `0.1`)
   - This provides variety in generated queries
   - Users can click the button multiple times to get different query suggestions

3. **Sentence Limit Enforcement**
   - The two-sentence maximum is enforced both in the LLM prompt and in post-processing
   - Post-processing ensures the constraint is met even if the LLM ignores the instruction
   - Implementation: `sentences = query.split('. ')` then `query = '. '.join(sentences[:2]) + '.'`

4. **Schema Information**
   - The `get_database_schema()` function provides comprehensive schema information
   - Includes table names, column names, data types, and row counts
   - This context helps the LLM generate relevant, contextually appropriate queries

5. **Security Considerations**
   - No security concerns as the feature only generates text, not SQL
   - The generated text is not executed automatically
   - Users must manually click the Query button to execute
   - Existing SQL injection protections apply when the query is executed

6. **Cost Considerations**
   - Each button click makes one LLM API call
   - Using `gpt-4.1-mini` and `claude-3-haiku-20240307` (smaller, cheaper models)
   - Max tokens limited to 100 (very small, ~2 sentences)
   - Cost per generation is minimal

7. **UX Considerations**
   - Button positioning (right side) provides visual balance
   - Overwrite behavior is intentional (user always gets fresh query)
   - Focus on input field after generation allows immediate editing
   - Loading state prevents confusion during generation
   - Error messages guide users to resolve issues (e.g., upload data first)

8. **Future Enhancements** (out of scope for this feature)
   - Query history: save previously generated queries
   - Favorites: allow users to save interesting queries
   - Query categories: generate specific types of queries (aggregations, filters, etc.)
   - Multi-table query suggestions: specifically suggest JOIN queries
   - Regenerate with constraints: "generate a simpler query" or "generate a more complex query"

### Testing Notes

- E2E tests should upload sample data (users.json) to ensure tables exist
- E2E tests should verify the visual appearance matches design (spacing, alignment, styling)
- E2E tests should verify the two-sentence constraint by counting sentences in generated queries
- Unit tests should mock all external API calls to avoid costs and external dependencies
- Unit tests should test various schema configurations (empty, single table, multiple tables)

### Documentation

- The README.md may benefit from a brief mention of the Generate Query button in the Usage section
- Consider adding a note: "Click 'Generate Query' to get query suggestions based on your data"
- However, the UI should be self-explanatory, so extensive documentation may not be necessary
