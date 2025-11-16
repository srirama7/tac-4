# Feature: Natural Language Query Generator Button

## Feature Description
Add a new "Generate Query" button to the Natural Language SQL Interface that automatically generates interesting natural language queries based on the existing database tables and their structure. The button will use the LLM processor to create contextually relevant queries (limited to two sentences) and populate them into the query input field, overwriting any existing content. This feature enables users to explore their data through suggested queries without having to think of questions themselves.

## User Story
As a user of the Natural Language SQL Interface
I want a button that generates interesting natural language queries based on my uploaded tables
So that I can quickly explore my data without having to think of queries myself and learn what kinds of questions I can ask

## Problem Statement
Users who upload data to the Natural Language SQL Interface may not immediately know what questions to ask or what insights their data can provide. This creates friction in the user experience, especially for new users who are unfamiliar with their dataset's structure or capabilities. Users need inspiration and examples of meaningful queries they can run against their data.

## Solution Statement
Implement a "Generate Query" button that leverages the existing `llm_processor.py` module to analyze the current database schema (tables and columns) and generate contextually relevant, interesting natural language queries. The generated query will be automatically populated into the query input field, ready for the user to execute. The button will be styled consistently with the "Upload Data" button and positioned with space-between alignment in the query controls section.

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` (lines 1-228) - Contains the LLM integration functions that will be used to generate natural language queries based on schema information. We'll add a new function `generate_natural_language_query()` that uses the existing LLM providers (OpenAI, Anthropic, or Gemini) to create interesting queries.

- `app/server/core/data_models.py` (lines 1-82) - Contains Pydantic models for API requests/responses. We'll add new models `GenerateQueryRequest` and `GenerateQueryResponse` to handle the query generation endpoint.

- `app/server/server.py` (lines 1-280) - The FastAPI server that defines API endpoints. We'll add a new `POST /api/generate-query` endpoint that accepts the current schema and returns a generated natural language query.

- `app/client/src/api/client.ts` (lines 1-79) - API client configuration for frontend. We'll add a new `generateQuery()` method to call the generate-query endpoint.

- `app/client/src/types.d.ts` (lines 1-80) - TypeScript type definitions. We'll add interfaces `GenerateQueryRequest` and `GenerateQueryResponse` to match the backend models.

- `app/client/src/main.ts` (lines 1-423) - Main frontend application logic. We'll add the button initialization, event handler, and query population logic.

- `app/client/index.html` (lines 1-99) - HTML structure. We'll add the "Generate Query" button to the query-controls section (around line 23-25).

- `app/client/src/style.css` - CSS styling (need to check this file to understand button styling patterns and add styles for the generate query button).

### New Files

- `.claude/commands/e2e/test_query_generator.md` - E2E test file that validates the query generator button functionality, including button presence, click behavior, query population, and execution of generated queries.

- `app/server/tests/core/test_query_generator.py` - Unit tests for the query generation functionality, testing various schema configurations and LLM provider responses.

## Implementation Plan

### Phase 1: Foundation
Set up the backend infrastructure for query generation by creating the data models, adding the LLM processor function, and establishing the API endpoint. This phase ensures that the server can accept requests to generate queries and return meaningful natural language questions based on the current database schema.

### Phase 2: Core Implementation
Implement the frontend button, API client integration, and query population logic. This phase makes the feature visible and interactive for users, allowing them to click the button and see generated queries appear in the input field.

### Phase 3: Integration
Create comprehensive tests (unit and E2E) to validate the feature works correctly across different scenarios, schema configurations, and LLM providers. Ensure zero regressions by running all existing tests and validating the new functionality end-to-end.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Backend Data Models
- Read `app/server/core/data_models.py` to understand the existing model patterns
- Add `GenerateQueryRequest` model with no required fields (empty request body is acceptable since we get schema from database)
- Add `GenerateQueryResponse` model with fields: `query` (str), `tables_used` (List[str]), `error` (Optional[str])
- Ensure the models follow the same pattern as existing models (use Pydantic BaseModel, proper typing, optional error field)

### 2. Backend LLM Processor Function
- Read `app/server/core/llm_processor.py` to understand existing LLM integration patterns
- Add function `generate_natural_language_query(schema_info: Dict[str, Any], llm_provider: str = None) -> str`
- Create a prompt that instructs the LLM to generate an interesting, exploratory natural language query (max 2 sentences) based on the provided schema
- The prompt should encourage queries that:
  - Demonstrate interesting insights (aggregations, filtering, comparisons)
  - Use realistic business questions
  - Leverage multiple tables when available (with JOINs)
  - Vary in complexity (sometimes simple, sometimes complex)
- Implement the function to route to the appropriate LLM provider (same pattern as `generate_sql()`)
- Add provider-specific implementations: `generate_query_with_openai()`, `generate_query_with_anthropic()`, `generate_query_with_gemini()`
- Clean up any markdown formatting from LLM responses (remove ```text or similar)
- Return the generated query as a plain string

### 3. Backend API Endpoint
- Read `app/server/server.py` to understand endpoint patterns
- Add `POST /api/generate-query` endpoint with response model `GenerateQueryResponse`
- In the endpoint handler:
  - Get the current database schema using `get_database_schema()`
  - Check if there are any tables available (return error if schema is empty)
  - Call `generate_natural_language_query()` with the schema
  - Extract which tables are mentioned in the query (or default to all tables)
  - Return `GenerateQueryResponse` with the query and tables_used
- Add proper error handling and logging (follow existing patterns in `server.py`)
- Ensure the endpoint follows security best practices (no user input to sanitize since we're generating the query)

### 4. Backend Unit Tests
- Create `app/server/tests/core/test_query_generator.py`
- Add test for `generate_natural_language_query()` with mock schema:
  - Test with single table schema
  - Test with multiple tables schema
  - Test with empty schema (should raise error)
  - Test query length constraint (must be <= 2 sentences)
- Mock the LLM provider responses to avoid API calls during testing
- Follow the testing patterns from `app/server/tests/core/test_llm_processor.py`
- Run tests to ensure they pass: `cd app/server && uv run pytest tests/core/test_query_generator.py -v`

### 5. Frontend Type Definitions
- Read `app/client/src/types.d.ts` to understand existing type patterns
- Add `GenerateQueryRequest` interface (empty object or with optional provider field)
- Add `GenerateQueryResponse` interface matching the backend model: `query: string; tables_used: string[]; error?: string;`
- Ensure types match exactly with Pydantic models

### 6. Frontend API Client
- Read `app/client/src/api/client.ts` to understand API method patterns
- Add `generateQuery()` method to the `api` object
- Method should make a POST request to `/generate-query` endpoint
- Return type should be `Promise<GenerateQueryResponse>`
- Follow the same error handling pattern as other API methods

### 7. Frontend HTML Structure
- Read `app/client/index.html` and `app/client/src/style.css` to understand button styling
- Add a new button in the `query-controls` div (around line 23)
- Button HTML: `<button id="generate-query-button" class="secondary-button">Generate Query</button>`
- Position the button between the "Query" button and "Upload Data" button
- Ensure the flex layout uses `justify-content: space-between` or similar to space buttons apart

### 8. Frontend Button Logic
- Read `app/client/src/main.ts` to understand initialization patterns
- Create function `initializeGenerateQuery()` that:
  - Gets reference to `#generate-query-button`
  - Gets reference to `#query-input` textarea
  - Adds click event listener
- In the click handler:
  - Disable button and show loading state (spinner)
  - Call `api.generateQuery()`
  - On success: populate `queryInput.value` with the generated query (overwrite existing content)
  - On error: display error using existing `displayError()` function
  - Re-enable button and remove loading state
- Call `initializeGenerateQuery()` in the DOMContentLoaded event listener
- Add keyboard shortcut support if desired (optional enhancement)

### 9. Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand E2E test runner requirements
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_complex_query.md` for examples
- Create `.claude/commands/e2e/test_query_generator.md` with:
  - User Story describing the query generator feature
  - Test Steps that:
    1. Navigate to application URL
    2. Take screenshot of initial state
    3. Verify "Generate Query" button is present
    4. Click "Generate Query" button
    5. Take screenshot showing loading state
    6. Verify query input field is populated with generated text
    7. Take screenshot of populated query
    8. Verify generated query is not empty and <= 2 sentences
    9. Click "Query" button to execute the generated query
    10. Verify results appear (proving the generated query is valid)
    11. Take screenshot of results
  - Success Criteria listing all validation points
  - Specify 4-5 screenshots to be taken

### 10. CSS Styling (if needed)
- Read `app/client/src/style.css` to check if secondary-button class exists and is styled appropriately
- If needed, ensure the button has proper spacing in the query-controls flex container
- Verify the button style matches the "Upload Data" button aesthetic
- Test responsive behavior if applicable

### 11. Integration Testing
- Start the server and client: `./scripts/start.sh`
- Manually test the feature:
  - Verify button appears in the UI
  - Upload sample data (users.json)
  - Click "Generate Query" button
  - Verify query appears in input field
  - Click "Query" button to execute
  - Verify results appear
  - Test with multiple tables uploaded
  - Test with no tables (should show appropriate error)
- Stop the services when done

### 12. Run Validation Commands
- Execute all validation commands listed in the "Validation Commands" section below
- Ensure zero errors and zero regressions
- Fix any issues that arise before considering the feature complete

## Testing Strategy

### Unit Tests
- **Backend Tests** (`app/server/tests/core/test_query_generator.py`):
  - Test `generate_natural_language_query()` with various schema configurations
  - Mock LLM responses to test parsing logic
  - Test error handling for empty schemas
  - Test query length validation (must be <= 2 sentences)
  - Test that generated queries reference actual table/column names from schema

- **API Endpoint Tests** (can be added to existing server tests):
  - Test `/api/generate-query` endpoint returns valid response
  - Test endpoint with no tables in database
  - Test endpoint with single table
  - Test endpoint with multiple tables

### Edge Cases
- **No tables in database**: Should return an error message like "No tables available. Please upload data first."
- **Very large schema (many tables/columns)**: Should still generate a focused query without exceeding LLM token limits
- **LLM returns overly long query**: Should truncate or regenerate to meet 2-sentence limit
- **LLM API failure**: Should return user-friendly error message
- **Malformed LLM response**: Should handle gracefully and either retry or return error
- **Multiple rapid button clicks**: Button should be disabled during generation to prevent duplicate requests
- **Query input already has content**: Should overwrite (as specified in requirements)

## Acceptance Criteria
- [ ] "Generate Query" button is visible in the query controls section
- [ ] Button is styled consistently with "Upload Data" button (secondary-button class)
- [ ] Button is positioned with space-between alignment from primary buttons
- [ ] Clicking the button triggers a loading state (button disabled with spinner)
- [ ] Generated query appears in the query input field within reasonable time (<5 seconds)
- [ ] Generated query overwrites any existing content in the input field
- [ ] Generated query is limited to a maximum of two sentences
- [ ] Generated queries are contextually relevant to the uploaded table schemas
- [ ] Generated queries reference actual table and column names from the database
- [ ] Generated queries vary in complexity (aggregations, filters, joins when applicable)
- [ ] Error handling works when no tables are available
- [ ] Error handling works when LLM API fails
- [ ] All existing tests pass with zero regressions
- [ ] E2E test validates the feature works end-to-end
- [ ] Feature works with all three LLM providers (OpenAI, Anthropic, Gemini)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run query generator unit tests
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/client && bun run tsc --noEmit` - Run TypeScript type checking to validate zero type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature compiles correctly
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_query_generator.md` E2E test to validate the button appears, generates queries, and integrates properly

## Notes

### LLM Provider Priority
The feature should respect the same LLM provider priority as the existing query processing:
1. Gemini (if `GEMINI_API_KEY` exists)
2. OpenAI (if `OPENAI_API_KEY` exists)
3. Anthropic (if `ANTHROPIC_API_KEY` exists)

### Query Generation Prompt Guidelines
The prompt for generating queries should:
- Instruct the LLM to create realistic, business-oriented questions
- Encourage variety (different types of queries each time)
- Use proper table and column names from the schema
- Avoid overly technical or complex SQL concepts in the natural language
- Keep the query under 2 sentences (explicitly state this constraint)
- Generate queries that would yield meaningful results (not edge cases)

### Example Generated Queries
Based on a users table:
- "Show me all users who signed up in the last 30 days"
- "What are the top 5 most common email domains in the users table?"

Based on products and orders tables:
- "Which products have been ordered more than 10 times this month?"
- "Show the total revenue by product category"

### Future Enhancements
Consider these enhancements for future iterations:
- Add a "surprise me" mode that generates random queries periodically
- Allow users to regenerate if they don't like the suggestion
- Show a history of generated queries for reference
- Add keyboard shortcut (e.g., Cmd+G) to trigger generation
- Provide multiple query suggestions at once
- Learn from user behavior to generate more relevant queries over time

### Security Considerations
- No user input is processed in the generation flow (only schema metadata)
- Generated queries still go through the same SQL injection protection when executed
- LLM API keys should remain secure in environment variables
- Rate limiting may be needed if users spam the generate button (future consideration)

### Dependencies
No new dependencies are required. The feature uses:
- Existing LLM integrations (`openai`, `anthropic`, `google.generativeai`)
- Existing FastAPI and Pydantic infrastructure
- Existing frontend fetch API and TypeScript setup
