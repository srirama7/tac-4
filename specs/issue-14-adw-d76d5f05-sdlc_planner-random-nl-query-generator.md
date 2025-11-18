# Feature: Random Natural Language Query Generator

## Feature Description
This feature adds a new button to the Natural Language SQL Interface that generates interesting, random natural language queries based on the existing database tables and their structure. When clicked, the button generates a query (limited to two sentences maximum) using the LLM processor, automatically populates the query input field with the generated text (overwriting any existing content), and allows users to manually execute the query. The button is positioned separately from the primary query button, using the same visual style as the "Upload Data" button for consistency.

## User Story
As a user exploring my data
I want to get random query suggestions based on my current database schema
So that I can discover interesting insights and learn what kinds of questions I can ask about my data

## Problem Statement
Users may not know what kinds of questions to ask about their data, especially when first getting started with the Natural Language SQL Interface. They need inspiration and examples of meaningful queries based on their actual database schema. Current workflows require users to manually think of and type queries, which can be challenging for new users or when exploring unfamiliar datasets.

## Solution Statement
Add a "Random Query" button that leverages the existing LLM processor to analyze the current database schema and generate contextually relevant, interesting natural language queries. The button will automatically populate the query input field with the generated text, providing instant query suggestions while maintaining user control over execution. By reusing the existing `llm_processor.py` infrastructure and following established UI patterns (Upload Data button style), this solution integrates seamlessly with the current architecture.

## Relevant Files
Use these files to implement the feature:

- **app/server/core/llm_processor.py** - Contains the LLM integration logic for OpenAI and Anthropic. We'll add a new function `generate_random_query()` that generates natural language queries based on database schema, following the existing patterns for `generate_sql_with_openai()` and `generate_sql_with_anthropic()`.

- **app/server/core/sql_processor.py** - Contains `get_database_schema()` which retrieves the current database schema. We'll use this to provide table and column information to the LLM for query generation.

- **app/server/server.py** - The FastAPI application server. We'll add a new endpoint `POST /api/generate-random-query` that uses the LLM processor to create random queries.

- **app/server/core/data_models.py** - Contains Pydantic models for API requests and responses. We'll add `RandomQueryRequest` and `RandomQueryResponse` models.

- **app/client/index.html** - Contains the HTML structure for the UI. We'll add the new "Random Query" button in the query controls section, positioned to be visually distinct from the primary query button.

- **app/client/src/main.ts** - Contains the frontend application logic. We'll add the `initializeRandomQueryButton()` function and the API call handler to fetch and populate random queries.

- **app/client/src/api/client.ts** - Contains the API client methods. We'll add a `generateRandomQuery()` method to call the new backend endpoint.

- **app/client/src/types.d.ts** - Contains TypeScript type definitions. We'll add the `RandomQueryRequest` and `RandomQueryResponse` interfaces.

- **app/client/src/style.css** - Contains the styling for the application. We may need to add or adjust button styling to ensure the Random Query button is visually distinct and uses the Upload Data button style.

### New Files

- **app/server/tests/core/test_random_query.py** - Unit tests for the random query generation functionality, including testing with various schema configurations, API key availability, and error handling.

- **.claude/commands/e2e/test_random_query.md** - E2E test file that validates the Random Query button functionality, including UI interaction, query generation, and field population. This test should verify that clicking the button generates a query, populates the input field, and overwrites existing content.

## Implementation Plan

### Phase 1: Foundation
First, we'll establish the backend infrastructure by creating new data models and adding the query generation logic to the LLM processor. This includes defining the API contract (request/response models) and implementing the core algorithm that analyzes database schema and generates contextually relevant natural language queries. We'll ensure the implementation follows existing patterns in `llm_processor.py` and properly handles both OpenAI and Anthropic providers.

### Phase 2: Core Implementation
Next, we'll create the API endpoint in the FastAPI server to expose the random query generation functionality. Then we'll implement the frontend components, including adding the button to the HTML, creating the TypeScript handler logic, adding the API client method, and ensuring the generated query properly overwrites the input field. We'll style the button to match the Upload Data button appearance while positioning it distinctly from primary actions.

### Phase 3: Integration
Finally, we'll integrate the feature with the existing application flow, ensuring it works seamlessly with the query execution workflow. We'll add comprehensive tests (both unit tests for backend logic and E2E tests for user interaction), validate the feature against the acceptance criteria, and ensure zero regressions across the application.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Data Models for Random Query Generation
- Read `app/server/core/data_models.py`
- Add `RandomQueryRequest` model (empty or with optional preferences in the future)
- Add `RandomQueryResponse` model with fields: `query` (str), `tables_used` (List[str]), `error` (Optional[str])
- Update `app/client/src/types.d.ts` with corresponding TypeScript interfaces

### Step 2: Implement Random Query Generation in LLM Processor
- Read `app/server/core/llm_processor.py` to understand existing patterns
- Add `generate_random_query_with_openai(schema_info: Dict[str, Any]) -> str` function that creates interesting natural language queries based on schema
- Add `generate_random_query_with_anthropic(schema_info: Dict[str, Any]) -> str` function with the same behavior
- Add `generate_random_query(schema_info: Dict[str, Any]) -> str` routing function that follows the same priority logic as `generate_sql()` (OpenAI first, then Anthropic, then fallback)
- Ensure the LLM prompt instructs the model to:
  - Generate interesting, meaningful queries based on available tables and columns
  - Limit output to two sentences maximum
  - Focus on queries that demonstrate the database's capabilities
  - Vary query types (aggregations, filters, joins, etc.) for diversity
  - Return ONLY the natural language query text, no explanations

### Step 3: Create API Endpoint for Random Query Generation
- Read `app/server/server.py` to understand existing endpoint patterns
- Add `POST /api/generate-random-query` endpoint
- Endpoint should:
  - Call `get_database_schema()` to get current schema
  - Call `generate_random_query(schema_info)` from llm_processor
  - Return `RandomQueryResponse` with the generated query
  - Handle errors gracefully and return error messages in the response
  - Log success/failure with appropriate messages
- Follow the error handling patterns used in other endpoints

### Step 4: Write Backend Unit Tests
- Create `app/server/tests/core/test_random_query.py`
- Test `generate_random_query_with_openai()` with mock schema data
- Test `generate_random_query_with_anthropic()` with mock schema data
- Test routing logic in `generate_random_query()`
- Test error handling when API keys are missing
- Test with various schema configurations (single table, multiple tables, different column types)
- Test that generated queries are limited to two sentences maximum
- Run tests with `cd app/server && uv run pytest tests/core/test_random_query.py -v`

### Step 5: Add API Client Method
- Read `app/client/src/api/client.ts` to understand existing API methods
- Add `generateRandomQuery()` method to the api object
- Method should call `POST /api/generate-random-query` and return `Promise<RandomQueryResponse>`
- Follow the error handling patterns used in other API methods

### Step 6: Add Random Query Button to HTML
- Read `app/client/index.html`
- Add a new button with id `random-query-button` in the query-controls section
- Button text should be "Random Query"
- Add class `secondary-button` to match Upload Data button styling
- Position the button to be visually distinct from the primary Query button (use CSS flexbox with `justify-content: space-between` or similar)

### Step 7: Implement Frontend Random Query Logic
- Read `app/client/src/main.ts` to understand existing patterns
- Add `initializeRandomQueryButton()` function in `main.ts`
- Function should:
  - Get reference to the random-query-button element
  - Add click event listener
  - On click, disable button and show loading state
  - Call `api.generateRandomQuery()`
  - On success, populate the query input field (overwrite existing content) with the generated query
  - On error, call `displayError()` with appropriate message
  - Re-enable button after completion
- Call `initializeRandomQueryButton()` in the DOMContentLoaded event listener

### Step 8: Update Styling
- Read `app/client/src/style.css`
- Verify that `.secondary-button` styling exists and matches Upload Data button
- Update `.query-controls` styling to ensure proper spacing between buttons using `justify-content: space-between` or `gap` property
- Ensure the Random Query button is visually distinct from the primary Query button but maintains consistency with the Upload Data button style

### Step 9: Create E2E Test File
- Read `.claude/commands/test_e2e.md` and `.claude/commands/e2e/test_basic_query.md` to understand E2E test format
- Create `.claude/commands/e2e/test_random_query.md`
- Test should include:
  - User story describing the feature
  - Steps to navigate to the application and verify initial state
  - Upload sample data (users.json) to ensure schema exists
  - Screenshot of initial state with Random Query button visible
  - Click Random Query button
  - Verify query input field is populated with generated text
  - Verify text is limited to approximately two sentences
  - Screenshot of populated query field
  - Clear the field and click Random Query again
  - Verify new query is generated and overwrites the field
  - Screenshot of second generated query
  - Success criteria including button functionality, field population, and query variation

### Step 10: Run All Validation Commands
- Execute all commands listed in the Validation Commands section below
- Ensure zero errors and zero regressions
- Verify the feature works end-to-end
- Confirm all tests pass
- Verify the E2E test produces expected screenshots

## Testing Strategy

### Unit Tests
- **Test Random Query Generation Functions**: Verify that `generate_random_query_with_openai()` and `generate_random_query_with_anthropic()` generate valid natural language queries based on schema data
- **Test Routing Logic**: Ensure `generate_random_query()` correctly routes to OpenAI or Anthropic based on API key availability
- **Test Error Handling**: Verify graceful handling when API keys are missing or API calls fail
- **Test Query Length Constraint**: Confirm generated queries are limited to two sentences maximum
- **Test Schema Variation**: Test with different schema configurations including single table, multiple tables, various column types, and empty schemas
- **Test API Endpoint**: Verify the `/api/generate-random-query` endpoint returns correct responses for valid requests and appropriate errors for invalid requests

### Edge Cases
- **No Tables in Database**: When no tables exist, the endpoint should return an error message or a suggestion to upload data
- **Empty Schema**: Handle cases where tables exist but have no rows or minimal data
- **API Key Missing**: Gracefully handle when neither OpenAI nor Anthropic API keys are available
- **API Call Failure**: Handle network errors, timeout errors, and API rate limiting gracefully
- **Long Table/Column Names**: Ensure queries are still limited to two sentences even with lengthy identifiers
- **Multiple Rapid Clicks**: Ensure button is properly disabled during generation to prevent multiple simultaneous requests
- **Special Characters in Schema**: Verify queries are generated correctly even when table/column names contain special characters
- **Very Large Schema**: Test behavior with databases containing many tables and columns

## Acceptance Criteria
- [ ] A "Random Query" button is added to the query controls section, visually distinct from the primary Query button
- [ ] The button uses the same styling as the Upload Data button (secondary-button class)
- [ ] Clicking the button generates a natural language query based on the current database schema
- [ ] The generated query is limited to two sentences maximum
- [ ] The generated query automatically populates the query input field, overwriting any existing content
- [ ] The button shows a loading state while generating the query
- [ ] The button is disabled during query generation to prevent multiple simultaneous requests
- [ ] If an error occurs, an appropriate error message is displayed to the user
- [ ] The backend endpoint `/api/generate-random-query` successfully generates queries using the LLM processor
- [ ] The implementation reuses existing `llm_processor.py` logic and follows established patterns
- [ ] All backend unit tests pass with zero failures
- [ ] The E2E test validates the complete user workflow including button interaction, query generation, and field population
- [ ] All validation commands execute successfully with zero regressions
- [ ] The feature works with both OpenAI and Anthropic LLM providers (based on API key availability)
- [ ] Generated queries are contextually relevant to the available database schema
- [ ] Clicking the button multiple times generates different queries (demonstrates variety)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E `.claude/commands/e2e/test_random_query.md` test file to validate this functionality works end-to-end with real browser interaction
- `cd app/server && uv run pytest tests/core/test_random_query.py -v` - Run new random query unit tests to validate backend logic
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun run tsc --noEmit` - Run TypeScript type checking to validate frontend code has no type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature compiles correctly with zero errors

## Notes

### Future Enhancements
- **Query Categories**: Allow users to specify query types (aggregation, filtering, joining, etc.) via optional parameters
- **Favorite Queries**: Add ability to save generated queries for future use
- **Query History**: Track previously generated random queries to avoid immediate repetition
- **Difficulty Levels**: Generate queries of varying complexity (simple, intermediate, advanced)
- **Multi-Table Focus**: Optionally generate queries that specifically target joins between multiple tables

### Implementation Considerations
- The feature leverages the existing `llm_processor.py` infrastructure, which already handles OpenAI and Anthropic API integration with proper routing logic
- The two-sentence limit ensures queries remain concise and focused, improving user experience and reducing token usage
- Overwriting the input field (rather than appending) provides a clean, predictable UX and matches user expectations for a "generate" action
- Using the Upload Data button style creates visual consistency and helps users understand this is a secondary action (not the primary query execution button)
- The feature requires an active LLM API key (OpenAI or Anthropic) to function, consistent with the existing query processing feature
- Generated queries should be diverse and interesting to provide maximum value for exploration and learning
- Error handling should be consistent with other API endpoints to maintain a uniform user experience

### Security Notes
- The feature only reads database schema information (table names, column names, types) and does not execute any queries automatically
- Users must manually execute the generated query by clicking the Query button, maintaining full control over database operations
- The implementation follows existing security patterns from `sql_processor.py` and `sql_security.py`
- No user input is directly passed to the LLM beyond the schema information retrieved from the database
