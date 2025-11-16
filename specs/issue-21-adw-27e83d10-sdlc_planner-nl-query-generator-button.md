# Feature: Natural Language Query Generator Button

## Feature Description
Add a "Generate Query" button that uses LLM processing to automatically generate interesting natural language queries based on the existing database schema (tables and their structures). When clicked, the button will generate a creative, contextual query suggestion (maximum 2 sentences) and populate it directly into the query input field, overwriting any existing content. This feature helps users discover what kinds of questions they can ask about their data and demonstrates the power of the natural language SQL interface.

## User Story
As a user
I want to automatically generate interesting query suggestions based on my uploaded data
So that I can discover what kinds of questions I can ask and get inspiration for exploring my database without having to think of queries myself

## Problem Statement
Users who upload data to the Natural Language SQL Interface may not immediately know what kinds of questions they can ask about their data. This creates friction in the user experience and reduces engagement with the application. Users need inspiration and examples of meaningful queries they can run against their specific database schema to fully leverage the natural language interface capabilities.

## Solution Statement
Implement a "Generate Query" button positioned alongside the existing "Upload Data" button that, when clicked, analyzes the current database schema (tables, columns, row counts) and uses LLM processing to generate contextually relevant, interesting natural language query suggestions. The generated query will automatically populate the query input field, replacing any existing content, allowing users to immediately execute it or modify it as needed. This provides users with instant inspiration and demonstrates practical use cases for their specific data.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - FastAPI server with existing endpoint implementations; need to verify the `/api/generate-query-suggestion` endpoint is properly registered (already exists in git status)
- `app/server/core/data_models.py` - Pydantic models for request/response validation; contains `QuerySuggestionRequest` and `QuerySuggestionResponse` models (already updated per git status)
- `app/server/core/query_generator.py` - Core query suggestion generation logic using OpenAI, Anthropic, and Gemini APIs; implements routing logic and schema formatting (already exists per git status)
- `app/client/index.html` - Frontend HTML structure; already contains the "Generate Query" button UI element (already updated per git status)
- `app/client/src/main.ts` - Frontend TypeScript logic; already includes event handler for the Generate Query button (already updated per git status)
- `app/client/src/api/client.ts` - API client methods; already includes `generateQuerySuggestion()` method (already updated per git status)
- `app/client/src/types.d.ts` - TypeScript type definitions; already includes `QuerySuggestionRequest` and `QuerySuggestionResponse` types (already updated per git status)
- `app/client/src/style.css` - CSS styling for the UI; already includes styling for secondary buttons including Generate Query button (already updated per git status)
- `app/server/core/llm_processor.py` - Reference for LLM integration patterns (OpenAI, Anthropic) to ensure consistency

### New Files

- `app/server/tests/core/test_query_generator.py` - Unit tests for query generation functionality (already exists per git status)
- `.claude/commands/e2e/test_query_generator.md` - E2E test specification for the query generator feature (already exists per git status)

## Implementation Plan

### Phase 1: Foundation
The backend API endpoint `/api/generate-query-suggestion` has already been implemented in `app/server/server.py` (lines 244-286). The endpoint uses the `generate_query_suggestion()` function from `app/server/core/query_generator.py` which:
- Validates that the database has tables with data
- Routes to appropriate LLM provider (Gemini priority, then OpenAI, then Anthropic)
- Formats the schema information for the LLM prompt
- Generates a natural language query suggestion (max 2 sentences)
- Returns the suggestion with the list of tables analyzed

The data models (`QuerySuggestionRequest`, `QuerySuggestionResponse`) are already defined in `app/server/core/data_models.py` and match the TypeScript type definitions in `app/client/src/types.d.ts`.

### Phase 2: Core Implementation
The frontend implementation has already been completed:
- The "Generate Query" button exists in `app/client/index.html` (line 25) with the ID `generate-query-button`
- The button is styled as a secondary button and positioned in the `.secondary-buttons` flex container alongside "Upload Data"
- The event handler in `app/client/src/main.ts` (lines 46-69) handles the click event, calls the API, and populates the query input field
- The API client method exists in `app/client/src/api/client.ts` (lines 81-89)
- TypeScript types are defined in `app/client/src/types.d.ts` (lines 83-91)

### Phase 3: Integration
The feature is already integrated into the existing application flow:
- The button appears on page load alongside existing UI controls
- It uses the existing database schema retrieval mechanism
- Error handling follows the existing pattern (displaying errors using `displayError()`)
- Loading states are implemented (button shows spinner during generation)
- The generated query can be immediately executed using the existing query processing flow

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Review and validate existing implementation
- Read and verify all modified files match the feature requirements
- Verify the backend endpoint `/api/generate-query-suggestion` is correctly implemented
- Verify the `query_generator.py` module properly generates suggestions with OpenAI, Anthropic, and Gemini
- Verify the frontend button exists and is properly styled
- Verify the TypeScript event handler properly calls the API and populates the input field
- Verify error handling for edge cases (empty database, no API keys configured)

### Create comprehensive unit tests
- Read the existing test file at `app/server/tests/core/test_query_generator.py`
- Verify tests cover all three LLM providers (OpenAI, Anthropic, Gemini)
- Verify tests cover schema formatting
- Verify tests cover error cases (empty schema, missing API keys)
- Verify tests cover the routing logic (Gemini priority)
- Add any missing test cases as needed

### Create E2E test specification
- Read `.claude/commands/test_e2e.md` to understand E2E test format and requirements
- Read `.claude/commands/e2e/test_basic_query.md` as an example of E2E test structure
- Read the existing E2E test file at `.claude/commands/e2e/test_query_generator.md`
- Verify the E2E test covers:
  - Loading the application
  - Uploading sample data
  - Clicking the "Generate Query" button
  - Verifying the query input field is populated
  - Verifying the generated query is contextual and relevant to the uploaded data
  - Executing the generated query to verify it works
  - Taking screenshots at key steps
- Update the E2E test if any steps are missing or incorrect

### Manual testing and validation
- Start the backend server (`cd app/server && uv run python server.py`)
- Start the frontend dev server (`cd app/client && bun run dev`)
- Upload sample data (users, products, or events)
- Click the "Generate Query" button multiple times to verify variety in suggestions
- Verify the button shows a loading spinner during generation
- Verify the generated query populates the input field and overwrites existing content
- Verify clicking "Query" after generation executes successfully
- Test error cases:
  - Click "Generate Query" with no data uploaded (should show error message)
  - Test with missing API keys (should show appropriate error)
- Verify button styling matches the "Upload Data" button (secondary button style)
- Test on different browsers if possible

### Run validation commands
- Execute all commands in the "Validation Commands" section to ensure zero regressions
- Fix any failing tests or build errors
- Verify E2E test passes

## Testing Strategy

### Unit Tests
- **Test query generation with OpenAI**: Verify `generate_query_suggestion_with_openai()` calls OpenAI API with correct schema format and returns a valid query suggestion
- **Test query generation with Anthropic**: Verify `generate_query_suggestion_with_anthropic()` calls Anthropic API with correct schema format and returns a valid query suggestion
- **Test query generation with Gemini**: Verify `generate_query_suggestion_with_gemini()` calls Gemini API with correct schema format and returns a valid query suggestion
- **Test schema formatting**: Verify `format_schema_for_suggestion_prompt()` correctly formats table names, columns, types, and row counts
- **Test routing logic**: Verify `generate_query_suggestion()` routes to Gemini first, then OpenAI, then Anthropic based on API key availability
- **Test empty database validation**: Verify appropriate error is raised when schema has no tables
- **Test missing API key validation**: Verify appropriate error is raised when no LLM API keys are configured
- **Test quote removal**: Verify generated queries have surrounding quotes removed
- **Test prompt construction**: Verify the LLM prompt includes the 2-sentence limit rule and focuses on interesting queries

### Edge Cases
- **Empty database**: User clicks "Generate Query" before uploading any data - should return error message "Database is empty. Please upload data first."
- **No API keys configured**: No OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY in environment - should return error "No LLM API keys configured"
- **API timeout or failure**: LLM API call fails or times out - should return error message with details
- **Multiple tables**: Database has multiple tables with different schemas - should generate queries that may involve joins or focus on the most interesting table
- **Single table**: Database has only one table - should generate focused queries on that table's columns
- **Tables with minimal data**: Tables exist but have 0 or very few rows - should still generate valid query suggestions
- **Very long query response**: LLM returns query longer than 2 sentences - should still accept and display it (validation is in prompt, not code)
- **Rapid button clicks**: User clicks "Generate Query" multiple times quickly - button should be disabled during processing to prevent race conditions
- **Query field has existing content**: User has typed a query, then clicks "Generate Query" - existing content should be overwritten completely

## Acceptance Criteria
- [ ] "Generate Query" button appears in the UI alongside the "Upload Data" button with matching secondary button styling
- [ ] Button is positioned using `justify-content: space-between` to separate it from the primary "Query" button
- [ ] Clicking the button shows a loading spinner and disables the button until generation completes
- [ ] Generated query appears in the query input field, overwriting any existing content
- [ ] Generated queries are contextually relevant to the actual database schema (mention actual table/column names)
- [ ] Generated queries are maximum 2 sentences long
- [ ] Query suggestions are interesting and demonstrate practical use cases (not trivial like "show all records")
- [ ] Multiple clicks generate different queries (variety through LLM temperature=0.7)
- [ ] Error handling works for empty database (shows: "Database is empty. Please upload data first.")
- [ ] Error handling works for missing API keys (shows: "No LLM API keys configured. Please set GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY.")
- [ ] Generated queries can be executed successfully using the existing "Query" button
- [ ] Feature works with all three LLM providers (OpenAI, Anthropic, Gemini)
- [ ] LLM routing prioritizes Gemini, then OpenAI, then Anthropic (Gemini is recommended for SQL)
- [ ] All unit tests pass with good coverage (>80%)
- [ ] E2E test validates the complete user flow with screenshots
- [ ] Frontend build completes without TypeScript errors
- [ ] Backend server starts without errors
- [ ] No regressions in existing functionality (all existing tests still pass)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the E2E test file `.claude/commands/e2e/test_query_generator.md` to validate the query generator functionality works end-to-end with visual proof via screenshots
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run query generator unit tests to validate core functionality
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun run tsc --noEmit` - Run frontend TypeScript checks to validate type safety
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Implementation Status
Based on the git status, the following files have already been modified:
- Backend: `app/server/server.py`, `app/server/core/data_models.py`, `app/server/core/query_generator.py`
- Frontend: `app/client/index.html`, `app/client/src/main.ts`, `app/client/src/api/client.ts`, `app/client/src/types.d.ts`, `app/client/src/style.css`
- Tests: `app/server/tests/core/test_query_generator.py` (new)
- E2E: `.claude/commands/e2e/test_query_generator.md` (new)

This suggests the feature has already been partially or fully implemented. The tasks above focus on **validation, testing, and ensuring quality** rather than initial implementation.

### LLM Provider Configuration
The query generator supports three LLM providers with the following priority:
1. **Gemini** (recommended for SQL operations) - Uses `gemini-pro` model
2. **OpenAI** - Uses `gpt-4.1-mini` model
3. **Anthropic** - Uses `claude-3-haiku-20240307` model

Set the appropriate API key in `app/server/.env`:
```bash
GEMINI_API_KEY=your_key_here
# OR
OPENAI_API_KEY=your_key_here
# OR
ANTHROPIC_API_KEY=your_key_here
```

### Prompt Engineering
The LLM prompt includes specific rules to generate high-quality query suggestions:
- Maximum 2 sentences
- Natural, conversational language
- Relevant to actual columns and tables
- Focus on practical, insightful queries
- Consider both single-table and join queries for multiple tables
- Avoid overly simple queries like "show all records"
- Demonstrate the power of natural language querying

Temperature is set to 0.7 (higher than SQL generation which uses 0.1) to encourage creative and varied suggestions.

### UI/UX Considerations
- The "Generate Query" button uses the `.secondary-button` class to match the "Upload Data" button styling
- Both secondary buttons are contained in a `.secondary-buttons` flex container
- The query input field maintains focus after population for immediate editing if desired
- Loading states prevent multiple simultaneous API calls
- Error messages are displayed in the same location as query results for consistency

### Future Enhancements
Consider for future iterations:
- Add a "favorites" feature to save generated queries users like
- Implement query history to track previously generated suggestions
- Add filters/preferences for query types (analytical, aggregation, filtering, joins, etc.)
- Generate multiple suggestions and let users choose from a dropdown
- Add explanations of why each query is interesting or what insights it might reveal
- Support for more LLM providers (e.g., Google PaLM, Cohere)
