# Feature: Random Query Generator Button

## Feature Description
Create a new button that generates natural language queries based on existing tables and their structure in the database. When clicked, the button generates interesting, contextually-relevant SQL descriptions and automatically populates the query input field with the generated description. The generated query overwrites any existing content in the input field. This feature complements the existing "Random SQL" button and allows users to explore their data through AI-generated query suggestions without writing queries manually.

## User Story
As a data analyst
I want to generate random natural language query suggestions based on my database structure
So that I can easily explore my data and discover interesting insights without having to manually write queries

## Problem Statement
Currently, users must manually write natural language queries to explore their data. While there's a "Random SQL" button that generates random descriptions, users need an additional button with distinct visual prominence to generate interesting query suggestions based on the actual tables they've loaded. Users would benefit from having a dedicated, easily accessible button that generates creative queries tailored to their specific database structure.

## Solution Statement
We will create a new "Generate Query" button (using Upload Data button styling) placed in a visually distinct location from the primary "Query" and "Random SQL" buttons. This button will:

1. Fetch the current database schema via `/api/schema`
2. Call the existing `/api/random-sql` endpoint to generate a natural language query description based on available tables
3. Automatically populate the query input field with the generated description
4. Always overwrite existing content in the input field
5. Provide visual feedback during generation with loading state

The implementation leverages the existing `generate_random_sql_description()` function in `llm_processor.py` and the `/api/random-sql` endpoint already available in the server.

## Relevant Files

### Frontend Files
- **app/client/index.html** - Add new button to the HTML structure
- **app/client/src/main.ts** - Implement button click handler and query population logic
- **app/client/src/style.css** - Ensure button styling follows Upload Data button pattern
- **app/client/src/api/client.ts** - Verify API client has getRandomSQL() method (likely already exists)
- **app/client/src/types.d.ts** - Verify RandomSQLResponse type is defined (likely already exists)

### Backend Files
- **app/server/server.py** - Verify `/api/random-sql` endpoint exists and functions correctly
- **app/server/core/llm_processor.py** - Verify `generate_random_sql_description()` function is working
- **app/server/core/gemini_processor.py** - Verify Gemini API integration for creative query generation
- **app/server/core/data_models.py** - Verify RandomSQLRequest and RandomSQLResponse models exist

### Test Files
- **app/client/src/main.ts** - Update with new button functionality tests
- **app/server/tests/test_random_sql.py** - Verify existing tests cover the random SQL generation

### New Files
- **.claude/commands/e2e/test_random_query_generator.md** - E2E test file for the new feature

## Implementation Plan

### Phase 1: Foundation
- Verify the backend `/api/random-sql` endpoint is properly implemented and functional
- Confirm `generate_random_sql_description()` in `llm_processor.py` works correctly with Gemini API
- Ensure the frontend API client has the `getRandomSQL()` method
- Review existing button styling and layout patterns

### Phase 2: Core Implementation
- Add new "Generate Query" button to HTML (`index.html`)
- Style the button using Upload Data button styling with distinct positioning
- Implement button click handler in `main.ts` that:
  - Validates that tables are loaded
  - Shows loading state
  - Calls the `/api/random-sql` endpoint via API client
  - Populates query input field with generated description (always overwriting)
  - Displays errors if generation fails
  - Restores button state after completion

### Phase 3: Integration
- Ensure the new button integrates seamlessly with existing UI layout
- Verify keyboard shortcuts and focus management work correctly
- Test that generated queries can be executed with the primary "Query" button
- Ensure error handling matches existing patterns in the codebase

## Step by Step Tasks

### Task 1: Research and Verification
- Read `.claude/commands/test_e2e.md` to understand E2E testing patterns
- Read `.claude/commands/e2e/test_basic_query.md` to see example E2E test structure
- Verify `/api/random-sql` endpoint exists in `app/server/server.py`
- Verify `generate_random_sql_description()` function exists and works in `app/server/core/llm_processor.py`
- Verify frontend API client has `getRandomSQL()` method or similar
- Verify RandomSQLResponse type definition exists in `app/client/src/types.d.ts`
- Verify GEMINI_API_KEY is documented in `.env.sample`

### Task 2: Create E2E Test File
- Create `.claude/commands/e2e/test_random_query_generator.md` E2E test file
- Test file should cover:
  - Verifying the button displays correctly
  - Clicking the button generates a query
  - Generated query populates the input field
  - Generated query overwrites existing content
  - Query can be executed successfully
  - Error handling when no tables are loaded
  - Loading state display during generation

### Task 3: Add Generate Query Button to HTML
- Open `app/client/index.html`
- Add new button in the secondary buttons group (after "Random SQL" button)
- Button ID: `generate-query-button`
- Button text: `Generate Query` or `Suggest Query`
- Button class: `secondary-button` (same as Upload Data button)
- Ensure proper spacing and layout in secondary buttons container

### Task 4: Implement Button Click Handler in TypeScript
- Open `app/client/src/main.ts`
- Create new initialization function `initializeGenerateQuery()`
- Call this function from the DOMContentLoaded event listener
- Implement click handler that:
  - Gets reference to query input field
  - Gets schema to check if tables exist
  - Disables button and shows loading state (e.g., "Generating...")
  - Calls `api.getRandomSQL()` endpoint
  - On success: set `queryInput.value` to generated description (overwrites)
  - On error: display error message with `displayError()`
  - Restore button state in finally block
  - Add focus to query input field after population

### Task 5: Verify Styling and Visual Consistency
- Open `app/client/src/style.css`
- Confirm `.secondary-button` styling is applied correctly to new button
- Ensure button follows Upload Data button style pattern
- Verify hover states and disabled states work correctly
- Check responsive behavior on mobile screens

### Task 6: Create Unit Tests
- Create or update test file for the new button functionality
- Test button initialization
- Test API call on button click
- Test query field population with generated description
- Test error handling scenarios
- Test loading state display

### Task 7: Test Backend Endpoint
- Run `cd app/server && uv run pytest tests/test_random_sql.py` to verify backend endpoint works
- Verify `/api/random-sql` endpoint returns valid RandomSQLResponse
- Verify generated descriptions are two sentences maximum as per requirements
- Verify error handling when no tables are available

### Task 8: Execute E2E Test
- Read `.claude/commands/test_e2e.md` instructions
- Execute the `.claude/commands/e2e/test_random_query_generator.md` test file
- Validate all test steps pass
- Document any issues or adjustments needed

### Task 9: Run Full Validation Commands
Execute all validation commands to ensure zero regressions

## Testing Strategy

### Unit Tests
- Test button initialization and DOM element creation
- Test API client call to `/api/random-sql`
- Test query input field population logic
- Test error state handling and error message display
- Test loading state display and button disable/enable functionality
- Test that existing functionality (Query button, Random SQL button) still works

### Edge Cases
- No tables loaded - button should display error message
- API call timeout - should show error and restore button state
- Empty schema response - should handle gracefully
- Very long generated queries - should populate without truncation
- Multiple rapid clicks - should debounce or prevent multiple concurrent requests
- Network errors - should display appropriate error message
- Gemini API unavailable - should display meaningful error

## Acceptance Criteria
1. New "Generate Query" button is visible in the UI next to "Random SQL" button
2. Button styling matches Upload Data button style (white background, blue border)
3. Clicking button generates a query and populates query input field
4. Generated queries always overwrite existing content in input field
5. Button shows loading state (text changes to "Generating...") during API call
6. Generated queries are limited to two sentences maximum
7. Error message displays if no tables are loaded
8. Error message displays if API call fails
9. Button returns to enabled state after success or failure
10. Generated queries can be executed with the primary "Query" button
11. Feature works on all screen sizes (responsive)
12. Keyboard navigation works correctly
13. Existing functionality is not broken (zero regressions)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/test_random_sql.py -v` - Validate backend random SQL generation endpoint
- `cd app/server && uv run pytest` - Run all server tests to ensure zero regressions
- `cd app/client && bun tsc --noEmit` - Verify TypeScript compilation with no errors
- `cd app/client && bun run build` - Verify frontend production build succeeds
- Start the application with `./scripts/start.sh` and manually verify:
  - Button displays correctly
  - Button generates queries when clicked
  - Generated query populates input field
  - Multiple clicks work correctly
  - Errors display appropriately
- Read `.claude/commands/test_e2e.md`, then execute `.claude/commands/e2e/test_random_query_generator.md` E2E test to validate functionality end-to-end

## Notes

### Architecture Notes
- The feature leverages existing backend infrastructure (already has `/api/random-sql` endpoint)
- Uses Gemini API for creative query generation (temperature 0.8 for more variety)
- Follows vanilla TypeScript patterns used in the codebase (not React)
- Uses custom CSS with CSS variables for styling consistency
- Integrates seamlessly with existing DOM-based event handling

### Dependencies
- No new backend dependencies required (Gemini API already integrated via `google-generativeai`)
- Frontend uses only native DOM APIs and existing fetch infrastructure
- Requires GEMINI_API_KEY environment variable to be set

### Future Considerations
- Could add query refinement suggestions after execution
- Could add a history of previously generated queries
- Could add user preferences for query complexity/type
- Could add sharing of interesting queries generated
- Could implement query generation caching to reduce API calls

### Configuration
- Ensure `GEMINI_API_KEY` is set in `.env` file
- Verify Gemini Flash model access is available in your account
- Temperature and token limits are pre-configured in `generate_random_sql_description()`

### Development Tips
- The `/api/random-sql` endpoint already exists and should work with minimal changes
- Review `initializeRandomSQL()` function in `main.ts` as reference for similar button implementation
- Use consistent error handling patterns from existing code
- Test with sample data first before real databases
