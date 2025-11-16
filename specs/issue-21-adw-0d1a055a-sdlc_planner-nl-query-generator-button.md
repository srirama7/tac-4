# Feature: Natural Language Query Generator Button

## Feature Description
Add a new button to the Natural Language SQL Interface that automatically generates interesting natural language queries based on the existing database tables and their structures. The button will populate the query input field with a generated query, allowing users to discover query possibilities and understand what they can ask about their data. The generated queries will be contextually relevant to the uploaded tables and designed to showcase the application's capabilities.

## User Story
As a user
I want a button that generates example natural language queries based on my uploaded data
So that I can discover what kinds of questions I can ask and get started quickly without thinking of queries myself

## Problem Statement
Users who upload data to the Natural Language SQL Interface may not know what questions to ask or how to formulate their queries effectively. They need inspiration and examples that are contextually relevant to their specific data. Without sample queries, users might struggle to utilize the full potential of the natural language to SQL conversion feature, especially when dealing with unfamiliar datasets.

## Solution Statement
Implement a "Generate Query" button placed alongside the existing "Query" and "Upload Data" buttons in the query controls section. When clicked, this button will:
1. Retrieve the current database schema (tables and columns)
2. Send the schema information to the LLM processor to generate an interesting, contextual natural language query
3. Automatically populate (overwrite) the query input field with the generated query
4. Allow users to immediately execute the query or modify it as needed

The button will use the existing `llm_processor.py` infrastructure and follow the styling of the "Upload Data" button (secondary-button class). The generated queries will be limited to two sentences maximum for clarity and simplicity.

## Relevant Files
Use these files to implement the feature:

- **app/client/index.html** (lines 14-26) - Contains the query section HTML structure where the new button will be added to the query-controls div
- **app/client/src/main.ts** (lines 14-50) - Contains the query input initialization logic; will need to add the new button's click handler
- **app/client/src/api/client.ts** - API client module; will need to add a new API method to call the generate query endpoint
- **app/client/src/types.d.ts** - TypeScript type definitions; will need to add types for the new API request/response
- **app/client/src/style.css** (lines 116-125) - Contains the secondary-button styling that will be reused for the new button
- **app/server/server.py** (lines 1-280) - FastAPI server; will need to add a new endpoint `/api/generate-query` for query generation
- **app/server/core/llm_processor.py** (lines 1-228) - LLM processor module; will need to add a new function to generate natural language queries based on schema
- **app/server/core/data_models.py** (lines 1-82) - Pydantic models; will need to add request/response models for the generate query endpoint
- **app/server/core/sql_processor.py** - Used to retrieve database schema information for the LLM

### New Files
- **.claude/commands/e2e/test_generate_query.md** - End-to-end test file to validate the generate query button functionality

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure to support query generation by:
1. Adding new Pydantic models for the generate query request/response in `data_models.py`
2. Implementing the LLM-based query generation function in `llm_processor.py` that takes schema information and produces contextual natural language queries
3. Creating the FastAPI endpoint in `server.py` to handle generate query requests

### Phase 2: Core Implementation
Build the frontend user interface by:
1. Adding the "Generate Query" button to the HTML interface
2. Implementing the button's event handler in the main TypeScript file
3. Creating the API client method to call the backend endpoint
4. Adding appropriate loading states and error handling

### Phase 3: Integration
Connect the frontend and backend components by:
1. Testing the complete flow from button click to query population
2. Ensuring the generated queries work seamlessly with the existing query execution flow
3. Validating that the button styling matches the "Upload Data" button
4. Creating comprehensive end-to-end tests to validate the feature

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Backend Data Models
- Open `app/server/core/data_models.py`
- Add a new `GenerateQueryRequest` model with no required fields (empty request body)
- Add a new `GenerateQueryResponse` model with fields:
  - `query: str` - The generated natural language query
  - `error: Optional[str] = None` - Error message if generation fails

### Step 2: Backend LLM Query Generator
- Open `app/server/core/llm_processor.py`
- Add a new function `generate_natural_language_query(schema_info: Dict[str, Any]) -> str` that:
  - Takes the database schema as input
  - Formats the schema information for the LLM prompt
  - Creates a prompt asking the LLM to generate an interesting natural language query based on the tables and columns
  - Specifies in the prompt to limit the query to two sentences maximum
  - Uses the same LLM routing logic as `generate_sql()` (Gemini → OpenAI → Anthropic priority)
  - Returns the generated natural language query as a string
  - Handles errors appropriately
- The prompt should ask for queries that:
  - Are interesting and showcase data analysis capabilities
  - Are relevant to the actual tables and columns present
  - Use natural, conversational language
  - Can be successfully converted to SQL

### Step 3: Backend API Endpoint
- Open `app/server/server.py`
- Add a new POST endpoint `/api/generate-query` with response model `GenerateQueryResponse`
- The endpoint should:
  - Get the current database schema using `get_database_schema()`
  - Validate that at least one table exists (return error if no tables)
  - Call `generate_natural_language_query()` with the schema
  - Return the generated query in the response
  - Handle exceptions and return appropriate error messages
  - Log success and error cases using the existing logging pattern

### Step 4: Frontend TypeScript Types
- Open `app/client/src/types.d.ts`
- Add a `GenerateQueryResponse` interface with:
  - `query: string`
  - `error?: string`

### Step 5: Frontend API Client Method
- Open `app/client/src/api/client.ts`
- Add a new method `generateQuery()` to the `api` object that:
  - Makes a POST request to `/api/generate-query`
  - Returns a `Promise<GenerateQueryResponse>`
  - Follows the same pattern as existing API methods

### Step 6: Frontend HTML Button
- Open `app/client/index.html`
- Add a new button in the `.query-controls` div (line 22-25) between the Query button and Upload Data button
- Button should have:
  - `id="generate-query-button"`
  - `class="secondary-button"`
  - Text content: "Generate Query"
- Position it so the layout is: [Query] [Generate Query] [Upload Data] with space-between justification

### Step 7: Frontend Button Handler
- Open `app/client/src/main.ts`
- Create a new function `initializeGenerateQueryButton()` that:
  - Gets references to the generate query button and query input field
  - Adds a click event listener to the button
  - On click:
    - Disables the button and shows a loading spinner
    - Calls `api.generateQuery()`
    - If successful, overwrites the query input field value with the generated query
    - If error, displays error using the existing `displayError()` function
    - Re-enables the button when complete
- Call `initializeGenerateQueryButton()` from the `DOMContentLoaded` event listener

### Step 8: Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand the E2E test framework
- Read `.claude/commands/e2e/test_basic_query.md` to understand the test file format
- Create a new file `.claude/commands/e2e/test_generate_query.md` that validates:
  - User can click the "Generate Query" button
  - The query input field is populated with a generated query
  - The generated query is relevant to the uploaded table structure
  - The user can immediately execute the generated query
  - Results are displayed successfully
- The test should include specific steps to:
  1. Upload sample data (e.g., users.json)
  2. Click "Generate Query" button
  3. Verify the input field is populated
  4. Take screenshot of the generated query
  5. Click "Query" button to execute it
  6. Verify results appear
  7. Take screenshot of results
- Include at least 3-4 screenshots to demonstrate the functionality

### Step 9: Manual Testing and Validation
- Start the server and client using `./scripts/start.sh`
- Upload sample data using one of the sample data buttons
- Click the "Generate Query" button
- Verify the query input field is populated with a contextual query
- Execute the generated query and verify it returns results
- Test with multiple different table schemas (users, products, events)
- Verify error handling when no tables are loaded
- Test the loading state during query generation

### Step 10: Run Validation Commands
- Execute all validation commands listed in the Validation Commands section
- Ensure all tests pass with zero errors
- Run the new E2E test to validate the feature works end-to-end
- Verify no regressions in existing functionality

## Testing Strategy

### Unit Tests
- **Backend LLM function test** - Test `generate_natural_language_query()` with various schema structures
  - Single table with basic columns
  - Multiple tables with relationships
  - Tables with different data types (text, numeric, dates)
  - Edge case: empty schema (should handle gracefully)
- **API endpoint test** - Test `/api/generate-query` endpoint
  - Success case with existing tables
  - Error case with no tables loaded
  - Error case with LLM API failures
- **Frontend API client test** - Verify `api.generateQuery()` makes correct API calls

### Edge Cases
- **No tables loaded**: Button should be clickable but API should return friendly error message
- **LLM API key not configured**: Should fallback gracefully through providers or return helpful error
- **Very large schemas**: Query generation should handle databases with many tables/columns
- **Network failures**: Frontend should display appropriate error message
- **Concurrent clicks**: Button should be disabled during generation to prevent multiple simultaneous requests
- **Empty table names or columns**: Should handle edge cases in schema gracefully
- **Generated query exceeds two sentences**: Validate the LLM respects the prompt constraint

## Acceptance Criteria
- The "Generate Query" button is visible in the query controls section and styled consistently with the "Upload Data" button
- Clicking the button triggers query generation based on the current database schema
- The query input field is automatically populated (overwritten) with the generated query
- Generated queries are contextually relevant to the uploaded tables and their structures
- Generated queries are limited to a maximum of two sentences
- The button shows a loading state while generating the query
- Error messages are displayed appropriately when generation fails or no tables exist
- Users can immediately execute the generated query using the existing "Query" button
- The feature works with all three LLM providers (Gemini, OpenAI, Anthropic)
- All existing functionality remains unaffected (no regressions)
- The E2E test passes and validates the complete workflow

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test `.claude/commands/e2e/test_generate_query.md` to validate the generate query button functionality works end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/core/test_llm_processor.py -v` - Run LLM processor tests specifically to validate new query generation function
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript compilation to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Manual verification:
  1. Start the application with `./scripts/start.sh`
  2. Upload sample data (users, products, or events)
  3. Click "Generate Query" button
  4. Verify query input is populated with a relevant query
  5. Click "Query" button to execute the generated query
  6. Verify results are displayed correctly
  7. Repeat with different sample datasets to ensure variety

## Notes
- The feature leverages the existing `llm_processor.py` infrastructure, maintaining consistency with the current LLM integration pattern
- The button uses the `secondary-button` CSS class to match the "Upload Data" button styling, ensuring visual consistency
- Query generation uses the same LLM provider priority as SQL generation (Gemini → OpenAI → Anthropic), reducing configuration complexity
- The two-sentence limit ensures queries are concise and easy to understand at a glance
- Generated queries will always overwrite the current input field content, as specified in the requirements
- Consider adding telemetry/logging to track which types of generated queries users find most useful (future enhancement)
- Future enhancement: Allow users to request different types of queries (simple vs. complex, aggregations vs. filters, etc.)
- Future enhancement: Add a "history" feature to cycle through previously generated queries
- The feature requires at least one table to be loaded; appropriate error handling is implemented for this edge case
- The LLM prompt should be crafted to produce queries that are likely to succeed when converted back to SQL by the existing query processing pipeline
