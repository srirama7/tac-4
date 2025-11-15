# Feature: Natural Language Query Generator Button

## Feature Description
This feature adds a new button to the Natural Language SQL Interface that generates creative natural language queries based on the existing database tables and their structure. When clicked, the button uses the existing LLM processor to analyze available tables, columns, and data types, then generates an interesting query suggestion (limited to two sentences) and automatically populates the query input field, overwriting any existing content. The button is styled similarly to the "Upload Data" button and positioned separately from the primary "Query" button to maintain clear visual hierarchy.

## User Story
As a user of the Natural Language SQL Interface
I want to click a button that generates interesting natural language query suggestions
So that I can discover insights in my data without having to think of queries myself

## Problem Statement
Users may not know what interesting queries they can ask about their data, especially when first uploading a dataset. Without guidance or examples, users might only ask basic questions and miss opportunities to discover valuable insights. The current interface requires users to come up with queries entirely on their own, which can be challenging when unfamiliar with the data structure or analytical possibilities.

## Solution Statement
We will add a "Generate Query" button that leverages the existing LLM processor (`llm_processor.py`) to analyze the database schema and generate creative, interesting natural language queries. The button will:
1. Fetch the current database schema (tables, columns, data types)
2. Send this information to the LLM with instructions to generate an interesting query
3. Receive a creative query suggestion (maximum 2 sentences)
4. Automatically populate the query input field with this suggestion, overwriting existing content
5. Allow users to either run the query immediately or modify it before execution

The implementation follows existing patterns in the codebase for API communication, error handling, and UI/UX consistency.

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Already contains `generate_query_suggestion()` and related functions that generate natural language query suggestions based on database schema. This is the core LLM logic we'll use.
- `app/server/core/data_models.py` - Already contains `QuerySuggestionRequest` and `QuerySuggestionResponse` models for the API endpoint
- `app/server/server.py` - Already contains the `/api/suggest-query` endpoint (lines 243-282) that handles query suggestion generation
- `app/client/src/main.ts` - Already contains `initializeQueryGenerator()` function (lines 53-80) that handles the button click and populates the input field
- `app/client/index.html` - Already contains the "Generate Query" button HTML (line 24) in the query controls section
- `app/client/src/api/client.ts` - Already contains `generateQuerySuggestion()` API method (lines 80-89) for communicating with the backend
- `app/client/src/types.d.ts` - Contains TypeScript type definitions for API responses
- `app/client/src/style.css` - Contains CSS styles for buttons including `.secondary-button` class used by the Generate Query button

### New Files
- `.claude/commands/e2e/test_query_generator.md` - E2E test file to validate the query generator functionality works end-to-end

## Implementation Plan

### Phase 1: Foundation
The backend foundation is already complete with:
- LLM processor functions (`generate_query_suggestion_with_openai`, `generate_query_suggestion_with_anthropic`)
- Data models (`QuerySuggestionRequest`, `QuerySuggestionResponse`)
- API endpoint (`/api/suggest-query`)
- Unit tests for the query generator (`test_query_generator.py`)

### Phase 2: Core Implementation
The core implementation is already complete with:
- Frontend API client method (`api.generateQuerySuggestion()`)
- UI button in HTML
- Event handler for button clicks
- Logic to populate the query input field

### Phase 3: Integration
The feature is already integrated with:
- Existing database schema endpoint
- LLM provider selection logic
- Error handling and loading states
- UI styling matching the Upload Data button

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Validate Backend Implementation
- Read `app/server/core/llm_processor.py` and verify the `generate_query_suggestion()` function exists and works correctly
- Read `app/server/server.py` and verify the `/api/suggest-query` endpoint is properly implemented
- Read `app/server/core/data_models.py` and verify `QuerySuggestionRequest` and `QuerySuggestionResponse` models are defined

### Validate Frontend Implementation
- Read `app/client/index.html` and verify the "Generate Query" button exists with id `generate-query-button`
- Read `app/client/src/main.ts` and verify the `initializeQueryGenerator()` function is properly implemented and called on DOM load
- Read `app/client/src/api/client.ts` and verify the `generateQuerySuggestion()` API method is implemented
- Read `app/client/src/types.d.ts` and verify type definitions for `QuerySuggestionRequest` and `QuerySuggestionResponse` exist

### Validate Unit Tests
- Read `app/server/tests/core/test_query_generator.py` and verify unit tests exist for the query generator functionality
- Run the unit tests to ensure they pass: `cd app/server && uv run pytest tests/core/test_query_generator.py -v`

### Create E2E Test
- Read `.claude/commands/test_e2e.md` to understand the E2E test framework and structure
- Read `.claude/commands/e2e/test_basic_query.md` to understand the E2E test format and see an example
- Create a new E2E test file `.claude/commands/e2e/test_query_generator.md` that validates:
  - The "Generate Query" button is visible and clickable
  - Clicking the button shows a loading state
  - The query input field is populated with a generated query (non-empty)
  - The generated query is different from any placeholder text
  - The generated query is 2 sentences or less
  - Error handling works when no tables are uploaded
  - Screenshots are captured at key steps

### Run Validation Commands
- Execute all validation commands listed in the "Validation Commands" section to ensure zero regressions

## Testing Strategy

### Unit Tests
- **Test query suggestion generation with OpenAI**: Verify that `generate_query_suggestion_with_openai()` returns a non-empty query suggestion when given valid schema information
- **Test query suggestion generation with Anthropic**: Verify that `generate_query_suggestion_with_anthropic()` returns a non-empty query suggestion when given valid schema information
- **Test query suggestion routing**: Verify that `generate_query_suggestion()` correctly routes to OpenAI or Anthropic based on available API keys
- **Test error handling**: Verify appropriate error messages when API keys are missing or API calls fail
- **Test query length validation**: Verify generated queries are limited to approximately 2 sentences

### Edge Cases
- **No tables in database**: Should return an error message asking user to upload data first
- **Empty schema**: Should handle gracefully and inform user to add data
- **API key not configured**: Should return appropriate error message indicating which API key is needed
- **Network/API failures**: Should handle timeouts and API errors gracefully with user-friendly messages
- **Rapid button clicks**: Button should be disabled during processing to prevent duplicate requests
- **Multiple tables with complex relationships**: Should generate queries that showcase interesting cross-table insights
- **Single table with limited columns**: Should still generate creative queries within the constraints

## Acceptance Criteria
- [ ] "Generate Query" button is visible in the UI, styled as a secondary button, positioned between "Query" and "Upload Data" buttons
- [ ] Clicking the button fetches database schema from `/api/schema` endpoint
- [ ] Button sends schema to `/api/suggest-query` endpoint with appropriate LLM provider
- [ ] Button shows loading state (spinner) while generating query
- [ ] Generated query appears in the query input field, overwriting existing content
- [ ] Generated query is limited to 2 sentences maximum
- [ ] Generated query is creative and interesting (not generic like "show me all data")
- [ ] Error handling displays user-friendly messages when:
  - No tables are uploaded in the database
  - API keys are not configured
  - LLM API calls fail
- [ ] Button is disabled during query generation to prevent duplicate requests
- [ ] Query input field receives focus after query is populated
- [ ] Unit tests pass for all query generator functions
- [ ] E2E test validates the complete user flow with screenshots
- [ ] All existing tests continue to pass (zero regressions)
- [ ] Frontend build completes without TypeScript errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md` to understand how to run E2E tests
- Read and execute the new E2E test file `.claude/commands/e2e/test_query_generator.md` to validate this functionality works end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Implementation Already Complete
This feature has been fully implemented in the codebase. All backend and frontend components are in place:
- Backend LLM functions exist and are tested
- API endpoint is implemented
- Frontend button, event handlers, and API integration are complete
- The implementation follows existing code patterns and conventions

### Tasks Focus on Validation
The tasks in this plan focus on:
1. Validating that all components are properly implemented
2. Creating comprehensive E2E tests
3. Ensuring zero regressions

### LLM Provider Flexibility
The implementation supports both OpenAI and Anthropic LLM providers, with automatic routing based on available API keys (OpenAI has priority if both keys are present).

### Query Quality
The LLM prompts are designed to generate:
- Creative, interesting queries (not generic)
- Queries that showcase insights, patterns, trends, or relationships
- Maximum 2 sentences
- Natural language that users can understand and potentially modify

### Button Styling
The "Generate Query" button uses the `.secondary-button` CSS class, matching the "Upload Data" button style for visual consistency. The buttons are arranged with `justify-content: space-between` to create clear separation from the primary "Query" button.

### Future Enhancements
Potential future improvements could include:
- Multiple query suggestions for users to choose from
- Query history/favorites
- Category-based suggestions (aggregations, filters, joins, etc.)
- Difficulty levels (simple, intermediate, advanced)
- Learning from user's query patterns to personalize suggestions
