# Feature: Random Query Generator Button

## Feature Description
This feature adds a new button to the Natural Language SQL Interface that generates interesting natural language queries based on the existing database tables and their structure. When clicked, the button uses the LLM processor to create contextually relevant queries that demonstrate the capabilities of the application. The generated query automatically populates (overwrites) the input field, allowing users to execute it manually. This feature helps users understand what types of questions they can ask and provides inspiration for exploring their data.

## User Story
As a user of the Natural Language SQL Interface
I want a button that generates example queries based on my uploaded tables
So that I can learn what types of questions to ask and discover insights in my data without having to think of queries from scratch

## Problem Statement
Users often struggle with understanding what types of natural language queries they can ask when first using the application. The empty query input field can be intimidating, and users may not know the best way to phrase their questions to get meaningful results. This creates a barrier to entry and reduces the application's usability, especially for new users who are unfamiliar with the capabilities of natural language-to-SQL conversion.

## Solution Statement
Implement a "Generate Query" button positioned separately from the primary query controls that leverages the existing LLM processor to create contextually aware, interesting queries based on the current database schema. The button will analyze available tables and their structures, then generate a natural language query (limited to two sentences) that demonstrates realistic use cases. This generated query will overwrite the current input field content, allowing users to immediately execute it and see results. The button will use the same styling as the "Upload Data" button for visual consistency.

## Relevant Files
Use these files to implement the feature:

- **app/server/core/llm_processor.py** - Contains LLM integration logic for OpenAI and Anthropic; will be extended with a new `generate_random_query()` function that creates natural language queries based on table schemas
- **app/server/server.py** - FastAPI server with existing API endpoints; will add a new `/api/generate-query` endpoint to handle query generation requests
- **app/server/core/data_models.py** - Pydantic models for request/response validation; will add `QueryGenerationRequest` and `QueryGenerationResponse` models
- **app/client/src/main.ts** - Main TypeScript file handling UI interactions; will add button event handler and API call for query generation
- **app/client/src/api/client.ts** - API client for backend communication; will add `generateQuery()` method
- **app/client/index.html** - Main HTML structure; will add the new "Generate Query" button in the query controls section
- **app/client/src/style.css** - Stylesheet for UI components; may need minor adjustments for button positioning
- **app/client/src/types.d.ts** - TypeScript type definitions; will add interfaces for query generation request/response

### New Files
- **.claude/commands/e2e/test_query_generator.md** - E2E test file to validate the query generator button functionality works correctly by clicking the button, verifying a query is generated, and executing it to ensure it produces valid results

## Implementation Plan

### Phase 1: Foundation
First, establish the backend infrastructure by adding the necessary data models and LLM processing logic. This includes creating Pydantic models for the query generation request/response and implementing a new function in the LLM processor that analyzes database schemas and generates contextually relevant natural language queries. The LLM will be prompted to create interesting, realistic queries that showcase the types of questions users can ask based on their specific table structures.

### Phase 2: Core Implementation
Implement the API endpoint in the FastAPI server that accepts requests for query generation and returns generated queries. Then, add the frontend UI components including the "Generate Query" button with appropriate styling, and implement the client-side logic to call the API and populate the input field with the generated query. The button will be positioned using CSS flexbox with `justify-content: space-between` to separate it from the primary "Query" button.

### Phase 3: Integration
Connect all components by ensuring the frontend button correctly calls the backend API, handles loading states, and properly overwrites the query input field. Add comprehensive error handling for cases where no tables exist or the LLM fails to generate a query. Create E2E tests to validate the complete workflow from button click to query generation to execution, ensuring the feature works seamlessly with the existing application.

## Step by Step Tasks

### 1. Add Backend Data Models
- Open `app/server/core/data_models.py`
- Add a new `QueryGenerationRequest` Pydantic model with no required fields (empty request)
- Add a new `QueryGenerationResponse` Pydantic model with fields:
  - `query: str` - The generated natural language query
  - `tables_analyzed: List[str]` - List of table names used to generate the query
  - `error: Optional[str] = None` - Error message if generation fails

### 2. Implement Query Generation Logic in LLM Processor
- Open `app/server/core/llm_processor.py`
- Create a new function `generate_random_query(schema_info: Dict[str, Any]) -> str` that:
  - Analyzes the database schema from `schema_info`
  - Formats a prompt asking the LLM to generate an interesting natural language query
  - Uses the same routing logic as `generate_sql()` to choose between OpenAI/Anthropic
  - Includes prompt instructions to:
    - Create realistic, interesting queries that showcase the data
    - Limit output to a maximum of two sentences
    - Focus on queries that would provide meaningful insights
    - Use proper natural language phrasing
  - Returns the generated query string
- Handle edge cases:
  - Return a helpful message if no tables exist
  - Catch and re-raise LLM API errors with descriptive messages

### 3. Add API Endpoint for Query Generation
- Open `app/server/server.py`
- Import the new data models and `generate_random_query` function
- Create a new POST endpoint `@app.post("/api/generate-query", response_model=QueryGenerationResponse)`
- Implement the endpoint handler `async def generate_query_endpoint()`:
  - Get the current database schema using `get_database_schema()`
  - Check if any tables exist; if not, return an error in the response
  - Call `generate_random_query(schema_info)` to generate the query
  - Extract the list of table names analyzed
  - Return `QueryGenerationResponse` with the generated query and tables analyzed
  - Wrap in try/except to handle errors gracefully and return them in the response

### 4. Add Frontend TypeScript Types
- Open `app/client/src/types.d.ts`
- Add interface `QueryGenerationRequest` (empty object `{}`)
- Add interface `QueryGenerationResponse` matching the backend model:
  - `query: string`
  - `tables_analyzed: string[]`
  - `error?: string`

### 5. Add API Client Method
- Open `app/client/src/api/client.ts`
- Add a new method `generateQuery()` to the `api` object:
  - Makes a POST request to `/api/generate-query`
  - Returns `Promise<QueryGenerationResponse>`
  - Uses the existing `apiRequest` helper function

### 6. Add Generate Query Button to HTML
- Open `app/client/index.html`
- In the `query-controls` div (around line 22-25), modify the structure:
  - Change the div to use `justify-content: space-between` styling
  - Keep the "Query" button on the left
  - Add a new button with:
    - `id="generate-query-button"`
    - `class="secondary-button"`
    - Text content: "Generate Query"
    - Position it on the right side, separate from the "Query" and "Upload Data" buttons

### 7. Update CSS for Button Layout
- Open `app/client/src/style.css`
- Modify `.query-controls` class to ensure proper spacing:
  - Verify `justify-content: space-between` is set (or add it)
  - Ensure buttons are properly aligned
- No other CSS changes needed since we're reusing the existing `secondary-button` style

### 8. Implement Frontend Button Logic
- Open `app/client/src/main.ts`
- In the `initializeQueryInput()` function or create a new `initializeGenerateQuery()` function:
  - Get reference to the button: `document.getElementById('generate-query-button')`
  - Add click event listener that:
    - Disables the button and shows loading state
    - Calls `api.generateQuery()`
    - If successful and no error:
      - Get the query input element
      - Set its value to the generated query (this overwrites existing content)
      - Optionally add a brief visual feedback (like a subtle highlight)
    - If error:
      - Display an error message to the user (use existing `displayError()` function or create a subtle notification)
    - Finally, re-enable the button and clear loading state
  - Handle the case where no tables exist by showing a helpful message

### 9. Initialize the Generate Query Button
- Open `app/client/src/main.ts`
- In the `DOMContentLoaded` event listener, call the new initialization function (e.g., `initializeGenerateQuery()`)
- Ensure proper initialization order

### 10. Create E2E Test File
- Create a new file `.claude/commands/e2e/test_query_generator.md`
- Follow the structure from `.claude/commands/e2e/test_basic_query.md`
- Include test steps that:
  1. Navigate to the application URL
  2. Verify the "Generate Query" button is present
  3. Upload sample data (users.json) to ensure tables exist
  4. Click the "Generate Query" button
  5. Verify the query input field is populated with a non-empty query
  6. Take a screenshot of the generated query
  7. Verify the query is limited to two sentences maximum
  8. Click the "Query" button to execute the generated query
  9. Verify results are returned successfully
  10. Take a screenshot of the results
- Define success criteria:
  - Button is visible and clickable
  - Query is generated and populates the input field
  - Generated query is executable and returns results
  - Query is limited to two sentences
  - Screenshots are captured

### 11. Test Backend Endpoint
- Start the backend server: `cd app/server && uv run python server.py`
- Upload sample data through the UI or API
- Test the `/api/generate-query` endpoint using curl or Postman:
  ```bash
  curl -X POST http://localhost:8000/api/generate-query
  ```
- Verify the response contains a valid query and tables_analyzed list
- Test with no tables (empty database) to verify error handling

### 12. Test Frontend Integration
- Start both frontend and backend
- Click the "Generate Query" button
- Verify:
  - Loading state appears
  - Query input field is populated with generated query
  - Generated query makes sense for the available tables
  - Query can be executed successfully
  - Button works multiple times (generates different queries)

### 13. Run All Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Fix any issues that arise
- Verify the E2E test passes completely

## Testing Strategy

### Unit Tests
- **Backend LLM Processor Test**: Test `generate_random_query()` function with mock schema data
  - Verify it returns a non-empty string
  - Verify it handles empty schema (no tables) appropriately
  - Verify it limits output to two sentences
- **Backend API Endpoint Test**: Test `/api/generate-query` endpoint
  - Verify successful response with valid schema
  - Verify error response when no tables exist
  - Verify response model matches `QueryGenerationResponse`
- **Frontend API Client Test**: Test `api.generateQuery()` method
  - Mock the API response and verify the method returns correct data
  - Test error handling

### Edge Cases
- **No tables in database**: Button should display helpful message or disable
- **LLM API failure**: Should show user-friendly error message
- **Very large schemas**: Query generation should still complete in reasonable time
- **Multiple table relationships**: Generated queries should demonstrate joins or multi-table queries
- **Empty query input vs. existing query**: Button should overwrite any existing content
- **Rapid button clicks**: Should prevent multiple simultaneous API calls (debounce or disable)
- **Network errors**: Should handle timeout and connection failures gracefully

## Acceptance Criteria
- A "Generate Query" button is visible in the UI, styled like the "Upload Data" button
- Button is positioned separately from the primary "Query" button (using `justify-content: space-between`)
- Clicking the button generates a natural language query based on current database tables
- Generated query appears in the query input field, overwriting any existing content
- Generated queries are limited to a maximum of two sentences
- Generated queries are contextually relevant to the available table structures
- Button shows loading state during API call
- If no tables exist, user receives a helpful error message
- Generated queries can be successfully executed using the existing query functionality
- Button works correctly when clicked multiple times (generates different queries each time)
- E2E test validates the complete workflow from button click to query execution

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md` and understand the E2E testing framework
- Read and execute `.claude/commands/e2e/test_query_generator.md` to validate the query generator functionality works end-to-end with screenshots proving the feature works
- `cd app/server && uv run pytest tests/ -v` - Run all server tests to validate no regressions in backend
- `cd app/server && uv run python -m py_compile server.py core/*.py` - Validate Python syntax
- `cd app/server && uv run ruff check .` - Run Python linter to check code quality
- `cd app/client && bun tsc --noEmit` - Run TypeScript type checking to validate frontend types
- `cd app/client && bun run build` - Run frontend build to validate production build works
- Manually test the complete workflow:
  1. Start server and client (`scripts/start.sh`)
  2. Upload sample data (users.json)
  3. Click "Generate Query" button
  4. Verify query appears in input field
  5. Click "Query" button to execute
  6. Verify results are displayed
  7. Repeat 3-6 multiple times to test different generated queries

## Notes
- The query generation uses the same LLM provider routing as the existing SQL generation (OpenAI priority, then Anthropic)
- Generated queries should be creative but realistic, showcasing actual use cases for the data
- Consider adding a variety to the generated queries to prevent repetitive suggestions (the LLM's temperature can help with this)
- The two-sentence limit ensures queries are concise and focused
- Future enhancements could include:
  - Multiple query suggestions presented to the user
  - Query generation based on specific tables (not just all tables)
  - Query difficulty levels (simple vs. complex queries)
  - History of generated queries
- The button uses the `secondary-button` style to distinguish it from the primary action
- Error handling is critical since LLM APIs can fail or rate limit
- The feature leverages existing infrastructure (`llm_processor.py`, `sql_security.py`) for consistency
