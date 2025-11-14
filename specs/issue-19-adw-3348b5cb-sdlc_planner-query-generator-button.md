# Feature: Random Natural Language Query Generator Button

## Feature Description
This feature adds a new button to the Natural Language SQL Interface that automatically generates interesting, natural language queries based on the database's table structures. When clicked, the button leverages the LLM processor to analyze the available tables and their columns, then creates a contextually relevant query suggestion that demonstrates the data exploration capabilities. The generated query will automatically populate the input field (overwriting any existing content), allowing users to execute it manually with a single click.

## User Story
As a user exploring my database
I want to click a button to generate example queries based on my table structures
So that I can discover interesting ways to query my data without needing to think of queries myself

## Problem Statement
Users often struggle with knowing what questions to ask about their data, especially when working with unfamiliar datasets. This creates friction in the user experience as users need to understand the table structure and think of meaningful queries themselves. Without example queries, users may not realize the full potential of the natural language interface or understand how to phrase complex questions.

## Solution Statement
Add a "Generate Query" button that uses the existing LLM processor to create natural language query suggestions based on the current database schema. The button will be styled consistently with the "Upload Data" button and positioned separately from the primary Query button. When clicked, it will generate a random, contextually relevant query (limited to two sentences maximum) and populate the query input field, giving users instant inspiration for exploring their data.

## Relevant Files
Use these files to implement the feature:

- `app/client/index.html` - Contains the HTML structure where we need to add the new button in the query controls section
- `app/client/src/main.ts` - Contains the client-side JavaScript logic where we'll add the button click handler and API integration
- `app/client/src/api/client.ts` - Contains the API client methods where we'll add the new endpoint for query generation
- `app/client/src/types.d.ts` - Contains TypeScript type definitions where we'll define the request/response types for query generation
- `app/client/src/style.css` - Contains the CSS styles where we'll add styling for the new button matching the Upload Data button style
- `app/server/server.py` - Contains the FastAPI server where we'll add the new `/api/generate-query` endpoint
- `app/server/core/llm_processor.py` - Contains LLM integration logic where we'll add the query generation function
- `app/server/core/data_models.py` - Contains Pydantic models where we'll add request/response models for the new endpoint
- `.claude/commands/test_e2e.md` - Reference for understanding E2E test structure
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test to understand test patterns

### New Files

- `.claude/commands/e2e/test_query_generator.md` - New E2E test file to validate the random query generator feature works correctly

## Implementation Plan

### Phase 1: Foundation
Before implementing the query generator feature, we need to set up the backend infrastructure to support query generation. This includes creating new data models for the request/response, adding the query generation logic to the LLM processor, and exposing a new API endpoint in the FastAPI server. These foundational changes will enable the frontend to request and receive generated queries.

### Phase 2: Core Implementation
With the backend foundation in place, we'll implement the frontend components. This involves adding the new button to the HTML structure with appropriate styling, creating the client-side API integration, and implementing the button click handler that fetches a generated query and populates the input field. The UI will be designed to match the existing "Upload Data" button style and be positioned appropriately.

### Phase 3: Integration
Finally, we'll integrate the feature end-to-end by creating comprehensive tests and validating the complete workflow. This includes creating an E2E test that validates the button appears, generates queries correctly, and populates the input field as expected. We'll also run the full test suite to ensure no regressions were introduced.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Task 1: Add Backend Data Models
- Read `app/server/core/data_models.py` to understand existing model patterns
- Add `GenerateQueryRequest` model with no required fields (empty request body)
- Add `GenerateQueryResponse` model with `query: str` and optional `error: Optional[str]` fields
- Follow existing Pydantic model conventions in the file

### Task 2: Implement Query Generation Logic in LLM Processor
- Read `app/server/core/llm_processor.py` to understand existing LLM integration patterns
- Add a new function `generate_random_query(schema_info: Dict[str, Any], llm_provider: str = "openai") -> str`
- The function should analyze the schema and generate an interesting, natural language query
- Create a prompt that instructs the LLM to:
  - Generate a single interesting query based on the available tables and columns
  - Limit the query to two sentences maximum
  - Make the query creative and demonstrate the data's potential
  - Focus on meaningful questions that would provide insights
- Follow the same error handling patterns as existing functions
- Support both OpenAI and Anthropic providers using the existing routing logic
- Clean up any markdown formatting from the LLM response

### Task 3: Add API Endpoint for Query Generation
- Read `app/server/server.py` to understand existing endpoint patterns
- Add a new POST endpoint `/api/generate-query` that:
  - Accepts an optional `GenerateQueryRequest` body
  - Gets the current database schema using `get_database_schema()`
  - Calls `generate_random_query()` from the LLM processor
  - Returns a `GenerateQueryResponse` with the generated query
  - Handles errors gracefully and returns them in the response
  - Logs success and failure using the existing logging patterns
- Add appropriate error handling with try/except blocks

### Task 4: Add TypeScript Type Definitions
- Read `app/client/src/types.d.ts` to understand existing type patterns
- Add `GenerateQueryRequest` interface (empty object)
- Add `GenerateQueryResponse` interface with `query: string` and `error?: string` fields
- Follow existing naming conventions and structure

### Task 5: Add API Client Method
- Read `app/client/src/api/client.ts` to understand existing API patterns
- Add a new `generateQuery()` method to the `api` object
- The method should make a POST request to `/generate-query`
- Return a `Promise<GenerateQueryResponse>`
- Follow the same patterns as existing methods like `processQuery()` and `uploadFile()`

### Task 6: Add Button to HTML
- Read `app/client/index.html` to understand the structure
- Add a new button with id `generate-query-button` to the `.query-controls` div
- Position it in the same container as the existing buttons
- Use class `secondary-button` to match the Upload Data button style
- Add appropriate text: "Generate Query"
- Place the button between the "Query" button and "Upload Data" button

### Task 7: Style the Generate Query Button
- Read `app/client/src/style.css` to understand existing button styles
- Ensure the button inherits the correct `secondary-button` styles
- Verify it matches the Upload Data button appearance
- Add any additional styles needed for proper spacing using flexbox justify-apart as specified

### Task 8: Implement Button Click Handler in Frontend
- Read `app/client/src/main.ts` to understand existing initialization patterns
- Create a new function `initializeQueryGenerator()` in the main.ts file
- Add the initialization call to the `DOMContentLoaded` event listener
- The function should:
  - Get the generate query button element
  - Get the query input element
  - Add a click event listener that:
    - Disables the button and shows loading state
    - Calls `api.generateQuery()`
    - Populates the query input field with the response (overwrites existing content)
    - Re-enables the button
    - Handles errors by displaying them using the existing `displayError()` function
- Follow the same patterns as `initializeQueryInput()` for consistency

### Task 9: Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand the E2E test execution format
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_complex_query.md` for E2E test structure examples
- Create `.claude/commands/e2e/test_query_generator.md` with:
  - User Story describing the query generator feature
  - Test Steps that:
    - Navigate to the application
    - Verify the Generate Query button is present
    - Click the Generate Query button
    - Verify the query input field is populated with a generated query
    - Verify the generated query is not empty and contains meaningful text
    - Take screenshots at key steps (initial state, button click, populated query)
    - Click the Query button to verify the generated query can be executed
    - Verify results appear
  - Success Criteria that validates:
    - Button exists and is clickable
    - Query is generated and populated
    - Generated query is executable
    - No errors occur
    - At least 4 screenshots are taken

### Task 10: Manual Testing
- Start the server and client using the scripts in `scripts/`
- Upload sample data using the Upload Data button
- Click the Generate Query button
- Verify the query input field is populated with a generated query
- Execute the generated query and verify it returns results
- Test with different datasets to ensure variety in generated queries
- Verify the button styling matches the Upload Data button
- Verify the button is positioned correctly (justified apart from primary buttons)

### Task 11: Run Validation Commands
- Execute all validation commands listed in the "Validation Commands" section below
- Fix any issues that arise
- Ensure zero regressions in existing functionality
- Verify all tests pass

## Testing Strategy

### Unit Tests
- Test the `generate_random_query()` function with various schema configurations
- Verify the function returns queries within the two-sentence limit
- Test error handling when LLM API calls fail
- Test the `/api/generate-query` endpoint returns proper response format
- Verify the endpoint handles missing schema gracefully

### Edge Cases
- Empty database with no tables - should return an appropriate error message
- Database with only one table and one column - should generate a simple query
- Database with multiple complex tables - should generate a query involving interesting joins or aggregations
- LLM API timeout or failure - should return an error without crashing
- Extremely long table/column names - should handle gracefully
- Special characters in table/column names - should escape properly in generated queries

## Acceptance Criteria
- A new "Generate Query" button appears in the UI, styled like the Upload Data button
- The button is positioned separately from the Query button, using justify-apart spacing
- Clicking the button generates a natural language query based on current tables
- The generated query is limited to two sentences maximum
- The generated query automatically populates the query input field, overwriting any existing content
- The generated query leverages the existing llm_processor.py functionality
- The button shows a loading state while generating the query
- Errors are handled gracefully and displayed to the user
- The generated queries are contextually relevant and interesting
- The feature works with both OpenAI and Anthropic LLM providers
- The E2E test validates the complete workflow
- All existing tests continue to pass without regression

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md` to understand E2E test execution
- Read and execute the new `.claude/commands/e2e/test_query_generator.md` E2E test file to validate the query generator functionality works end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### LLM Integration
The feature leverages the existing `llm_processor.py` module which already handles both OpenAI and Anthropic API integrations. The query generation prompt should be designed to produce creative, varied queries that demonstrate the data exploration capabilities of the interface.

### Query Quality
The generated queries should be:
- Contextually relevant to the available tables and columns
- Interesting and insightful (e.g., aggregations, filters, joins when multiple tables exist)
- Limited to two sentences maximum as specified
- Executable without errors
- Demonstrative of the natural language interface capabilities

### UI/UX Considerations
- The button should be clearly visible but not overshadow the primary Query button
- Loading state is important since LLM API calls can take 1-3 seconds
- The button should be disabled while a query is being generated to prevent multiple simultaneous requests
- Error messages should be user-friendly and actionable

### Security
- No user input is required, so SQL injection is not a concern
- The feature only reads the schema, it doesn't modify any data
- LLM API keys are already secured in environment variables
- Generated queries are processed through the same security validation as user-entered queries

### Future Enhancements
While not part of this implementation, future improvements could include:
- Generating multiple query suggestions and letting users choose
- Regenerating queries if the user doesn't like the suggestion
- Learning from user query patterns to generate more relevant suggestions
- Adding query categories (simple, complex, analytical, etc.)
