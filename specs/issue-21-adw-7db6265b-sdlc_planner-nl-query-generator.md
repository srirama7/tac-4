# Feature: Natural Language Query Generator Button

## Feature Description
This feature adds a new button that generates natural language queries based on the existing database tables and their structure. When clicked, the button generates interesting and contextually relevant natural language queries (limited to two sentences maximum) using the LLM processor, then automatically populates the query input field with the generated query, overwriting any existing content. The button is styled consistently with the "Upload Data" button and positioned with spacing from the primary action buttons.

## User Story
As a user
I want to generate example natural language queries based on my uploaded tables
So that I can quickly explore my data without having to think of queries myself

## Problem Statement
Users who have uploaded data tables may not know what kinds of questions they can ask about their data. They need inspiration and guidance on how to formulate natural language queries that are relevant to their specific database schema. Currently, users must manually type queries, which can be a barrier to exploring their data effectively.

## Solution Statement
Add a "Generate Query" button that leverages the existing llm_processor.py module to analyze the current database schema and generate contextually relevant, interesting natural language queries. The generated query will be limited to two sentences maximum to maintain clarity and will automatically populate the input field, replacing any existing content. This provides users with immediate, actionable examples of how to query their data.

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains the LLM integration logic (OpenAI and Anthropic) that will be extended to generate natural language queries based on table structures
- `app/server/server.py` - FastAPI server that will host the new `/api/generate-query` endpoint
- `app/server/core/data_models.py` - Contains Pydantic models; will need new models for the query generation request/response
- `app/server/core/sql_processor.py` - Contains `get_database_schema()` function that will provide table structure information to the LLM
- `app/client/src/main.ts` - Main TypeScript file that handles UI interactions; will add the button click handler and input field population logic
- `app/client/index.html` - HTML structure where the new button will be added
- `app/client/src/style.css` - Styles for the UI; will add styling for the new button consistent with the "Upload Data" button
- `app/client/src/types.d.ts` - TypeScript type definitions; will add types for the new API endpoint
- `app/client/src/api/client.ts` - API client that will add the new `generateQuery()` method

### New Files
- `app/server/tests/core/test_query_generator.py` - Unit tests for the query generation functionality
- `.claude/commands/e2e/test_nl_query_generator.md` - E2E test specification for validating the query generator button functionality

## Implementation Plan

### Phase 1: Foundation
1. Review the existing `llm_processor.py` to understand the current LLM integration patterns
2. Analyze the database schema structure returned by `get_database_schema()` to understand what information is available
3. Design the prompt engineering strategy for generating contextually relevant natural language queries based on table schemas
4. Define the API contract (request/response models) for the new endpoint

### Phase 2: Core Implementation
1. Extend `llm_processor.py` with a new function `generate_natural_language_query()` that:
   - Takes database schema information as input
   - Uses the same LLM routing logic as existing functions
   - Generates interesting, contextually relevant queries limited to two sentences
   - Returns a single natural language query string
2. Add new Pydantic models in `data_models.py` for the query generation endpoint
3. Implement the new `/api/generate-query` endpoint in `server.py` that:
   - Calls `get_database_schema()` to get current table structures
   - Passes schema to `generate_natural_language_query()`
   - Returns the generated query string
   - Handles errors gracefully with appropriate error responses
4. Add comprehensive unit tests in `test_query_generator.py`

### Phase 3: Integration
1. Add the "Generate Query" button to `index.html` positioned with spacing from primary buttons
2. Style the button in `style.css` to match the "Upload Data" button aesthetic
3. Add TypeScript types in `types.d.ts` for the new API endpoint
4. Extend the API client in `client.ts` with a `generateQuery()` method
5. Implement the click handler in `main.ts` that:
   - Calls the API endpoint
   - Handles loading states (disable button, show loading indicator)
   - Overwrites the query input field with the generated query
   - Handles errors with appropriate user feedback
6. Test the integration end-to-end manually

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Backend Query Generation Logic
- Add `generate_natural_language_query()` function to `app/server/core/llm_processor.py`
- Implement LLM prompt that analyzes table schemas and generates contextually relevant queries
- Ensure generated queries are limited to two sentences maximum
- Use the same LLM routing logic as existing functions (OpenAI priority, then Anthropic)
- Handle edge cases (no tables, empty schema, LLM errors)

### Step 2: Add Data Models
- Add `QueryGenerationRequest` and `QueryGenerationResponse` models to `app/server/core/data_models.py`
- Ensure models follow existing Pydantic patterns in the codebase
- Include error field in response model for graceful error handling

### Step 3: Implement API Endpoint
- Add `/api/generate-query` POST endpoint to `app/server/server.py`
- Endpoint should retrieve database schema using `get_database_schema()`
- Call `generate_natural_language_query()` with schema information
- Return generated query with appropriate error handling
- Add proper logging following existing patterns

### Step 4: Create Backend Unit Tests
- Create `app/server/tests/core/test_query_generator.py`
- Test query generation with various table schemas (single table, multiple tables, no tables)
- Test LLM provider routing logic
- Test error handling (no API keys, LLM failures, empty schemas)
- Mock LLM API calls to avoid actual API usage in tests

### Step 5: Add Frontend Button to HTML
- Add "Generate Query" button to `app/client/index.html` in the `.query-controls` section
- Position it with `justify-content: space-between` or similar spacing from primary buttons
- Give it an ID like `generate-query-button` for easy selection
- Use appropriate semantic HTML

### Step 6: Style the Frontend Button
- Add styles to `app/client/src/style.css` for the new button
- Style should match the "Upload Data" button (secondary-button class or similar)
- Ensure proper spacing and visual hierarchy
- Add hover and disabled states

### Step 7: Add TypeScript Types
- Add `QueryGenerationRequest` and `QueryGenerationResponse` interfaces to `app/client/src/types.d.ts`
- Ensure types match the backend Pydantic models exactly

### Step 8: Extend API Client
- Add `generateQuery()` method to `app/client/src/api/client.ts`
- Follow existing API client patterns
- Handle request/response properly

### Step 9: Implement Frontend Click Handler
- Add click handler in `app/client/src/main.ts` for the generate query button
- Implement loading state (disable button, show loading indicator)
- Call `api.generateQuery()`
- On success: overwrite the query input field value with the generated query
- On error: display error message to user
- Re-enable button when done

### Step 10: Create E2E Test Specification
- Create `.claude/commands/e2e/test_nl_query_generator.md` based on examples in `.claude/commands/e2e/`
- Read `.claude/commands/test_e2e.md` and `.claude/commands/e2e/test_basic_query.md` to understand the E2E test format
- Define test steps that validate:
  - Button is visible and clickable
  - Clicking button generates a query
  - Generated query populates the input field
  - Query overwrites existing content in the field
  - Button shows loading state during generation
  - Errors are handled gracefully
- Include screenshot capture points

### Step 11: Manual Testing
- Start the server and client
- Upload sample data to create tables
- Click the "Generate Query" button
- Verify that a natural language query is generated and populated in the input field
- Verify that existing content is overwritten
- Test with no tables uploaded (should handle gracefully)
- Test with multiple tables (should generate interesting multi-table queries)
- Verify loading states work correctly

### Step 12: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Run backend tests including the new unit tests
- Run frontend type checking and build
- Execute the new E2E test to validate the feature works end-to-end

## Testing Strategy

### Unit Tests
- **Query Generation Function Tests**:
  - Test with single table schema (should generate relevant single-table query)
  - Test with multiple tables schema (should generate interesting multi-table queries)
  - Test with empty schema (should return appropriate error or default message)
  - Test that generated queries are limited to two sentences maximum
  - Test LLM provider routing (OpenAI priority, then Anthropic fallback)
  - Mock LLM API responses to ensure deterministic tests

- **API Endpoint Tests**:
  - Test successful query generation flow
  - Test error handling when no tables exist
  - Test error handling when LLM API fails
  - Test error handling when no API keys are configured
  - Verify proper logging of successes and failures

### Edge Cases
- **No Tables**: User clicks button when no tables are uploaded - should show friendly error message
- **Very Large Schema**: Many tables with many columns - ensure prompt doesn't exceed token limits
- **LLM Timeout**: LLM API takes too long to respond - should timeout gracefully
- **Malformed Schema**: Database returns unexpected schema format - should handle without crashing
- **No API Keys**: Neither OpenAI nor Anthropic keys are configured - should return clear error message
- **Query Too Long**: LLM generates query longer than two sentences - should be enforced in prompt or trimmed
- **Concurrent Clicks**: User clicks button multiple times rapidly - should prevent multiple simultaneous requests
- **Empty Input Overwrite**: Overwriting empty input field should work the same as overwriting existing content
- **Long Existing Content**: Overwriting a very long existing query should work cleanly

## Acceptance Criteria
- New "Generate Query" button is visible in the UI, positioned with spacing from primary buttons
- Button styling matches the "Upload Data" button aesthetic
- Clicking the button triggers a query generation request to the backend
- Button shows loading state while generating (disabled, with loading indicator)
- Generated natural language query is limited to two sentences maximum
- Generated query automatically populates the query input field
- Any existing content in the query input field is completely overwritten
- If no tables exist, user receives a clear, friendly error message
- If LLM API fails, user receives a clear error message
- Backend unit tests pass with >80% coverage for new code
- E2E test passes and validates the complete user flow
- Feature works with both OpenAI and Anthropic LLM providers
- No regressions in existing functionality (all existing tests pass)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test `.claude/commands/e2e/test_nl_query_generator.md` to validate the query generator button functionality works as expected
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run the new query generator tests specifically
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate TypeScript types are correct
- `cd app/client && bun run build` - Run frontend build to validate the feature builds correctly with zero errors

## Notes

### LLM Prompt Strategy
The prompt for generating natural language queries should:
- Analyze the available tables and their columns
- Generate queries that showcase interesting relationships or insights
- Vary query complexity (sometimes simple single-table, sometimes multi-table joins)
- Use realistic natural language that a user would actually type
- Focus on common analytical questions (aggregations, filters, time-based queries, etc.)
- Respect the two-sentence maximum constraint

### Example Generated Queries
Based on a users table with columns (id, name, email, signup_date):
- "Show me all users who signed up in the last 30 days"
- "How many users signed up each month?"

Based on products table (id, name, price, category) and orders table (id, product_id, quantity, order_date):
- "What are the top 5 best-selling products by total quantity sold?"
- "Show me the total revenue for each product category"

### UI/UX Considerations
- The button should be clearly labeled (e.g., "Generate Query" or "Get Query Ideas")
- Loading state is critical to prevent user confusion during API call
- Error messages should be helpful and actionable
- The button should be discoverable but not compete visually with the primary "Query" button
- Consider adding a tooltip or help text explaining what the button does

### Future Enhancements (Out of Scope)
- Generate multiple query suggestions instead of just one
- Allow users to click multiple times to get different suggestions
- Save query history for reference
- Categorize queries by type (aggregation, filter, join, etc.)
- Add a "surprise me" mode that generates random interesting queries
