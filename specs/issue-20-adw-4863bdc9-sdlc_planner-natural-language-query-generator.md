# Feature: Natural Language Query Generator Button

## Feature Description
This feature adds a new button to the Natural Language SQL Interface that automatically generates interesting natural language queries based on the existing database tables and their structure. When clicked, the button will use an LLM to analyze the current schema and create meaningful, contextual queries that users can execute. The generated query will overwrite whatever is currently in the query input field, providing users with quick inspiration for exploring their data.

The button will be positioned separately from the primary query action buttons, using the same visual style as the "Upload Data" button to maintain UI consistency. Each generated query will be limited to two sentences maximum to keep them concise and focused.

## User Story
As a user of the Natural Language SQL Interface
I want to automatically generate interesting queries based on my database structure
So that I can quickly explore my data without thinking of questions manually

## Problem Statement
Users who upload data to the Natural Language SQL Interface may not immediately know what questions to ask about their data. They need to understand the schema, think of relevant questions, and formulate them in natural language. This creates friction in the user experience, especially for:
- New users who are exploring the application for the first time
- Users who have uploaded new datasets and want to quickly see what insights are available
- Users experiencing "blank page syndrome" when facing an empty query input field

The current interface requires users to come up with queries entirely on their own, which can be challenging when working with unfamiliar data structures.

## Solution Statement
We will add a "Generate Query" button that leverages the existing LLM infrastructure (llm_processor.py) to automatically create contextual, interesting natural language queries based on the current database schema. The button will:

1. Retrieve the current database schema including table names, column names, column types, and row counts
2. Send this schema information to an LLM with a specialized prompt designed to generate interesting analytical questions
3. Receive a concise natural language query (max 2 sentences) that explores the data in a meaningful way
4. Overwrite the query input field with this generated query
5. Allow users to immediately execute the query or generate a new one

This approach:
- Reduces friction by providing query suggestions instantly
- Helps users discover what types of questions they can ask
- Educates users about their data structure through example queries
- Reuses the existing LLM infrastructure for consistency and cost efficiency
- Maintains the same security and validation patterns used throughout the application

## Relevant Files
Use these files to implement the feature:

- **app/server/server.py** - Main FastAPI server where we'll add a new endpoint `/api/generate-query` to handle query generation requests
- **app/server/core/llm_processor.py** - Contains the LLM integration logic; we'll add a new function `generate_natural_language_query()` to create queries based on schema
- **app/server/core/data_models.py** - Contains Pydantic models; we'll add `GenerateQueryRequest` and `GenerateQueryResponse` models
- **app/server/core/sql_processor.py** - Contains `get_database_schema()` function which we'll use to retrieve current schema information
- **app/client/src/main.ts** - Main TypeScript file where we'll add the button click handler and UI update logic
- **app/client/src/api/client.ts** - API client module where we'll add the `generateQuery()` method
- **app/client/index.html** - HTML template where we'll add the new "Generate Query" button to the UI
- **app/client/src/style.css** - CSS file where we may need to add minor styling adjustments for button positioning
- **app/client/src/types.d.ts** - TypeScript type definitions where we'll add types for the new API response

### New Files
- **.claude/commands/e2e/test_query_generator.md** - E2E test file to validate the query generation feature works correctly

## Implementation Plan

### Phase 1: Foundation
First, we'll establish the backend infrastructure by creating the data models and LLM query generation logic. This includes:
- Adding Pydantic models for request/response validation
- Creating a specialized LLM prompt that generates interesting queries based on schema
- Building the query generation function that interfaces with OpenAI/Anthropic APIs
- Ensuring proper error handling for cases where no tables exist or API calls fail

### Phase 2: Core Implementation
Next, we'll implement the API endpoint and frontend components:
- Creating the FastAPI endpoint that receives requests and returns generated queries
- Adding the API client method in TypeScript to communicate with the backend
- Implementing the button UI element with appropriate styling and positioning
- Creating the click handler that calls the API and updates the input field
- Adding loading states and error handling for a smooth user experience

### Phase 3: Integration
Finally, we'll integrate the feature with existing functionality and validate it works correctly:
- Testing the feature with various database schemas (empty, single table, multiple tables)
- Ensuring the generated queries work with the existing query execution flow
- Creating comprehensive E2E tests to validate the feature end-to-end
- Running all validation commands to ensure zero regressions

## Step by Step Tasks

### 1. Add Backend Data Models
- Open `app/server/core/data_models.py`
- Add `GenerateQueryRequest` model (empty model, no parameters needed since it uses current schema)
- Add `GenerateQueryResponse` model with fields:
  - `query: str` - The generated natural language query
  - `error: Optional[str]` - Error message if generation fails

### 2. Implement Query Generation Logic
- Open `app/server/core/llm_processor.py`
- Add new function `generate_natural_language_query(schema_info: Dict[str, Any]) -> str`
- Create a specialized prompt that:
  - Takes the schema information (tables, columns, types, row counts)
  - Instructs the LLM to generate an interesting analytical query
  - Limits the query to 2 sentences maximum
  - Ensures the query is something that would work with the available data
- Implement routing logic similar to `generate_sql()` to use available API keys (OpenAI first, then Anthropic)
- Add proper error handling and validation
- Return a clean natural language query string

### 3. Create API Endpoint
- Open `app/server/server.py`
- Add new POST endpoint `/api/generate-query` with response model `GenerateQueryResponse`
- Endpoint logic:
  - Get current database schema using `get_database_schema()`
  - Check if any tables exist; if not, return error "No tables available. Please upload data first."
  - Call `generate_natural_language_query()` with schema info
  - Return the generated query in the response model
- Add comprehensive error handling with try/except
- Add logging for success and error cases following existing patterns

### 4. Add TypeScript Types
- Open `app/client/src/types.d.ts`
- Add interface `GenerateQueryResponse`:
  - `query: string`
  - `error?: string`

### 5. Implement API Client Method
- Open `app/client/src/api/client.ts`
- Add `generateQuery()` method to the `api` object
- Method should:
  - Make a POST request to `/generate-query`
  - Return `Promise<GenerateQueryResponse>`
  - Follow the same pattern as existing API methods

### 6. Add Button to HTML
- Open `app/client/index.html`
- Locate the `.query-controls` div (contains Query and Upload Data buttons)
- Add a new button with:
  - id: `generate-query-button`
  - class: `secondary-button` (same as Upload Data button)
  - text: "Generate Query"
  - Position it using `justify-content: space-between` on the `.query-controls` parent
- Update `.query-controls` CSS to use `justify-content: space-between` so the Generate Query button is separated from the primary buttons

### 7. Add CSS Styling
- Open `app/client/src/style.css`
- Modify `.query-controls` to add `justify-content: space-between` so buttons are spaced apart
- Ensure the new button aligns with the existing secondary button styles
- No additional styles should be needed since we're reusing `.secondary-button`

### 8. Implement Button Click Handler
- Open `app/client/src/main.ts`
- In `initializeQueryInput()` function, add event listener for the generate query button
- Click handler logic:
  - Disable the button and show loading state
  - Call `api.generateQuery()`
  - If successful, overwrite the query input field value with `response.query`
  - If error, call `displayError()` with the error message
  - Re-enable the button after completion
  - Add appropriate loading indicator (e.g., spinner or text change)
- Ensure proper error handling and user feedback

### 9. Create E2E Test
- Read `.claude/commands/test_e2e.md` and `.claude/commands/e2e/test_basic_query.md` to understand the E2E test format
- Create new file `.claude/commands/e2e/test_query_generator.md`
- Test should validate:
  - User Story: "As a user, I want to generate interesting queries, so that I can explore my data quickly"
  - Test Steps:
    1. Navigate to application
    2. Upload sample data (users.json)
    3. Verify "Generate Query" button is visible
    4. Click "Generate Query" button
    5. Verify query input field is populated with generated text
    6. Verify generated text mentions tables/columns from the schema
    7. Click Query button to execute the generated query
    8. Verify results are displayed successfully
    9. Take screenshots at each major step
  - Success Criteria:
    - Button is visible and clickable
    - Generated query overwrites input field
    - Generated query is 2 sentences or less
    - Generated query can be executed successfully
    - Results display correctly

### 10. Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Fix any issues that arise
- Ensure all tests pass successfully

## Testing Strategy

### Unit Tests
- **Backend Query Generation Function**: Test `generate_natural_language_query()` with various schema configurations:
  - Single table with few columns
  - Multiple tables with relationships
  - Tables with different data types (dates, numbers, text)
  - Verify output is 2 sentences or less
  - Verify output makes sense given the schema

- **API Endpoint**: Test `/api/generate-query` endpoint:
  - Returns 200 with valid query when tables exist
  - Returns error message when no tables exist
  - Handles LLM API failures gracefully
  - Logs appropriate messages

- **Frontend Button Handler**: Test button click handler:
  - Calls API correctly
  - Updates input field on success
  - Displays error on failure
  - Shows loading state during API call
  - Re-enables button after completion

### Edge Cases
- **No tables in database**: Should return friendly error message "No tables available. Please upload data first."
- **Single empty table**: Should generate query that works with empty result sets
- **Very large schema**: Should generate focused query, not trying to reference every table
- **LLM API failure**: Should gracefully handle and display error to user
- **Missing API keys**: Should fall back to available provider or show appropriate error
- **Network timeout**: Should not leave button in disabled state permanently
- **Concurrent clicks**: Should prevent multiple simultaneous API calls
- **Query input already has text**: Should overwrite existing text (as specified in requirements)

## Acceptance Criteria
- [ ] A "Generate Query" button is visible in the query section, styled consistently with the "Upload Data" button
- [ ] The button is positioned separately from the primary "Query" button using justify-content spacing
- [ ] Clicking the button calls the backend API to generate a natural language query
- [ ] The generated query is based on the current database schema (tables, columns, types)
- [ ] The generated query is limited to 2 sentences maximum
- [ ] The generated query overwrites the current value in the query input field
- [ ] The button shows a loading state while waiting for the API response
- [ ] If no tables exist, an appropriate error message is displayed: "No tables available. Please upload data first."
- [ ] If the API fails, an error message is displayed to the user
- [ ] The generated queries are interesting and make sense for the available data
- [ ] The feature works with both OpenAI and Anthropic LLM providers
- [ ] All existing tests continue to pass (zero regressions)
- [ ] E2E test validates the complete user flow

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test `.claude/commands/e2e/test_query_generator.md` to validate the query generation functionality works end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun run tsc --noEmit` - Run frontend type checking to validate TypeScript types are correct
- `cd app/client && bun run build` - Run frontend build to validate the feature builds without errors

## Notes

### LLM Prompt Design
The prompt for query generation should be carefully designed to produce useful results. Suggested prompt structure:

```
Given the following database schema:
[schema details]

Generate an interesting natural language query that a user might ask about this data. The query should:
- Be analytical or exploratory in nature
- Reference actual tables and concepts present in the schema
- Be something that would return useful insights
- Be limited to 2 sentences maximum
- Be phrased as a question or request (e.g., "Show me...", "What are...", "Find all...")

Examples of good queries:
- "Show me all users who signed up in the last month"
- "What are the top 5 products by price?"
- "Find the average order value by customer"

Generate only the natural language query, no explanations or SQL.
```

### Future Enhancements
Consider these potential improvements for future iterations:
- Generate multiple query suggestions and let users choose
- Tailor query complexity based on user expertise level
- Remember previously generated queries to avoid repetition
- Allow users to favorite/save generated queries
- Add query categories (aggregation, filtering, joining, etc.)

### Security Considerations
- The generated queries still go through the normal query execution flow with all SQL injection protections
- Schema information sent to LLM does not include actual data, only metadata
- API keys for LLM providers should remain in environment variables
- Rate limiting may be needed if generation is used excessively

### Cost Considerations
- Each query generation makes an LLM API call (cost per generation)
- Using Haiku (Anthropic) or GPT-4.1-mini (OpenAI) for cost efficiency
- Consider caching generated queries based on schema hash to reduce API calls
- Monitor usage if this feature becomes heavily used
