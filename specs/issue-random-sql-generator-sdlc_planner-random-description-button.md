# Feature: Random SQL Description Generator Button

## Feature Description
Add a new button to the Natural Language SQL Interface that generates random SQL descriptions based on the loaded database tables. When clicked, this button will use the Gemini LLM to create interesting and contextually relevant SQL query descriptions and automatically populate the query input field with the generated text. This feature helps users explore different types of queries they can ask about their data by providing inspiration through AI-generated natural language descriptions.

## User Story
As a user
I want a button that generates random SQL descriptions based on my loaded tables
So that I can get inspired with different types of queries I can ask about my data without having to think of questions from scratch

## Problem Statement
Users often lack inspiration when starting to query their data. They may load data into the application but not know what questions are worth asking or what patterns they could explore. This friction in the discovery process can lead to underutilization of the application and reduced user engagement.

## Solution Statement
Implement a "Random SQL" button that:
1. Analyzes the current database schema (tables and their column structures)
2. Uses the Gemini LLM to generate random, contextually relevant natural language SQL descriptions
3. Creates descriptions that are practical and demonstrate real-world query patterns
4. Automatically populates the query input field with the generated description
5. Follows the existing UI patterns (secondary-button style) and is positioned logically next to the Upload Data button
6. Provides clear feedback during generation with a loading state

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains LLM integration logic that will be extended to support Gemini API for generating random SQL descriptions
- `app/server/core/sql_processor.py` - Contains `get_database_schema()` function that provides table and column information
- `app/server/server.py` - FastAPI server where we'll add a new endpoint `/api/random-sql` to handle random SQL description generation requests
- `app/server/core/data_models.py` - Data models where we'll add request/response models for the new endpoint
- `app/client/src/main.ts` - Frontend TypeScript code where we'll add button click handler and API call logic
- `app/client/index.html` - HTML structure where we'll add the new "Random SQL" button
- `app/client/src/style.css` - CSS styling to ensure button consistency and positioning
- `app/client/src/api/client.ts` - API client where we'll add the new endpoint function
- `app/client/src/types.d.ts` - TypeScript type definitions where we'll add types for the new API

### New Files
- `.claude/commands/e2e/test_random_sql.md` - E2E test file to validate the random SQL generation feature works correctly
- `app/server/tests/test_random_sql.py` - Unit tests for the random SQL generation endpoint
- `app/server/core/gemini_processor.py` - Gemini-specific LLM processing module for query generation

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for random SQL description generation. This includes adding Gemini API integration, new API endpoint, data models, and LLM processing functions that analyze database schema and generate contextually relevant random SQL descriptions using Gemini 2.5 Flash.

### Phase 2: Core Implementation
Implement the frontend button and integration logic. Add the "Random SQL" button to the UI with proper styling and positioning, connect it to the backend API, and ensure it properly populates the query input field with the generated SQL descriptions.

### Phase 3: Integration
Add comprehensive testing (unit tests and E2E tests), ensure error handling works correctly, and validate the feature integrates seamlessly with existing LLM functionality without causing regressions.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Gemini LLM Processor Module
- Create new file `app/server/core/gemini_processor.py`
- Import required modules: `os`, `google.generativeai as genai`, `typing`
- Add function `generate_with_gemini(prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str`
- Configure Gemini API with `GEMINI_API_KEY` environment variable
- Use Gemini 2.5 Flash model (`gemini-2.5-flash`) as default
- Include proper error handling with descriptive error messages
- Return only the generated text (clean up any markdown or extra formatting)
- Add logging for debugging and monitoring

### Step 2: Add Gemini Query Generation Function
- Open `app/server/core/llm_processor.py`
- Add `generate_random_sql_description(schema_info: str, llm_provider: str = "gemini") -> str` function
- Create a prompt that instructs the LLM to generate an interesting random SQL description based on the provided tables and columns
- Specify in the prompt:
  - Generate practical, real-world query scenarios
  - Descriptions should be 1-3 sentences maximum
  - Make them specific to the actual data structure provided
  - Include query patterns like filtering, aggregation, sorting, joining
  - Vary the complexity and type of queries
- Route to Gemini API (or fallback to existing providers if Gemini is unavailable)
- Return only the generated description text
- Add comprehensive error handling with descriptive messages

### Step 3: Add Data Models for Random SQL Generation
- Open `app/server/core/data_models.py`
- Add `RandomSQLRequest` model with optional `llm_provider` field (defaults to "gemini")
- Add `RandomSQLResponse` model with `description` (string), `tables_analyzed` (list of strings), and optional `error` field
- Follow existing patterns in the file for consistency
- Add docstrings for clarity

### Step 4: Create API Endpoint for Random SQL Generation
- Open `app/server/server.py`
- Import the new data models and functions from `gemini_processor` and `llm_processor`
- Add new `POST /api/random-sql` endpoint
- Response model should be `RandomSQLResponse`
- Endpoint should:
  - Get database schema using `get_database_schema()`
  - Check if tables exist (return error if none)
  - Call `generate_random_sql_description()` function
  - Return the result with list of analyzed tables
  - Handle all errors gracefully with descriptive messages
- Follow existing endpoint patterns (error handling, logging, try-catch structure)
- Log successful generation with INFO level
- Add request validation and timeout handling

### Step 5: Add Frontend API Client Function
- Open `app/client/src/api/client.ts`
- Add `getRandomSQL()` function that calls `POST /api/random-sql`
- Follow existing patterns in the file (error handling, fetch configuration)
- Return the response data with proper typing
- Include timeout logic for long-running requests
- Add descriptive error messages for different failure scenarios

### Step 6: Add TypeScript Type Definitions
- Open `app/client/src/types.d.ts`
- Add `RandomSQLResponse` interface matching the backend model
- Include properties: `description: string`, `tables_analyzed: string[]`, `error?: string`
- Ensure it's available globally through module augmentation if needed

### Step 7: Add "Random SQL" Button to UI
- Open `app/client/index.html`
- Locate the query controls section (contains Query button and Upload Data button)
- Add new button with:
  - id: `random-sql-button`
  - class: `secondary-button`
  - text: "Random SQL"
- Ensure proper spacing and alignment with other buttons
- Position: Query button on left, Random SQL and Upload Data buttons on right with appropriate spacing

### Step 8: Implement Button Click Handler
- Open `app/client/src/main.ts`
- Add `initializeRandomSQL()` function
- Get reference to the random SQL button and query input field
- On button click:
  - Check if tables are loaded (show warning if not)
  - Disable button and show loading state (change text to "Generating..." or show spinner)
  - Call `api.getRandomSQL()`
  - Populate query input field with generated description (overwriting existing content)
  - Handle errors by displaying user-friendly error messages
  - Re-enable button after completion (success or failure)
- Add proper error handling and user feedback
- Call `initializeRandomSQL()` in the DOMContentLoaded event listener

### Step 9: Implement Loading State UI
- Update `app/client/src/style.css` to add loading state styling for the button
- Add visual feedback like:
  - Cursor change to "not-allowed" when disabled
  - Opacity reduction when disabled
  - Optional spinner animation
- Ensure button text updates to "Generating..." during API call
- Restore original text after completion

### Step 10: Add Unit Tests
- Create `app/server/tests/test_random_sql.py`
- Test successful random SQL description generation with mock schema
- Test error handling when no tables exist
- Test error handling when LLM API (Gemini) fails
- Test error handling when Gemini API key is not configured
- Test that description is not empty and has reasonable length
- Mock LLM API calls to avoid actual API usage during tests
- Test fallback behavior if Gemini is unavailable
- Follow existing test patterns in the test directory
- Aim for 100% code coverage of new functions

### Step 11: Create E2E Test Specification
- Create `.claude/commands/e2e/test_random_sql.md`
- Follow the format from `.claude/commands/e2e/test_basic_query.md` and `test_generate_query.md`
- Include User Story section
- Include detailed Test Steps:
  - Navigate to application
  - Verify "Random SQL" button is visible and enabled
  - Upload sample data (users.json or similar)
  - Click "Random SQL" button
  - Verify button shows loading state (text changes to "Generating...")
  - Verify query input field is populated with a random SQL description
  - Verify description is 1-3 sentences maximum
  - Verify error handling works (test by clicking without data loaded)
  - Take screenshots at key points
- Include Success Criteria section
- Include expected button behavior and timeout handling

### Step 12: Run Validation Commands
- Execute all validation commands listed in the Validation Commands section
- Ensure zero errors and zero regressions
- Verify Gemini API integration is working correctly
- Fix any issues that arise before marking the feature complete
- Verify all tests pass with appropriate coverage

### Step 13: Update Documentation
- Update `adws/README.md` to mention the random SQL feature (if applicable)
- Add comments to new code explaining complex logic
- Update any relevant API documentation
- Ensure all code follows project standards and conventions

## Testing Strategy

### Unit Tests
- Test random SQL endpoint with valid schema (multiple tables)
- Test random SQL endpoint with single table
- Test random SQL endpoint with empty database (no tables loaded)
- Test Gemini API integration with valid credentials
- Test Gemini API error handling (invalid key, API timeout, rate limiting)
- Test error handling for missing environment variables
- Verify generated descriptions are not empty
- Verify descriptions have reasonable length (not too short, not too long)
- Mock Gemini API calls to ensure tests run without external dependencies
- Test response structure matches `RandomSQLResponse` model

### Frontend Tests
- Test button element exists and is correctly styled
- Test button click triggers API call
- Test button shows loading state during API call
- Test query input field is populated with response
- Test error messages display when API fails
- Test button re-enables after API call completes
- Test that clicking multiple times rapidly is handled gracefully

### Edge Cases
- No tables loaded in database (should show error message)
- Gemini API key not configured (should return appropriate error)
- Network timeout when calling Gemini API (should handle gracefully with timeout)
- User clicks Random SQL button multiple times rapidly (should prevent multiple simultaneous requests)
- Generated description is empty or malformed (should handle and show error)
- Query input field already has text (should overwrite completely)
- Database has tables with unusual characters or names (should handle gracefully)
- Very large database schema (should still generate relevant descriptions)

## Acceptance Criteria
- A "Random SQL" button is visible in the UI next to the Upload Data button
- Button follows the secondary-button styling and matches existing buttons
- Button is positioned with proper spacing on the right side of the query controls
- Clicking the button shows a clear loading state (disabled state, text change, visual feedback)
- After successful generation, the query input field is populated with a random SQL description
- Generated description is practical and contextually relevant to the tables
- Description length is between 1-3 sentences (reasonable for user exploration)
- Any existing text in the query input field is completely overwritten
- If no tables are loaded, an appropriate error message is displayed to the user
- Button re-enables after generation completes (success or failure)
- Random SQL generation uses Gemini 2.5 Flash LLM model
- Descriptions vary on each click (truly random generation)
- Error messages are user-friendly and actionable
- All existing functionality continues to work without regression
- Unit tests pass with 100% coverage of new code paths
- E2E test validates the feature works end-to-end
- Gemini API integration is secure (API key from environment, not hardcoded)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/test_random_sql.py -v` - Run new unit tests for random SQL endpoint
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript type checking
- `cd app/client && bun run build` - Run frontend build to validate the feature compiles correctly
- `cd app && uv run python -m pytest` - Run all tests including server tests
- Verify `GEMINI_API_KEY` is set: `echo $GEMINI_API_KEY` (should not be empty)
- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test file `.claude/commands/e2e/test_random_sql.md` to validate the random SQL generation feature works end-to-end

## Notes
- The random SQL descriptions should be practical and demonstrate real-world use cases (e.g., "Show me all users who signed up in the last 30 days" or "What are the top 10 products by total inventory value?")
- Descriptions should vary in type and complexity to showcase different query patterns:
  - Filtering queries (WHERE clauses)
  - Aggregation queries (COUNT, SUM, AVG, etc.)
  - Sorting queries (ORDER BY)
  - Time-based queries (dates, timestamps)
  - Multi-table queries (JOINs) when appropriate
- The Gemini LLM prompt should encourage practical, real-world scenarios that users would actually want to explore
- Generated descriptions should reference actual column names and table structures from the loaded data
- Error messages should be user-friendly: "Please upload data first" instead of technical error details
- The loading state should provide clear visual feedback that generation is in progress
- Consider the user experience: fast generation, clear feedback, helpful error messages
- The feature should be resilient to Gemini API failures and provide graceful degradation
- Future enhancement ideas:
  - Allow users to customize query complexity (simple, medium, advanced)
  - Add ability to regenerate if user doesn't like the suggestion
  - Show explanation of what the query would return
  - Track which random queries are useful to improve suggestions
  - Add query categories (e.g., "Show me aggregations" vs "Show me recent data")
