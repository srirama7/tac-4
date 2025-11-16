# Feature: Natural Language Query Generator Button

## Feature Description
Add a new button that generates interesting natural language query suggestions based on existing database tables and their structure. The button will populate the query input field with automatically generated queries, allowing users to quickly explore their data without having to think of questions themselves. The generated queries will be contextually relevant to the uploaded data and limited to two sentences maximum.

## User Story
As a user of the Natural Language SQL Interface
I want to click a button that automatically generates interesting query suggestions based on my uploaded data
So that I can quickly explore my data and get inspiration for questions without having to think of queries myself

## Problem Statement
Users who upload data to the application may not know what questions to ask or may struggle to formulate natural language queries. This creates a barrier to entry and reduces the value users get from the application, particularly during the initial exploration phase. Users need an easy way to discover the capabilities of the natural language query system and get inspiration for useful queries based on their specific data.

## Solution Statement
Implement a "Generate Query" button that uses the existing LLM infrastructure (OpenAI, Anthropic, or Gemini) to analyze the current database schema and generate contextually relevant, interesting natural language queries. The button will be placed alongside the existing "Upload Data" button in the secondary buttons section, using the same visual styling. When clicked, it will call a new backend endpoint that generates a 2-sentence maximum query suggestion and populates it into the input field, ready for the user to execute manually. This provides immediate value and helps users understand what types of questions they can ask.

## Relevant Files
Use these files to implement the feature:

- **`app/server/server.py`** - Contains the FastAPI server with existing endpoints. We'll add a new `/api/generate-query-suggestion` endpoint here that mirrors the pattern of existing endpoints. (Lines 244-286 already implement this endpoint!)
- **`app/server/core/query_generator.py`** - NEW FILE already created that contains the core query generation logic with support for OpenAI, Anthropic, and Gemini providers. Includes routing logic similar to `llm_processor.py`.
- **`app/server/core/data_models.py`** - Contains Pydantic models for request/response. We'll reference existing `QuerySuggestionRequest` and `QuerySuggestionResponse` models (lines 85-91).
- **`app/server/core/llm_processor.py`** - Contains existing LLM integration patterns we should follow (format_schema_for_prompt function pattern, error handling, API key checking).
- **`app/client/index.html`** - Contains the UI structure. The "Generate Query" button already exists at line 25 in the secondary-buttons section.
- **`app/client/src/main.ts`** - Contains client-side logic. The Generate Query button handler already exists at lines 45-69.
- **`app/client/src/api/client.ts`** - Contains API client methods. The `generateQuerySuggestion` method already exists at lines 80-89.
- **`app/client/src/style.css`** - Contains styling. The button uses existing `.secondary-button` class which provides consistent styling with "Upload Data" button.
- **`app/client/src/types.d.ts`** - Contains TypeScript type definitions for API responses.

### New Files
- **`.claude/commands/e2e/test_query_generator.md`** - E2E test file to validate the query generator button works correctly (already exists at `../.claude/commands/e2e/test_query_generator.md`).
- **`app/server/tests/core/test_query_generator.py`** - Unit tests for the query generator module (already exists).

## Implementation Plan
### Phase 1: Foundation
**Status: ALREADY COMPLETE** - The backend query generator module has been implemented in `app/server/core/query_generator.py` with full support for three LLM providers (Gemini, OpenAI, Anthropic). The API endpoint `/api/generate-query-suggestion` has been added to `server.py` and follows existing patterns for error handling and logging. Unit tests exist in `app/server/tests/core/test_query_generator.py`. Data models are defined in `data_models.py`.

### Phase 2: Core Implementation
**Status: ALREADY COMPLETE** - The frontend implementation is complete. The "Generate Query" button exists in `index.html` (line 25), the click handler is implemented in `main.ts` (lines 45-69), the API client method exists in `client.ts` (lines 80-89), and styling is applied via the existing `.secondary-button` class in `style.css`.

### Phase 3: Integration
**Status: NEEDS VALIDATION** - The feature is fully implemented but requires comprehensive testing to ensure:
1. The button correctly calls the backend API
2. The generated query properly populates the input field
3. Error messages display appropriately when no data is uploaded
4. The feature works with all three LLM providers
5. The 2-sentence limit is enforced
6. The UI provides proper loading states and error feedback

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Verify Backend Implementation
- Read `app/server/core/query_generator.py` to confirm it contains all three LLM provider implementations
- Read `app/server/server.py` to confirm the `/api/generate-query-suggestion` endpoint is properly implemented (lines 244-286)
- Read `app/server/core/data_models.py` to confirm request/response models exist (lines 85-91)
- Verify the endpoint follows the same error handling patterns as other endpoints

### Step 2: Verify Frontend Implementation
- Read `app/client/index.html` to confirm the "Generate Query" button exists in the UI (line 25)
- Read `app/client/src/main.ts` to confirm the button click handler is implemented (lines 45-69)
- Read `app/client/src/api/client.ts` to confirm the API client method exists (lines 80-89)
- Read `app/client/src/types.d.ts` to confirm TypeScript types are defined for the API response
- Verify the button uses the `.secondary-button` class for consistent styling

### Step 3: Verify Unit Tests Exist
- Read `app/server/tests/core/test_query_generator.py` to confirm unit tests exist for the query generator module
- Verify tests cover all three LLM providers (OpenAI, Anthropic, Gemini)
- Verify tests check error cases (empty database, missing API keys)
- Run the unit tests: `cd app/server && uv run pytest tests/core/test_query_generator.py -v`

### Step 4: Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand the E2E test framework structure and requirements
- Read `.claude/commands/e2e/test_basic_query.md` as an example of E2E test format
- Read `.claude/commands/e2e/test_complex_query.md` as another example
- Review the existing E2E test file at `../.claude/commands/e2e/test_query_generator.md` (if it exists, validate it; if not, create it)
- The E2E test should validate:
  - Button is visible and clickable
  - Clicking the button shows a loading state
  - Generated query appears in the input field
  - Query is limited to 2 sentences
  - Error message appears when database is empty
  - Button returns to normal state after completion
- Include at least 5 screenshots showing: initial state, button click, loading state, populated query field, and final ready state

### Step 5: Manual Integration Testing
- Start the development server: `./scripts/start.sh`
- Navigate to http://localhost:5173
- Test the "Generate Query" button without any data uploaded (should show error)
- Upload sample data using one of the sample data buttons
- Click "Generate Query" button
- Verify the query input field is populated with a natural language query
- Verify the query is 2 sentences or less
- Verify the query makes sense given the uploaded data structure
- Click the "Query" button to execute the generated query
- Verify the generated query executes successfully and returns results
- Test with different sample datasets (users, products, events)
- Take screenshots of successful query generation and execution

### Step 6: Verify Error Handling
- Clear the database by removing all tables
- Click "Generate Query" button
- Verify appropriate error message appears ("Database is empty. Please upload data first.")
- Test with missing API keys (temporarily rename .env file)
- Verify appropriate error message appears when no LLM API keys are configured
- Restore .env file

### Step 7: Verify LLM Provider Routing
- Read the `generate_query_suggestion` function in `app/server/core/query_generator.py` (lines 207-250)
- Verify it prioritizes Gemini, then OpenAI, then Anthropic (matching the comment priority)
- Test with only GEMINI_API_KEY set - verify it uses Gemini
- Test with only OPENAI_API_KEY set - verify it uses OpenAI
- Test with only ANTHROPIC_API_KEY set - verify it uses Anthropic

### Step 8: Code Quality Check
- Review all modified files for code style consistency
- Verify all functions have appropriate error handling
- Verify logging is consistent with existing patterns
- Check that TypeScript types are properly defined
- Ensure no console.log statements remain in production code

### Step 9: Run All Validation Commands
- Execute the complete validation suite as specified in the "Validation Commands" section below
- Ensure zero errors and zero regressions
- Document any issues found and resolve them

## Testing Strategy
### Unit Tests
- **`test_query_generator.py`** - Tests for the query generator module:
  - Test `generate_query_suggestion_with_openai` generates valid queries
  - Test `generate_query_suggestion_with_anthropic` generates valid queries
  - Test `generate_query_suggestion_with_gemini` generates valid queries
  - Test `format_schema_for_suggestion_prompt` formats schema correctly
  - Test `generate_query_suggestion` routing logic with different API key configurations
  - Test error handling when schema is empty
  - Test error handling when no API keys are configured
  - Test that generated queries are 2 sentences or less
  - Mock LLM API calls to avoid actual API usage during tests

### Edge Cases
1. **Empty Database** - User clicks "Generate Query" before uploading any data
   - Expected: Error message "Database is empty. Please upload data first."
2. **No API Keys Configured** - All LLM API keys are missing from environment
   - Expected: Error message about missing API keys
3. **Single Table** - Database has only one table
   - Expected: Query suggestion focuses on that single table
4. **Multiple Tables** - Database has multiple tables
   - Expected: Query suggestion may use single-table or join queries intelligently
5. **Large Schema** - Database has many columns and tables
   - Expected: Query suggestion focuses on most interesting/useful columns
6. **API Timeout** - LLM API takes too long to respond
   - Expected: Graceful timeout error message
7. **Invalid API Key** - API key is set but invalid
   - Expected: Appropriate error message from LLM provider
8. **Network Failure** - Network connection fails during API call
   - Expected: Network error message displayed to user

## Acceptance Criteria
1. "Generate Query" button is visible in the UI next to "Upload Data" button
2. Button uses consistent styling with other secondary buttons
3. Button is clickable and shows loading state when generating query
4. Clicking the button calls the `/api/generate-query-suggestion` endpoint
5. Generated query appears in the query input field (overwrites existing content)
6. Generated query is limited to 2 sentences maximum
7. Generated query is contextually relevant to the database schema
8. Error message displays when database is empty
9. Error message displays when no API keys are configured
10. Loading state clears after query generation completes
11. Button returns to normal state after generation (success or failure)
12. User can manually edit the generated query before executing
13. User can execute the generated query by clicking "Query" button
14. Feature works with all three LLM providers (Gemini, OpenAI, Anthropic)
15. All existing tests continue to pass (zero regressions)
16. New unit tests pass for query generator module
17. E2E test validates the feature works end-to-end
18. Code follows existing patterns and conventions

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

**Note:** Most implementation is already complete. Validation focuses on ensuring everything works correctly together.

- Read `.claude/commands/test_e2e.md` to understand E2E test framework
- Read and validate the E2E test file at `../.claude/commands/e2e/test_query_generator.md` exists and follows the correct format
- Execute the E2E test: `/test_e2e 2d2d10f0 test_e2e ../.claude/commands/e2e/test_query_generator.md http://localhost:5173` (requires server and client running)
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run query generator unit tests specifically
- `cd app/client && bun tsc --noEmit` - Run TypeScript type checking to validate zero errors
- `cd app/client && bun run build` - Run frontend build to validate zero errors
- Manual smoke test: Start app with `./scripts/start.sh`, upload sample data, click "Generate Query", verify query appears in input field, execute the query, verify it returns results

## Notes
### Implementation Status
This feature appears to be **already implemented** based on the code review:
- Backend endpoint exists in `server.py` (lines 244-286)
- Query generator module exists in `core/query_generator.py` with full implementation
- Frontend button exists in `index.html` (line 25)
- Frontend handler exists in `main.ts` (lines 45-69)
- API client method exists in `client.ts` (lines 80-89)
- Data models exist in `data_models.py` (lines 85-91)
- Unit tests exist in `tests/core/test_query_generator.py`
- E2E test file exists at `../.claude/commands/e2e/test_query_generator.md`

### Primary Focus
The implementation tasks should focus on **validation and testing** rather than new development:
1. Verify all existing code works correctly together
2. Run unit tests and fix any failures
3. Run E2E tests and fix any failures
4. Test edge cases and error conditions
5. Ensure zero regressions in existing functionality

### Future Enhancements
Consider for future iterations:
- Allow users to specify query complexity (simple, moderate, complex)
- Provide multiple query suggestions to choose from
- Add a "history" of generated queries
- Allow users to save favorite queries
- Generate queries based on specific tables (user-selected)
- Add support for more LLM providers (e.g., local models)
- Implement query suggestion caching to reduce API costs
- Add analytics to track which generated queries are most useful

### API Key Priority
The implementation uses Gemini as the primary provider for SQL operations, falling back to OpenAI, then Anthropic. This prioritization is intentional for cost and performance optimization with SQL-focused tasks.

### Security Considerations
- All generated queries go through the same SQL security validation as user-entered queries
- LLM-generated queries are not automatically executed - user must click "Query" button
- API keys are stored securely in environment variables
- No user data is sent to LLM APIs (only schema information)

### Dependencies
- Requires one of: GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY in environment
- Uses existing `google-generativeai`, `openai`, and `anthropic` Python packages
- No new npm packages required for frontend
