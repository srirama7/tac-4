# Feature: Natural Language Query Generator Button

## Feature Description
Add a new button to the Natural Language SQL Interface that automatically generates interesting natural language queries based on the existing database tables and their structure. When clicked, this button will use the LLM to create sample queries that showcase what users can ask about their data, then populate the query input field with these generated queries. The button will be positioned separately from the primary action buttons (Query and Upload Data) and will use the Upload Data button style for visual consistency.

## User Story
As a user
I want to get suggested natural language queries based on my loaded tables
So that I can discover interesting questions to ask about my data without having to think of queries myself

## Problem Statement
Users who upload data to the Natural Language SQL Interface may not immediately know what types of questions they can ask about their data. This creates a blank slate problem where users stare at an empty query input field without inspiration. Additionally, users unfamiliar with their data structure might not know what interesting patterns or insights exist within their tables. A query suggestion feature would help users:
- Discover what types of questions are possible
- Learn about their data structure through example queries
- Get started quickly with meaningful analysis
- Understand the capabilities of the natural language interface

## Solution Statement
We will implement a "Generate Query" button that leverages the existing `llm_processor.py` module to create contextual, table-aware natural language query suggestions. The button will:
1. Analyze the current database schema (tables, columns, data types, row counts)
2. Send this structure to the LLM with a prompt to generate an interesting natural language query
3. Limit the generated query to two sentences maximum
4. Automatically populate (overwrite) the query input field with the generated query
5. Be styled consistently with the Upload Data button (secondary-button style)
6. Be positioned with `justify-content: space-between` to separate it from primary action buttons

This approach reuses existing LLM infrastructure, maintains UI consistency, and provides immediate value to users exploring their data.

## Relevant Files
Use these files to implement the feature:

- **app/server/core/llm_processor.py** - Contains the LLM integration functions (`generate_sql_with_openai`, `generate_sql_with_anthropic`, `format_schema_for_prompt`). We'll add a new function `generate_natural_language_query` that creates interesting query suggestions based on table schemas.

- **app/server/core/data_models.py** - Contains Pydantic models for API requests/responses. We'll add `NLQueryGeneratorRequest` and `NLQueryGeneratorResponse` models to handle the new endpoint.

- **app/server/server.py** - The FastAPI server. We'll add a new POST endpoint `/api/generate-nl-query` that receives table schema information and returns a generated natural language query.

- **app/server/core/sql_processor.py** - Contains the `get_database_schema()` function that we'll use to fetch table structures for context.

- **app/client/src/types.d.ts** - TypeScript type definitions. We'll add corresponding TypeScript interfaces for the new API request/response types.

- **app/client/src/api/client.ts** - API client functions. We'll add a `generateNLQuery()` method to call the new backend endpoint.

- **app/client/src/main.ts** - Main frontend logic. We'll add event handlers for the new Generate Query button and logic to populate the query input field.

- **app/client/index.html** - HTML structure. We'll add the new Generate Query button to the query controls section.

- **app/client/src/style.css** - Styling. We'll ensure the button uses the secondary-button style and update the query-controls layout to use `justify-content: space-between`.

- **.claude/commands/test_e2e.md** - E2E test runner reference for understanding how to create E2E tests.

- **.claude/commands/e2e/test_basic_query.md** - Example E2E test structure to follow when creating the new test.

### New Files

- **app/server/tests/core/test_nl_query_generator.py** - Unit tests for the natural language query generation functionality.

- **.claude/commands/e2e/test_nl_query_generator.md** - E2E test file to validate the Generate Query button works end-to-end, including UI interaction, API call, and input field population.

## Implementation Plan

### Phase 1: Foundation
1. Add new Pydantic models to `app/server/core/data_models.py` for request/response handling
2. Create a new function in `app/server/core/llm_processor.py` to generate natural language queries based on schema
3. Add corresponding TypeScript interfaces to `app/client/src/types.d.ts`
4. Write unit tests for the new LLM processor function

### Phase 2: Core Implementation
1. Implement the FastAPI endpoint `/api/generate-nl-query` in `app/server/server.py`
2. Add the API client method in `app/client/src/api/client.ts`
3. Update the HTML to include the Generate Query button in `app/client/index.html`
4. Update CSS to style the button and adjust layout in `app/client/src/style.css`
5. Implement the button click handler and input population logic in `app/client/src/main.ts`

### Phase 3: Integration
1. Test the feature end-to-end manually to ensure proper integration
2. Create the E2E test specification in `.claude/commands/e2e/test_nl_query_generator.md`
3. Run all validation commands to ensure zero regressions
4. Verify the button works with both empty databases and databases with multiple tables

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Backend Data Models
- Open `app/server/core/data_models.py`
- Add `NLQueryGeneratorRequest` model (empty or with optional llm_provider field)
- Add `NLQueryGeneratorResponse` model with fields: `generated_query` (str), `table_count` (int), `error` (Optional[str])

### Step 2: Implement LLM Query Generator Function
- Open `app/server/core/llm_processor.py`
- Add function `generate_natural_language_query(schema_info: Dict[str, Any], llm_provider: str = "openai") -> str`
- Create a prompt that asks the LLM to generate an interesting 1-2 sentence natural language query based on the provided tables and columns
- Reuse the existing `format_schema_for_prompt` helper function
- Handle both OpenAI and Anthropic providers using the existing pattern
- Ensure the prompt instructs the LLM to return ONLY the natural language query text (no SQL, no explanations)
- Add error handling for missing API keys

### Step 3: Write Unit Tests for Query Generator
- Create `app/server/tests/core/test_nl_query_generator.py`
- Write tests for `generate_natural_language_query` function
- Test with mock schema data
- Test error handling for missing API keys
- Test response format validation (ensure 2 sentences or less)

### Step 4: Add Backend API Endpoint
- Open `app/server/server.py`
- Import the new data models and generator function
- Add POST endpoint `/api/generate-nl-query` with response model `NLQueryGeneratorResponse`
- Get database schema using `get_database_schema()`
- If no tables exist, return error: "No tables available. Please upload data first."
- Call `generate_natural_language_query()` with schema info
- Return response with generated query and table count
- Add proper error handling and logging

### Step 5: Add Frontend Type Definitions
- Open `app/client/src/types.d.ts`
- Add `NLQueryGeneratorRequest` interface
- Add `NLQueryGeneratorResponse` interface with fields matching backend models

### Step 6: Add Frontend API Client Method
- Open `app/client/src/api/client.ts`
- Add method `generateNLQuery(): Promise<NLQueryGeneratorResponse>`
- Use POST request to `/generate-nl-query`

### Step 7: Update HTML Structure
- Open `app/client/index.html`
- Add a new button `<button id="generate-query-button" class="secondary-button">Generate Query</button>` in the `.query-controls` div
- Position it after the Upload Data button

### Step 8: Update CSS Styling
- Open `app/client/src/style.css`
- Update `.query-controls` to use `justify-content: space-between` for proper spacing
- Ensure the Generate Query button uses the existing `.secondary-button` class

### Step 9: Implement Frontend Logic
- Open `app/client/src/main.ts`
- Add `initializeGenerateQuery()` function
- Get references to the generate query button and query input field
- Add click event listener to the button
- On click: disable button, show loading state, call `api.generateNLQuery()`
- On success: overwrite the query input value with the generated query
- On error: display error message using existing `displayError()` function
- Re-enable button after completion
- Call `initializeGenerateQuery()` from the DOMContentLoaded event

### Step 10: Create E2E Test Specification
- Create `.claude/commands/e2e/test_nl_query_generator.md`
- Follow the format from `test_basic_query.md`
- Add user story: "As a user, I want to generate sample queries based on my data so that I can discover interesting questions to ask"
- Add test steps:
  1. Navigate to application
  2. Verify Generate Query button is present
  3. Upload sample data (users.json)
  4. Click Generate Query button
  5. Verify query input field is populated with a natural language query
  6. Verify the query is 2 sentences or less
  7. Take screenshot of populated query
  8. Click the Query button to execute the generated query
  9. Verify results are returned successfully
  10. Take screenshot of results
- Add success criteria: button works, input is populated, query executes successfully, 2 screenshots taken

### Step 11: Run Validation Commands
- Execute all commands in the Validation Commands section to validate the feature works with zero regressions

## Testing Strategy

### Unit Tests
- **test_nl_query_generator.py**: Test the `generate_natural_language_query()` function with various schema configurations
  - Test with single table schema
  - Test with multiple tables
  - Test with empty schema (should handle gracefully)
  - Test with different column types (TEXT, INTEGER, REAL, DATE)
  - Mock LLM API calls to ensure consistent testing
  - Verify query length is reasonable (not exceeding 2 sentences)
  - Test both OpenAI and Anthropic providers

### Edge Cases
- **No tables in database**: Should return user-friendly error message "No tables available. Please upload data first."
- **API key not configured**: Should return appropriate error message about missing API key
- **LLM returns invalid format**: Should handle gracefully and provide fallback or error
- **Network timeout**: Should show error and re-enable button
- **Multiple rapid clicks**: Button should be disabled during processing to prevent duplicate requests
- **Very large schema (many tables)**: Should handle gracefully without exceeding token limits
- **Empty tables (0 rows)**: Should still generate queries but note limited data
- **Special characters in table/column names**: Should properly format schema for LLM prompt

## Acceptance Criteria
- [ ] New "Generate Query" button appears in the query controls section, visually separated from Query and Upload Data buttons
- [ ] Button uses the secondary-button style (white background, primary color border)
- [ ] Button is positioned using `justify-content: space-between` layout
- [ ] Clicking the button when no tables exist shows error: "No tables available. Please upload data first."
- [ ] Clicking the button with tables loaded generates a natural language query in 1-2 sentences
- [ ] Generated query overwrites any existing text in the query input field
- [ ] Button shows loading state while generating query
- [ ] Button is disabled during query generation to prevent duplicate requests
- [ ] Generated queries are contextually relevant to the loaded tables and columns
- [ ] Generated queries can be successfully executed by clicking the Query button
- [ ] Error handling works for missing API keys and network failures
- [ ] All existing tests pass with zero regressions
- [ ] New unit tests achieve >90% code coverage for new functionality
- [ ] E2E test validates the complete user workflow

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

**Read E2E test documentation and create E2E test file:**
- Read `.claude/commands/test_e2e.md` to understand E2E testing framework
- Read `.claude/commands/e2e/test_basic_query.md` to understand test file structure
- Verify `.claude/commands/e2e/test_nl_query_generator.md` was created with proper test steps

**Run backend unit tests:**
- `cd app/server && uv run pytest` - Run all server tests including new query generator tests to validate backend functionality works with zero regressions

**Run backend tests for new feature:**
- `cd app/server && uv run pytest tests/core/test_nl_query_generator.py -v` - Run specific tests for the natural language query generator

**Run frontend type checking:**
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript type checking to validate the feature works with zero regressions

**Run frontend build:**
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

**Execute E2E test:**
- Read `.claude/commands/test_e2e.md`
- Read `.claude/commands/e2e/test_nl_query_generator.md`
- Execute the E2E test to validate the Generate Query button works end-to-end

## Notes

### Implementation Details
- Reuse the existing LLM provider routing logic from `generate_sql()` - prioritize OpenAI if available, fallback to Anthropic
- The prompt should ask the LLM to generate creative, diverse queries that showcase different types of analysis (aggregations, filters, joins, date ranges, etc.)
- Consider caching schema information client-side to reduce API calls, but ensure it refreshes when tables are added/removed
- The button should be accessible via keyboard navigation

### Future Enhancements
- Add a "Surprise Me" mode that cycles through different types of queries (simple filters, aggregations, multi-table joins)
- Allow users to save favorite generated queries
- Add a history of generated queries
- Support generating multiple query suggestions at once
- Add the ability to regenerate a different query without uploading new data
- Consider adding query complexity levels (simple, intermediate, advanced)

### LLM Prompt Design
The prompt for generating natural language queries should:
- Emphasize generating interesting, insightful questions
- Encourage variety (don't always generate the same type of query)
- Request queries that demonstrate SQL capabilities (JOINs, aggregations, WHERE clauses, etc.)
- Ensure queries are specific to the actual column names and table names in the schema
- Limit output to 1-2 sentences maximum
- Avoid technical jargon - use plain, conversational language

Example prompt structure:
```
Given the following database schema:

[formatted schema here]

Generate ONE interesting natural language question that a user might ask about this data. The question should:
- Be 1-2 sentences maximum
- Use plain, conversational language
- Demonstrate interesting analysis (aggregations, filters, comparisons, or joins)
- Reference actual table and column names from the schema
- Be specific and actionable

Return ONLY the natural language question, no SQL, no explanations.
```
