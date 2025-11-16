# Feature: Natural Language Query Generator Button

## Feature Description
Add an interactive button to the Natural Language SQL Interface that generates interesting natural language query suggestions based on the existing database tables and their structure. When clicked, the button will use LLM services to create contextually relevant, creative query suggestions that demonstrate the capabilities of the database. These generated queries will automatically populate the input field, replacing any existing content, allowing users to execute them manually. The button will be positioned separately from the primary action buttons and styled similarly to the "Upload Data" button for visual consistency.

## User Story
As a user of the Natural Language SQL Interface
I want to click a button that generates interesting natural language queries based on my data
So that I can quickly explore my database without having to think of queries myself and learn what kinds of questions I can ask

## Problem Statement
Users who upload data to the Natural Language SQL Interface may not immediately know what queries to run or how to phrase them effectively. This creates a barrier to entry and reduces the value users get from the application. Users need inspiration and examples of well-formed natural language queries that are relevant to their specific data schema, helping them understand both the capabilities of the system and the structure of their data.

## Solution Statement
Implement a "Generate Query" button that:
1. Analyzes the current database schema (tables, columns, and row counts)
2. Uses the existing LLM integration (llm_processor.py) to generate creative, contextually-relevant natural language queries
3. Generates concise queries (maximum two sentences) that are interesting and demonstrate various query capabilities
4. Automatically populates the query input field with the generated query, overwriting any existing content
5. Provides visual feedback during generation (loading state)
6. Is styled consistently with the "Upload Data" button and positioned with proper spacing from primary buttons
7. Intelligently uses available LLM providers with the same priority system as query processing

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains LLM integration functions for OpenAI and Anthropic that will be extended to include query suggestion generation
- `app/server/server.py` - FastAPI server where a new endpoint will be added to handle query generation requests
- `app/server/core/data_models.py` - Contains Pydantic models where new request/response models for query generation will be defined
- `app/server/core/sql_processor.py` - Contains `get_database_schema()` function that provides schema information needed for query generation
- `app/client/src/main.ts` - Frontend logic where the new button functionality and API call will be implemented
- `app/client/index.html` - HTML structure where the new "Generate Query" button will be added to the UI
- `app/client/src/api/client.ts` - API client where the new endpoint method will be added
- `app/client/src/types.d.ts` - TypeScript type definitions where new types for the query generation API will be defined
- `app/client/src/style.css` - Styling file where button styles will be applied for visual consistency

### New Files
- `app/server/core/query_generator.py` - New module containing the core query suggestion generation logic
- `app/server/tests/core/test_query_generator.py` - Unit tests for the query generation functionality
- `.claude/commands/e2e/test_query_generator.md` - E2E test specification for validating the query generator button works end-to-end

## Implementation Plan
### Phase 1: Foundation
Create the backend infrastructure for query generation by adding a new query_generator module with LLM integration. This includes defining the API models, creating the core generation logic that analyzes database schemas, and building prompts that instruct the LLM to generate interesting, context-aware natural language queries. The foundation will reuse existing LLM provider patterns and ensure consistent behavior with the existing query processing system.

### Phase 2: Core Implementation
Implement the backend API endpoint that receives schema information and returns generated query suggestions. Create comprehensive unit tests to validate the generation logic works correctly with various schema configurations. Implement error handling, loading states, and LLM provider fallback logic. Ensure the query generation respects the two-sentence maximum constraint and generates diverse, interesting queries.

### Phase 3: Integration
Integrate the query generation functionality into the frontend by adding the "Generate Query" button to the UI, implementing the click handler that calls the API, and updating the input field with the generated query. Style the button consistently with existing UI patterns, position it appropriately with justified spacing, and add visual feedback during generation. Create an E2E test to validate the complete user flow from button click to query population.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Backend Data Models
- Add `QuerySuggestionRequest` model to `app/server/core/data_models.py`
  - Should include optional schema information
  - Include provider preference similar to QueryRequest
- Add `QuerySuggestionResponse` model
  - Include suggested query text (max 2 sentences)
  - Include error field for error handling
  - Include provider used for transparency
- Update TypeScript types in `app/client/src/types.d.ts` to match

### Step 2: Implement Query Generation Logic
- Create `app/server/core/query_generator.py` module
- Implement `generate_query_suggestion(schema_info, llm_provider)` function
  - Format schema information for LLM prompt
  - Create prompt that instructs LLM to generate interesting queries
  - Specify constraints: max 2 sentences, natural language, contextually relevant
  - Include variety in query types (filters, aggregations, joins, date ranges, etc.)
- Implement `generate_query_with_openai()` helper function
  - Use OpenAI API to generate query suggestions
  - Use gpt-4.1-mini model for cost efficiency
  - Set temperature to 0.7 for creativity
  - Handle API errors gracefully
- Implement `generate_query_with_anthropic()` helper function
  - Use Anthropic API to generate query suggestions
  - Use claude-3-haiku model for cost efficiency
  - Set temperature to 0.7 for creativity
  - Handle API errors gracefully
- Implement `generate_query_with_gemini()` helper function
  - Use Google Gemini API to generate query suggestions
  - Use gemini-1.5-flash model for cost efficiency
  - Set temperature to 0.7 for creativity
  - Handle API errors gracefully
  - Add GEMINI_API_KEY environment variable support
- Implement provider routing logic with priority: Gemini > OpenAI > Anthropic
  - Check for GEMINI_API_KEY first (highest priority)
  - Fall back to OPENAI_API_KEY if Gemini unavailable
  - Fall back to ANTHROPIC_API_KEY if both unavailable
  - Use request preference as final fallback

### Step 3: Create Backend API Endpoint
- Add `/api/query-suggestion` POST endpoint to `app/server/server.py`
  - Accept QuerySuggestionRequest
  - Call `get_database_schema()` to get current schema
  - Call `generate_query_suggestion()` with schema and provider preference
  - Return QuerySuggestionResponse with generated query
  - Handle errors and return appropriate error messages
  - Add logging for successful generation and errors

### Step 4: Write Backend Unit Tests
- Create `app/server/tests/core/test_query_generator.py`
- Test query generation with OpenAI (mocked API calls)
- Test query generation with Anthropic (mocked API calls)
- Test query generation with Gemini (mocked API calls)
- Test provider priority logic (Gemini > OpenAI > Anthropic)
- Test schema formatting for prompt
- Test error handling when API calls fail
- Test error handling when no API keys are available
- Test two-sentence constraint is communicated in prompt
- Test with single table schema
- Test with multiple table schema
- Test with empty schema (no tables)

### Step 5: Add Frontend API Client Method
- Update `app/client/src/api/client.ts`
- Add `generateQuerySuggestion()` method
  - Call POST `/api/query-suggestion`
  - Handle response and errors
  - Return QuerySuggestionResponse

### Step 6: Add Generate Query Button to UI
- Update `app/client/index.html`
- Add "Generate Query" button in the query-controls section
  - Position it with justify-content: space-between or similar to create spacing
  - Use class "secondary-button" to match "Upload Data" button style
  - Add id "generate-query-button" for JavaScript binding
  - Place button between "Query" and "Upload Data" buttons with proper spacing

### Step 7: Implement Frontend Button Functionality
- Update `app/client/src/main.ts`
- Add `initializeQueryGenerator()` function
  - Get button element by id
  - Add click event listener
  - Show loading state (disable button, show loading spinner)
  - Call API to get query suggestion
  - Populate input field with generated query (overwrite existing content)
  - Handle errors with user-friendly messages
  - Reset button state after completion
- Call `initializeQueryGenerator()` in DOMContentLoaded event

### Step 8: Add Visual Feedback and Styling
- Update button styles to match "Upload Data" button
- Add loading spinner/state during query generation
- Add hover effects consistent with other buttons
- Ensure proper spacing using CSS flexbox justify-apart or gap
- Add disabled state styling
- Ensure responsive design for mobile devices

### Step 9: Create E2E Test Specification
- Create `.claude/commands/e2e/test_query_generator.md`
- Define test steps:
  1. Navigate to application URL
  2. Upload sample data (users.json)
  3. Take screenshot of initial state
  4. Verify "Generate Query" button is visible
  5. Click "Generate Query" button
  6. Verify button shows loading state
  7. Wait for query to be generated
  8. Verify query input field is populated with text
  9. Take screenshot of generated query
  10. Verify query is max 2 sentences
  11. Click "Query" button to execute generated query
  12. Verify results appear
  13. Take screenshot of results
  14. Click "Generate Query" again
  15. Verify new query is different from previous
  16. Take screenshot of new generated query
- Define success criteria:
  - Button is visible and styled correctly
  - Clicking generates a query
  - Query is natural language (not SQL)
  - Query is contextually relevant to schema
  - Query is maximum 2 sentences
  - Query overwrites existing input field content
  - Loading state is shown during generation
  - Generated queries can be executed successfully
  - Multiple generations produce varied queries

### Step 10: Update Environment Configuration Documentation
- Update `.env.sample` in `app/server/` to include GEMINI_API_KEY
- Add comment explaining Gemini API key is optional but has highest priority
- Document the provider priority system: Gemini > OpenAI > Anthropic

### Step 11: Run Validation Commands
- Execute all validation commands listed below
- Fix any test failures or errors
- Ensure zero regressions in existing functionality

## Testing Strategy
### Unit Tests
- Test query generation with different schema configurations:
  - Single table with few columns
  - Multiple tables with relationships
  - Tables with various data types
  - Empty schema (no tables)
- Test LLM provider routing and priority logic
- Test error handling for API failures
- Test prompt construction and schema formatting
- Test response parsing and validation
- Mock all LLM API calls to avoid actual API usage in tests
- Test that generated queries include variety (aggregations, filters, joins, date queries)

### Integration Tests
- Test complete flow from API endpoint to response
- Test frontend button click to API call to input population
- Test error handling when backend is unavailable
- Test loading states and UI feedback

### Edge Cases
- No tables in database (empty schema)
- Very large schema with many tables and columns
- Schema with special characters in table/column names
- API rate limiting or timeout
- All API keys missing (no provider available)
- Network errors during API call
- Malformed API responses
- Very long table or column names
- Tables with no rows

## Acceptance Criteria
- A "Generate Query" button is visible in the UI, styled like the "Upload Data" button
- Button is positioned with proper spacing (justify-apart) from other buttons
- Clicking the button generates a contextually-relevant natural language query based on current database schema
- Generated queries are limited to two sentences maximum
- Query automatically populates the input field, overwriting any existing content
- Button shows loading state during generation (disabled with spinner)
- Error messages are displayed if generation fails
- Generated queries can be successfully executed to retrieve results
- Multiple clicks generate varied, interesting queries
- Feature works with OpenAI, Anthropic, and Gemini LLM providers
- Provider priority follows: Gemini (highest) > OpenAI > Anthropic
- All existing functionality continues to work without regression
- E2E test validates the complete user flow
- Unit tests achieve high coverage of generation logic

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test file `.claude/commands/e2e/test_query_generator.md` to validate this functionality works.

- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run query generator unit tests
- `cd app/server && uv run pytest tests/ -v` - Run all server tests to ensure no regressions
- `cd app/server && uv run python -m py_compile server.py main.py core/*.py` - Validate Python syntax
- `cd app/server && uv run ruff check .` - Run linting to catch code quality issues
- `cd app/client && bun tsc --noEmit` - Run TypeScript type checking
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes
- Use Gemini API as the highest priority provider for query generation to demonstrate multi-provider support
  - Install `google-generativeai` Python package using `uv add google-generativeai`
  - Use environment variable `GEMINI_API_KEY` for API authentication
  - Use `gemini-1.5-flash` model for cost-effective generation
  - Priority order: Gemini > OpenAI > Anthropic (based on API key availability)
- Set temperature to 0.7 for query generation to encourage creative, varied suggestions
- Use existing `get_database_schema()` function to get schema information
- Reuse existing LLM client patterns from `llm_processor.py`
- Generated queries should showcase different query types: filters, aggregations, sorting, date ranges, joins (when multiple tables), etc.
- Consider adding randomness/variety to prevent repetitive suggestions
- Button should be disabled when there are no tables in the database
- Generated queries should be natural language, NOT SQL
- Keep prompts concise but ensure they communicate the two-sentence constraint clearly
- Consider user experience: fast response times, clear loading states, helpful error messages
- The query generator should work offline gracefully (show error if no API key available)
- Future enhancement: Allow users to specify query complexity or focus area
