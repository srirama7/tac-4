# Feature: Query Generator Button

## Feature Description
Add a "Generate Query" button to the Natural Language SQL Interface that generates natural language queries based on existing database tables and their structure. The button will analyze the current database schema and use the LLM processor to create interesting, contextually relevant natural language questions that users can execute. Each click will generate a fresh query (limited to two sentences maximum) and automatically populate the input field, overwriting any existing content. The button will be styled consistently with the "Upload Data" button and positioned separately from the primary "Query" button using space-between layout.

## User Story
As a data analyst or casual user
I want a button that generates example queries based on my uploaded data
So that I can discover interesting insights, understand what types of questions I can ask, and explore my data without needing to think of queries myself

## Problem Statement
Users often don't know what questions to ask about their data, especially when working with unfamiliar datasets. They need inspiration and examples to understand the types of queries they can run. Currently, users must think of their own natural language queries, which can be challenging when first exploring a dataset. This creates a barrier to entry and limits data exploration.

## Solution Statement
Implement a "Generate Query" button that:
1. Analyzes the current database schema (tables, columns, data types, row counts)
2. Uses the existing `llm_processor.py` module to generate contextually relevant natural language queries
3. Populates the query input field with the generated query (always overwriting existing content)
4. Generates interesting queries limited to two sentences maximum
5. Provides variety by generating different queries on each click
6. Is styled as a secondary button matching the "Upload Data" button style
7. Is positioned separately from the primary "Query" button using justify-content: space-between

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains the LLM processing logic; already has `generate_random_query()`, `generate_random_query_with_openai()`, and `generate_random_query_with_anthropic()` functions that generate natural language queries based on database schema
- `app/server/core/data_models.py` - Contains data models; already has `RandomQueryRequest` and `RandomQueryResponse` models for the query generation API
- `app/server/server.py` - Main FastAPI server; already has `/api/generate-query` endpoint that calls `generate_random_query()` from llm_processor
- `app/server/core/sql_processor.py` - Contains `get_database_schema()` function used to retrieve current schema information for query generation
- `app/client/src/main.ts` - Frontend logic; already has `initializeQueryGenerator()` function that handles the Generate Query button click event
- `app/client/src/api/client.ts` - API client configuration; already has `generateRandomQuery()` method for calling the backend endpoint
- `app/client/index.html` - UI elements; already has the Generate Query button in the query controls section
- `app/client/src/style.css` - Styling; already has `.secondary-button` and `.button-group-right` classes for proper button styling and layout
- `.claude/commands/test_e2e.md` - E2E test runner command that executes Playwright tests
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test showing the test format and structure

### New Files
- `.claude/commands/e2e/test_query_generator.md` - E2E test file that validates the query generator button functionality (already exists)
- `app/server/tests/core/test_query_generator.py` - Unit tests for the query generator functionality (to be created)

## Implementation Plan
### Phase 1: Foundation
The foundation consists of backend functionality that generates natural language queries. This includes updating the LLM processor to generate contextually relevant queries based on database schema, creating the data models for request/response handling, and implementing the API endpoint that serves query generation requests.

### Phase 2: Core Implementation
The core implementation focuses on the frontend integration. This includes adding the "Generate Query" button to the UI, implementing the click handler that calls the backend API, populating the input field with generated queries, adding loading states for better UX, and ensuring the button is properly styled and positioned.

### Phase 3: Integration
Integration ensures the feature works end-to-end with proper error handling, testing, and validation. This includes creating unit tests for the backend query generation logic, creating E2E tests to validate the full user flow, handling edge cases (like no tables in database), and ensuring zero regressions in existing functionality.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Review Existing Backend Implementation
- Read `app/server/core/llm_processor.py` to verify `generate_random_query()`, `generate_random_query_with_openai()`, and `generate_random_query_with_anthropic()` functions exist
- Verify these functions generate natural language queries (NOT SQL)
- Verify they limit queries to two sentences maximum
- Verify they use schema information to create contextually relevant queries
- Verify they support both OpenAI and Anthropic providers with proper routing

### Step 2: Review Existing Data Models
- Read `app/server/core/data_models.py` to verify `RandomQueryRequest` and `RandomQueryResponse` models exist
- Verify `RandomQueryRequest` has optional `target_tables` field for targeting specific tables
- Verify `RandomQueryResponse` has `query` field for the generated natural language query
- Verify both models include optional `error` fields for error handling

### Step 3: Review Existing API Endpoint
- Read `app/server/server.py` to verify `/api/generate-query` POST endpoint exists
- Verify it retrieves database schema using `get_database_schema()`
- Verify it calls `generate_random_query()` with schema information
- Verify it returns `RandomQueryResponse` with proper error handling
- Verify it logs success and failure cases appropriately

### Step 4: Review Existing Frontend Button and Layout
- Read `app/client/index.html` to verify "Generate Query" button exists with id `generate-query-button`
- Verify button is in a `.button-group-right` container
- Verify `.query-controls` uses `justify-content: space-between` to separate Query button from Generate Query/Upload Data buttons
- Verify button uses `secondary-button` class for consistent styling

### Step 5: Review Existing Frontend API Client
- Read `app/client/src/api/client.ts` to verify `generateRandomQuery()` method exists
- Verify it calls `/api/generate-query` endpoint with POST method
- Verify it accepts optional `RandomQueryRequest` parameter
- Verify it returns `RandomQueryResponse` with proper typing

### Step 6: Review Existing Frontend Event Handler
- Read `app/client/src/main.ts` to verify `initializeQueryGenerator()` function exists
- Verify it attaches click handler to `generate-query-button`
- Verify it shows loading state (disabled button with spinner and "Generating..." text)
- Verify it calls `api.generateRandomQuery()` to fetch query from backend
- Verify it populates `query-input` field with generated query (overwriting existing content)
- Verify it handles errors by displaying them via `displayError()`
- Verify it focuses the query input after successful generation

### Step 7: Review CSS Styling
- Read `app/client/src/style.css` to verify `.secondary-button` class styling matches "Upload Data" button
- Verify `.button-group-right` creates proper flex layout with gap
- Verify `.query-controls` uses `justify-content: space-between` for proper spacing
- Verify `.loading` spinner animation exists for button loading state

### Step 8: Create Unit Tests for Query Generator
- Create `app/server/tests/core/test_query_generator.py` with comprehensive test coverage
- Test `generate_random_query()` with valid schema (single table)
- Test `generate_random_query()` with multiple tables
- Test `generate_random_query()` with empty schema (returns helpful message)
- Test query length validation (maximum two sentences)
- Test that generated queries are natural language (NOT SQL)
- Test both OpenAI and Anthropic provider routing
- Test error handling when API keys are missing
- Mock LLM API calls to avoid actual API usage in tests

### Step 9: Read E2E Test Documentation
- Read `.claude/commands/test_e2e.md` to understand E2E test runner
- Read `.claude/commands/e2e/test_basic_query.md` to understand test format
- Understand test structure: User Story, Test Steps, Success Criteria
- Understand screenshot requirements and directory structure

### Step 10: Review Existing E2E Test
- Read `.claude/commands/e2e/test_query_generator.md` to verify it tests the complete user flow
- Verify it tests button visibility and styling
- Verify it tests loading states
- Verify it tests query generation with single and multiple tables
- Verify it tests query overwrites existing input
- Verify it tests query variety (different queries on each click)
- Verify it tests error handling when no tables exist
- Verify it tests that generated queries can be executed successfully
- Verify it includes at least 7 screenshots capturing key moments

### Step 11: Manual Testing
- Start the server and client using `./scripts/start.sh`
- Verify "Generate Query" button is visible in the UI
- Verify button is styled with secondary-button class (white background, purple border)
- Verify button is separated from Query button (space-between layout)
- Upload sample data (users.json)
- Click "Generate Query" button
- Verify loading state shows (disabled button with spinner)
- Verify query input field is populated with natural language query
- Verify query is maximum two sentences
- Click "Generate Query" again and verify different query is generated
- Verify new query overwrites previous content
- Execute generated query using "Query" button and verify it works
- Upload additional table (products.csv)
- Generate query again and observe it may reference multiple tables
- Remove all tables and verify appropriate error handling

### Step 12: Run Validation Commands
- Execute all validation commands to ensure the feature works correctly with zero regressions

## Testing Strategy
### Unit Tests
- Test query generation with various database schemas
- Test query length validation (two sentences maximum)
- Test natural language output (NOT SQL)
- Test provider routing (OpenAI vs Anthropic)
- Test schema handling (single table, multiple tables, no tables)
- Test error handling (missing API keys, malformed schema, API failures)
- Mock LLM API calls to ensure tests don't make actual API requests
- Test randomness/variety in generated queries

### Integration Tests
- Test complete flow from button click to query population
- Test API endpoint with various request payloads
- Test error responses and error handling
- Test with real database schema information

### Edge Cases
- No tables in database (should return informative message)
- Single table with minimal columns
- Multiple tables with complex schemas
- Very large database with many tables (ensure performance is acceptable)
- Network failures when calling LLM API
- Invalid or malformed schema data
- Missing API keys for both OpenAI and Anthropic
- Button clicked multiple times in quick succession (rate limiting)
- Generated query exceeds two sentences (validation)
- Generated query is SQL instead of natural language (validation)

## Acceptance Criteria
- "Generate Query" button is visible in the query controls section
- Button is styled consistently with "Upload Data" button (secondary-button class)
- Button is positioned separately from "Query" button using space-between layout
- Clicking button shows loading state (disabled with spinner and "Generating..." text)
- Generated query appears in the query input field
- Generated query is natural language (NOT SQL code)
- Generated query is limited to maximum two sentences
- Generated query is contextually relevant to the database schema
- Each click generates a different/varied query (variety via higher temperature)
- Generated query always overwrites existing content in input field
- Generated queries can be successfully executed using the "Query" button
- Works with single table in database
- Works with multiple tables in database
- Handles no tables scenario gracefully with informative message
- Displays errors appropriately when API calls fail
- Loading state prevents multiple simultaneous generations
- Query input receives focus after successful generation
- All existing functionality continues to work without regression
- E2E test validates complete user flow with screenshots
- Unit tests provide comprehensive coverage of backend logic

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run query generator unit tests
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_query_generator.md` to validate the query generator functionality works end-to-end with visual confirmation via screenshots

## Notes
- The backend implementation already exists and uses `llm_processor.py` with `generate_random_query()` functions
- The frontend implementation already exists with proper button, API client, and event handlers
- The implementation uses higher temperature (0.8) for query generation to ensure variety
- The system prioritizes OpenAI API if both OpenAI and Anthropic keys are available
- Query generation requires at least one table in the database; otherwise returns helpful message
- The button uses the same secondary-button styling as "Upload Data" for visual consistency
- The layout uses `justify-content: space-between` to create clear visual separation between primary action (Query) and secondary actions (Generate Query, Upload Data)
- E2E test file already exists at `.claude/commands/e2e/test_query_generator.md`
- Future enhancements could include:
  - Query history to avoid repeating recent queries
  - Ability to target specific tables via dropdown
  - Query complexity selector (simple, medium, complex)
  - Copy-to-clipboard functionality
  - Query favorites/bookmarking
  - Query templates based on common analytics patterns
