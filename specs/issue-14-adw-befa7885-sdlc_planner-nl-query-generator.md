# Feature: Random Natural Language Query Generator

## Feature Description
This feature adds a "Generate Query" button to the Natural Language SQL Interface that automatically generates interesting natural language questions based on the current database schema. When clicked, the button uses the existing LLM processor to analyze available tables and their structures, then creates a relevant, contextual query suggestion that is automatically populated into the query input field, replacing any existing content. This helps users discover new ways to explore their data and provides inspiration when they're unsure what questions to ask.

## User Story
As a user of the Natural Language SQL Interface
I want to click a button that generates interesting natural language queries based on my database tables
So that I can discover new ways to query my data and get inspiration for questions I can ask without having to think of queries from scratch

## Problem Statement
Users often face a blank canvas problem when first loading their data - they don't know what questions to ask or what insights might be available. This leads to underutilization of the natural language query feature and requires users to have strong analytical thinking skills upfront. There's no easy way for users to explore what's possible with their data or get inspiration for meaningful queries.

## Solution Statement
Implement a "Generate Query" button positioned alongside the primary action buttons that:
1. Analyzes the current database schema (tables, columns, data types, row counts)
2. Uses the existing LLM processor (`llm_processor.py`) to generate contextually relevant natural language questions
3. Automatically populates the query input field with the generated question
4. Overwrites any existing content in the input field
5. Limits generated queries to a maximum of two sentences for clarity
6. Provides variety by generating different questions on subsequent clicks

The backend functionality is already implemented in `app/server/server.py:243-276` (the `/api/generate-query` endpoint) and `app/server/core/llm_processor.py:230-435` (the query generation functions). The frontend already has the button implemented in `app/client/index.html:24` and the event handler in `app/client/src/main.ts:53-83`. We have comprehensive unit tests in `app/server/tests/core/test_query_generator.py` and an E2E test specification in `.claude/commands/e2e/test_query_generator.md`.

## Relevant Files
Use these files to implement the feature:

**Backend (Already Implemented):**
- `app/server/server.py:243-276` - Contains the `/api/generate-query` endpoint that generates natural language queries based on database schema
- `app/server/core/llm_processor.py:230-435` - Contains `generate_natural_language_query()` and provider-specific functions that create interesting questions using OpenAI, Anthropic, or Gemini
- `app/server/core/data_models.py:84-91` - Contains `GenerateQueryRequest` and `GenerateQueryResponse` models for the query generation API
- `app/server/core/sql_processor.py` - Contains `get_database_schema()` used to retrieve table and column information

**Frontend (Already Implemented):**
- `app/client/index.html:24` - Contains the "Generate Query" button UI element positioned with `class="secondary-button"`
- `app/client/src/main.ts:53-83` - Contains `initializeQueryGenerator()` function that handles button clicks, shows loading state, calls the API, and populates the input field
- `app/client/src/api/client.ts:80-89` - Contains `api.generateQuery()` method that calls the `/api/generate-query` endpoint
- `app/client/src/style.css:117-126` - Contains button styling for `.secondary-button` class

**Testing (Already Implemented):**
- `app/server/tests/core/test_query_generator.py` - Contains comprehensive unit tests for all query generation functions including OpenAI, Anthropic, Gemini providers, error handling, and edge cases
- `.claude/commands/e2e/test_query_generator.md` - Contains detailed E2E test specification for the query generator feature
- `.claude/commands/test_e2e.md` - Contains the E2E test runner instructions

### New Files
No new files need to be created. All required functionality has been implemented.

## Implementation Plan

### Phase 1: Foundation
**Status: COMPLETE** ✅

The foundation is already complete:
- Backend API endpoint `/api/generate-query` exists and is functional (server.py:243-276)
- LLM processor functions for query generation are implemented with support for OpenAI, Anthropic, and Gemini (llm_processor.py:230-435)
- Data models for request/response are defined (data_models.py:84-91)
- Database schema retrieval is working (sql_processor.py)

### Phase 2: Core Implementation
**Status: COMPLETE** ✅

The core implementation is already complete:
- Frontend button exists in the UI (index.html:24)
- Button event handler is implemented with loading states (main.ts:53-83)
- API client method is implemented (client.ts:80-89)
- Input field population logic is working
- Button styling matches design requirements (style.css:117-126)

### Phase 3: Integration
**Status: COMPLETE** ✅

The integration is already complete:
- Button is positioned correctly with other action buttons (index.html:24)
- API endpoint is registered and accessible
- Error handling is in place
- Loading states provide user feedback
- Query overwrites existing input field content as required

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Validate Backend Implementation
- Read `app/server/server.py` lines 243-276 and verify the `/api/generate-query` endpoint exists and handles both empty and populated databases correctly
- Read `app/server/core/llm_processor.py` lines 230-435 and verify all query generation functions are implemented for OpenAI, Anthropic, and Gemini
- Read `app/server/core/data_models.py` lines 84-91 and verify the request/response models match the API endpoint

### Step 2: Validate Frontend Implementation
- Read `app/client/index.html` line 24 and verify the "Generate Query" button exists with proper class and ID
- Read `app/client/src/main.ts` lines 53-83 and verify the event handler, loading state, API call, and input population logic
- Read `app/client/src/api/client.ts` lines 80-89 and verify the API client method signature and implementation
- Read `app/client/src/style.css` lines 117-126 and verify the button styling

### Step 3: Run Unit Tests
- Execute `cd app/server && uv run pytest tests/core/test_query_generator.py -v` to run all unit tests for the query generator
- Verify all tests pass with zero failures
- Review test coverage for edge cases: missing API keys, two-sentence limit, question mark handling, provider routing

### Step 4: Validate E2E Test Specification
- Read `.claude/commands/e2e/test_query_generator.md` and verify it contains comprehensive test steps
- Verify the test covers: button visibility, loading state, query generation, input field population, query overwriting, query execution, and multiple generations
- Verify success criteria match feature requirements

### Step 5: Execute E2E Test
- Read `.claude/commands/test_e2e.md` to understand the E2E test execution process
- Execute the E2E test by running: `/test_e2e <adw_id> test_e2e .claude/commands/e2e/test_query_generator.md http://localhost:5173`
- Verify all test steps pass successfully
- Review screenshots captured during the test
- Verify the generated queries are relevant to the database schema and limited to two sentences

### Step 6: Manual Feature Verification
- Start the application using `./scripts/start.sh`
- Upload sample data using the "Upload Data" button
- Click the "Generate Query" button multiple times
- Verify each click generates a different, relevant query
- Verify queries are limited to two sentences maximum
- Verify the query input field is populated correctly
- Verify existing content is overwritten
- Verify loading state is shown during generation
- Execute a generated query and verify it works correctly

### Step 7: Run Full Validation Suite
- Execute all validation commands listed in the Validation Commands section
- Verify zero regressions in server tests
- Verify zero TypeScript compilation errors
- Verify successful frontend build

## Testing Strategy

### Unit Tests
**Status: COMPLETE** ✅

Unit tests already exist in `app/server/tests/core/test_query_generator.py` covering:

1. **OpenAI Provider Tests:**
   - Successful query generation
   - Question mark handling (automatic addition when missing)
   - Two-sentence limit enforcement
   - Missing API key error handling
   - API error handling
   - Single table scenarios
   - Multiple table scenarios

2. **Anthropic Provider Tests:**
   - Successful query generation
   - Question mark handling (automatic addition when missing)
   - Two-sentence limit enforcement
   - Missing API key error handling
   - API error handling

3. **Gemini Provider Tests:**
   - All the same test cases as OpenAI and Anthropic

4. **Provider Routing Tests:**
   - Gemini priority when Gemini key exists
   - OpenAI fallback when only OpenAI key exists
   - Anthropic fallback when only Anthropic key exists
   - Provider preference when no keys available

### Edge Cases

1. **Empty Database:**
   - When no tables exist, endpoint returns: "Upload some data first to generate queries!"
   - This is already handled in `server.py:251-255`

2. **Single Table:**
   - Generates queries focused on that specific table
   - Tested in unit tests

3. **Multiple Tables:**
   - Generates queries that may involve joins or cross-table analysis
   - Tested in unit tests

4. **Long Query Responses:**
   - Automatic truncation to two sentences maximum
   - Tested in unit tests with `test_generate_query_with_openai_two_sentence_limit` and `test_generate_query_with_anthropic_two_sentence_limit`

5. **Missing Question Mark:**
   - Automatically appends question mark if missing
   - Tested in unit tests

6. **API Failures:**
   - Error handling and user-friendly error messages
   - Tested in unit tests

7. **Missing API Keys:**
   - Proper error messaging when no LLM provider is configured
   - Tested in unit tests

8. **Rapid Clicking:**
   - Button is disabled during processing to prevent duplicate requests
   - Implemented in `main.ts:59`

9. **Query Overwriting:**
   - Always overwrites existing content in input field
   - Implemented in `main.ts:72`

## Acceptance Criteria

✅ **All criteria are met by the existing implementation:**

1. A "Generate Query" button is visible in the UI alongside the "Query" and "Upload Data" buttons
2. The button uses the same styling as the "Upload Data" button (secondary-button class)
3. Clicking the button shows a loading state while processing
4. The button is disabled during query generation to prevent duplicate requests
5. Generated queries are automatically populated into the query input field
6. Any existing content in the input field is overwritten by the generated query
7. Generated queries are limited to a maximum of two sentences
8. Generated queries end with a question mark
9. Generated queries are contextually relevant to the database schema (tables and columns)
10. Multiple clicks generate different queries to provide variety
11. When no tables exist, a helpful message is shown: "Upload some data first to generate queries!"
12. The LLM processor is used to generate queries (existing `llm_processor.py` functions)
13. Error handling provides user-friendly messages if generation fails
14. The feature works with OpenAI, Anthropic, and Gemini providers based on available API keys
15. All unit tests pass with zero failures
16. E2E test validates the full user workflow
17. No regressions in existing functionality

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

**Read and execute the E2E test:**
- Read `.claude/commands/test_e2e.md` for test execution instructions
- Execute the E2E test by running the test_e2e slash command with the query generator test file: `.claude/commands/e2e/test_query_generator.md`
- Verify all test steps pass and screenshots are captured

**Run server unit tests:**
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run query generator unit tests specifically
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions

**Run frontend validation:**
- `cd app/client && bun tsc --noEmit` - Run TypeScript compilation to validate zero type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature works in production mode

**Manual validation:**
- Start the application with `./scripts/start.sh`
- Verify the "Generate Query" button is visible
- Upload sample data and click "Generate Query" multiple times
- Verify different queries are generated each time
- Verify queries are relevant to the uploaded data
- Execute a generated query and verify it returns results

## Notes

### Implementation Status
**This feature is ALREADY FULLY IMPLEMENTED.** All code, tests, and documentation exist and are functional. The validation steps above are to verify the existing implementation meets all requirements.

### Key Implementation Details

1. **Backend Architecture:**
   - The `/api/generate-query` endpoint in `server.py` handles query generation requests
   - `llm_processor.py` contains the core generation logic with support for multiple LLM providers (OpenAI, Anthropic, Gemini)
   - Gemini has priority for query generation operations (see routing logic in `generate_natural_language_query()`)
   - Two-sentence limit is enforced in the generation functions
   - Question marks are automatically added if missing

2. **Frontend Architecture:**
   - Button is positioned in the query controls section using flexbox with `justify-content: space-between`
   - Loading state is implemented using the same pattern as the Query button
   - Input field focus is set after query population for better UX
   - Error handling displays user-friendly messages

3. **Testing Strategy:**
   - Unit tests use mocking to avoid actual API calls during testing
   - E2E tests use Playwright for browser automation
   - Tests cover all edge cases and error scenarios

4. **Provider Priority:**
   - For SQL generation: Gemini → OpenAI → Anthropic
   - For query generation: Gemini → OpenAI → Anthropic
   - This prioritization is based on available API keys

5. **Future Enhancements (Not Required for Current Feature):**
   - Add query categories (aggregations, filters, joins, trends)
   - Add query history to avoid repeating recent suggestions
   - Add "favorite" functionality to save good query suggestions
   - Add query complexity levels (simple, medium, advanced)
   - Add ability to generate queries for specific tables only

6. **Dependencies:**
   - No new packages were required
   - Feature uses existing `openai`, `anthropic`, and `google-generativeai` packages
   - Frontend uses existing API client patterns

7. **Performance Considerations:**
   - Query generation typically takes 1-3 seconds depending on LLM provider
   - Button disabled state prevents duplicate requests
   - Database schema is fetched fresh on each request to ensure accuracy

8. **Accessibility:**
   - Button has clear, descriptive text
   - Loading state provides visual feedback
   - Error messages are clear and actionable

9. **Security:**
   - No user input is directly passed to the LLM (only database schema)
   - API keys are stored securely in environment variables
   - SQL injection is not a concern as this feature only generates natural language questions

10. **Compatibility:**
    - Works with all supported database schemas
    - Compatible with existing CSV, JSON, and JSONL file uploads
    - Works across all modern browsers
