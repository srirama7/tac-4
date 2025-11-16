# Feature: Natural Language Query Generator Button

## Feature Description
Add a new button to the application that automatically generates interesting natural language queries based on the existing database tables and their structure. When clicked, the button will use LLM capabilities to create contextually relevant queries (limited to two sentences) that demonstrate what questions users can ask about their data. The generated query will populate the main query input field, overwriting any existing content, allowing users to execute it manually.

## User Story
As a user
I want to see example queries generated based on my actual data structure
So that I can better understand what questions I can ask and how to phrase them naturally

## Problem Statement
New users often struggle to formulate effective natural language queries because they don't know what types of questions work well or how to phrase them. Without examples specific to their uploaded data, users may not fully leverage the natural language SQL interface capabilities. The application currently lacks a discovery mechanism to help users explore their data through example queries.

## Solution Statement
Implement a "Generate Query" button positioned alongside existing action buttons that analyzes the current database schema (tables, columns, row counts) and uses the existing LLM processor infrastructure to create contextually relevant, interesting natural language queries. The generated query will immediately populate the input field, replacing any existing content, giving users immediate examples they can execute or modify. The button will be styled consistently with the "Upload Data" button and positioned with space-between justification to maintain visual balance.

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains the LLM integration functions (OpenAI and Anthropic) that will be extended to support query generation based on schema information
- `app/server/core/data_models.py` - Defines Pydantic models for API requests/responses; will need a new model for query suggestion requests/responses
- `app/server/server.py` - FastAPI server with API endpoints; will need a new endpoint `/api/generate-query-suggestion` to handle query generation requests
- `app/server/core/sql_processor.py` - Contains the `get_database_schema()` function that retrieves table and column information needed for query generation
- `app/client/index.html` - Main HTML structure where the new "Generate Query" button will be added to the query controls section
- `app/client/src/main.ts` - TypeScript client code where button click handler and API integration will be implemented
- `app/client/src/api/client.ts` - API client module where the new query suggestion endpoint will be added
- `app/client/src/types.d.ts` - TypeScript type definitions where the query suggestion response type will be defined
- `app/client/src/style.css` - CSS styles where the new button styling will be defined to match the "Upload Data" button

### New Files

- `app/server/core/query_generator.py` - New module containing the core logic for generating natural language query suggestions based on database schema
- `app/server/tests/core/test_query_generator.py` - Unit tests for the query generator module
- `.claude/commands/e2e/test_query_generator.md` - E2E test file to validate the query generator feature works end-to-end

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for query generation by implementing a new core module that analyzes database schema and uses LLM capabilities to generate interesting, contextually relevant natural language queries. This includes defining data models for the request/response cycle and implementing the core generation logic with proper error handling.

### Phase 2: Core Implementation
Build the API endpoint that exposes the query generation functionality and integrate it into the existing FastAPI server. Implement the frontend button component with proper styling and event handling, connecting it to the new API endpoint. Ensure the generated query properly populates the input field with content replacement.

### Phase 3: Integration
Connect the frontend and backend components, ensuring proper error handling, loading states, and user feedback. Validate that the feature works seamlessly with the existing query execution flow. Create comprehensive E2E tests that validate the entire user journey from clicking the button to executing the generated query.

## Step by Step Tasks

### Task 1: Create Backend Query Generator Module
- Create `app/server/core/query_generator.py` with a function `generate_query_suggestion(schema_info: Dict[str, Any], llm_provider: str = "openai") -> str`
- The function should analyze the schema to understand table structures, column types, and relationships
- Use the existing `generate_sql_with_openai()` or `generate_sql_with_anthropic()` from `llm_processor.py` with a specialized prompt
- The prompt should instruct the LLM to create interesting natural language questions (max 2 sentences) that users might want to ask
- Handle edge cases: empty database, single table, multiple tables, different column types
- Implement proper error handling and logging

### Task 2: Define Data Models
- Add new Pydantic models to `app/server/core/data_models.py`:
  - `QuerySuggestionRequest` with optional `llm_provider` field (defaults to "openai")
  - `QuerySuggestionResponse` with fields: `query` (str), `tables_analyzed` (List[str]), `error` (Optional[str])
- Ensure models follow existing patterns and include proper field descriptions

### Task 3: Create API Endpoint
- Add a new POST endpoint `/api/generate-query-suggestion` to `app/server/server.py`
- The endpoint should:
  - Get the current database schema using `get_database_schema()`
  - Call `generate_query_suggestion()` from the new module
  - Return the generated query in a `QuerySuggestionResponse` model
  - Handle errors gracefully and return them in the response
- Add appropriate logging for debugging and monitoring

### Task 4: Write Backend Unit Tests
- Create `app/server/tests/core/test_query_generator.py`
- Test cases should include:
  - Generating queries with single table schema
  - Generating queries with multiple tables
  - Handling empty database (no tables)
  - Testing both OpenAI and Anthropic providers
  - Error handling for invalid schemas
  - Verify generated queries are limited to 2 sentences
- Use mocking for LLM API calls to avoid actual API usage in tests

### Task 5: Add Frontend TypeScript Types
- Add `QuerySuggestionResponse` interface to `app/client/src/types.d.ts`:
  - `query: string`
  - `tables_analyzed: string[]`
  - `error?: string`

### Task 6: Create API Client Method
- Add `generateQuerySuggestion()` method to `app/client/src/api/client.ts`
- The method should POST to `/api/generate-query-suggestion` and return `QuerySuggestionResponse`
- Follow existing patterns for error handling and response parsing

### Task 7: Add UI Button Element
- Add a new button to `app/client/index.html` in the `.query-controls` section
- Button properties:
  - `id="generate-query-button"`
  - `class="secondary-button"`
  - Text: "Generate Query"
- Position the button using CSS flexbox with `justify-content: space-between` to create visual separation from primary buttons
- The layout should have the "Query" button on one side and "Generate Query" + "Upload Data" buttons grouped on the other side

### Task 8: Style the Generate Query Button
- Add CSS styles to `app/client/src/style.css` for the generate query button
- The button should match the "Upload Data" button styling (secondary-button class)
- Add hover and active states for better UX
- Ensure the button is responsive and works well on mobile devices
- Update `.query-controls` to use flexbox with `justify-content: space-between` for proper spacing

### Task 9: Implement Button Click Handler
- Add click event listener in `app/client/src/main.ts` function `initializeQueryInput()`
- When clicked:
  - Disable the button and show loading state (spinner)
  - Call `api.generateQuerySuggestion()`
  - On success: populate the query input field with the generated query, overwriting existing content
  - On error: display an error message using the existing `displayError()` function
  - Re-enable the button when complete
- Show visual feedback during the generation process

### Task 10: Create E2E Test File
- Create `.claude/commands/e2e/test_query_generator.md` following the format of `test_basic_query.md`
- Test steps should include:
  1. Navigate to the application
  2. Upload sample data (users.json)
  3. Verify the "Generate Query" button is present
  4. Click the "Generate Query" button
  5. Verify the query input field is populated with generated text
  6. Verify the generated query is 2 sentences or less
  7. Click the "Query" button to execute the generated query
  8. Verify the query executes successfully and returns results
  9. Take screenshots at key steps
- Success criteria: Button works, query is generated, query executes successfully

### Task 11: Run Validation Commands
- Execute all validation commands to ensure the feature works correctly with zero regressions
- Run backend tests: `cd app/server && uv run pytest`
- Run frontend TypeScript check: `cd app/client && bun tsc --noEmit`
- Run frontend build: `cd app/client && bun run build`
- Read `.claude/commands/test_e2e.md`, then execute the new E2E test: `.claude/commands/e2e/test_query_generator.md`
- Fix any issues discovered during validation

## Testing Strategy

### Unit Tests
- **Query Generator Module Tests** (`test_query_generator.py`):
  - Test `generate_query_suggestion()` with various schema configurations:
    - Single table with basic columns (id, name, email)
    - Multiple tables with different column types (integers, text, dates)
    - Empty database (should handle gracefully)
    - Tables with many columns (20+)
  - Test both OpenAI and Anthropic provider routing
  - Mock LLM API calls to ensure tests run without actual API usage
  - Verify output format: 2 sentences maximum, natural language, relevant to schema
  - Test error handling: API failures, invalid schemas, timeout scenarios

- **API Endpoint Tests**:
  - Test `/api/generate-query-suggestion` endpoint response format
  - Verify proper error responses when schema is empty
  - Test with different database states

- **Frontend Integration Tests**:
  - Test button click handler functionality
  - Test API client method `generateQuerySuggestion()`
  - Verify input field population and content replacement
  - Test loading states and error display

### Edge Cases
- **Empty Database**: No tables uploaded - should return a friendly error or prompt to upload data
- **Single Table**: Should generate relevant queries for that single table
- **Multiple Tables**: Should generate queries that potentially use JOIN operations or focus on interesting single-table queries
- **Large Schemas**: Tables with 50+ columns - ensure the LLM prompt doesn't exceed token limits
- **API Failures**: LLM API is down or returns errors - should display user-friendly error message
- **Concurrent Requests**: User clicks button multiple times rapidly - should handle gracefully with debouncing
- **No API Keys**: Neither OpenAI nor Anthropic keys configured - should return helpful error message
- **Very Long Table Names**: Should truncate gracefully in prompts
- **Special Characters in Column Names**: Should handle columns with spaces, underscores, etc.
- **Network Timeout**: Slow LLM response - should have reasonable timeout and error handling

## Acceptance Criteria
- A new "Generate Query" button appears in the UI alongside the "Upload Data" button with proper spacing
- The button is styled consistently with secondary buttons (matching "Upload Data" style)
- Clicking the button triggers LLM-based query generation using the existing `llm_processor.py` infrastructure
- Generated queries are contextually relevant to the current database schema (tables and columns)
- Generated queries are limited to 2 sentences maximum as specified
- The generated query populates the main query input field, overwriting any existing content
- Users can immediately execute the generated query using the existing "Query" button
- The button shows loading state (spinner) while generating the query
- Appropriate error messages are shown if query generation fails
- The feature works with both OpenAI and Anthropic LLM providers
- All existing tests continue to pass (zero regressions)
- New unit tests for the query generator module pass
- E2E test validates the complete user flow works correctly
- Frontend TypeScript compilation succeeds without errors
- Frontend build succeeds without errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run ruff check .` - Run backend linting to ensure code quality
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run query generator unit tests
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript check to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_query_generator.md` to validate the complete user flow works end-to-end

## Notes

### LLM Provider Routing
- Follow the existing pattern in `llm_processor.py` where OpenAI takes priority if the API key is available, then Anthropic
- The query generation should use the same routing logic: `generate_sql()` function pattern
- Users can optionally specify a preferred provider in the request

### Query Generation Prompt Design
The prompt for generating queries should:
- Analyze the schema structure: table names, column names, column types, row counts
- Generate queries that showcase interesting data exploration patterns
- Prefer queries that demonstrate the natural language capabilities (e.g., "Show me users who signed up in the last month" rather than "Select all users")
- For multiple tables, occasionally suggest queries that would use JOINs
- Vary the complexity based on schema richness (simple queries for simple schemas, more complex for rich schemas)
- Example prompt structure:
  ```
  Given the following database schema:
  [schema details]

  Generate an interesting natural language question that a user might want to ask about this data.

  Rules:
  - Maximum 2 sentences
  - Use natural, conversational language
  - Make it relevant to the actual columns and tables present
  - Focus on practical, insightful queries
  - For multiple tables, consider both single-table and join queries

  Natural language query:
  ```

### UI/UX Considerations
- The button should be non-intrusive but easily discoverable
- Loading states are important since LLM calls can take 1-3 seconds
- Error messages should guide users (e.g., "Please upload data first" if no tables exist)
- Consider adding a tooltip: "Generate example query based on your data"
- The button should be disabled during query generation to prevent multiple concurrent requests

### Future Enhancements (Not in Scope)
- Generate multiple query suggestions and let users choose
- Save query history for users to revisit interesting queries
- Add a "Surprise Me" mode that executes the query automatically
- Implement query templates based on common patterns
- Add analytics to track which generated queries are most useful

### Performance Considerations
- LLM API calls are the bottleneck (~1-3 seconds)
- Consider caching generated queries for the same schema to improve perceived performance
- Timeout should be set to ~10 seconds to handle slow API responses
- The schema passed to LLM should be formatted concisely to minimize token usage

### Security Considerations
- All generated queries will go through the existing SQL security validation before execution
- No user input is involved in the generation (schema comes from database)
- LLM output should be treated as untrusted and not executed automatically
- Follow existing patterns in `sql_security.py` for identifier validation
