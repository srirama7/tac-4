# Feature: Random Natural Language Query Generator Button

## Feature Description
A button that generates natural language queries based on existing database tables and their structure. When clicked, the button uses the LLM processor to create interesting, contextually relevant query suggestions (limited to two sentences maximum) that users can execute to explore their data. The generated query overwrites any existing content in the input field and is positioned separately from primary buttons using the Upload Data button style.

## User Story
As a user
I want a button that generates example queries based on my data
So that I can discover interesting insights and understand what types of questions I can ask

## Problem Statement
Users often don't know what questions to ask about their data, especially when first loading a dataset. They need inspiration and examples of the types of natural language queries the system can handle. Without query suggestions, users may struggle to utilize the full capabilities of the natural language SQL interface.

## Solution Statement
Implement a "Generate Query" button that:
1. Analyzes the current database schema (tables and columns)
2. Uses the LLM processor to generate contextually relevant natural language queries
3. Limits generated queries to a maximum of two sentences
4. Populates the query input field with the generated query (overwriting existing content)
5. Styles the button consistently with the Upload Data button
6. Positions the button separately (justified apart) from primary buttons

The solution leverages the existing llm_processor.py infrastructure to generate intelligent, table-structure-aware queries that provide meaningful examples for users.

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains LLM integration functions (generate_sql_with_openai, generate_sql_with_anthropic, format_schema_for_prompt). This will be extended to add a new function `generate_random_query()` that creates natural language queries based on table schemas.

- `app/server/core/sql_processor.py` - Contains get_database_schema() function which retrieves current database schema. This will be used to fetch table information for query generation.

- `app/server/core/data_models.py` - Contains Pydantic models for request/response. A new `RandomQueryRequest` and `RandomQueryResponse` model will be added.

- `app/server/server.py` - FastAPI server endpoints. A new `/api/generate-query` endpoint will be added to handle query generation requests.

- `app/client/src/api/client.ts` - Frontend API client. A new `generateRandomQuery()` method will be added.

- `app/client/src/main.ts` - Frontend main logic. Button initialization and click handler will be added to populate the query input field.

- `app/client/index.html` - HTML structure. A new button element will be added in the query-controls section.

- `app/client/src/style.css` - Styling for the button, positioned separately from primary buttons with Upload Data button styling.

- `README.md` - Documentation will be updated to describe the new query generator feature.

### New Files

- `app/server/tests/core/test_query_generator.py` - Unit tests for the random query generation logic

- `.claude/commands/e2e/test_query_generator.md` - E2E test file to validate the query generator button functionality works end-to-end

## Implementation Plan

### Phase 1: Foundation
1. **Backend Data Model Setup**: Create Pydantic models for query generation requests/responses in `data_models.py`
2. **Schema Analysis**: Verify `get_database_schema()` returns sufficient information (table names, column names, types, row counts) for generating contextual queries
3. **LLM Prompt Design**: Design prompts that generate natural language queries (not SQL) limited to two sentences, based on table structure

### Phase 2: Core Implementation
1. **Backend Query Generation Logic**:
   - Implement `generate_random_query()` function in `llm_processor.py`
   - Function analyzes database schema and generates interesting natural language questions
   - Ensures output is limited to two sentences maximum
   - Handles edge cases (no tables, empty tables, single vs. multiple tables)

2. **API Endpoint Creation**:
   - Create `/api/generate-query` POST endpoint in `server.py`
   - Endpoint retrieves schema, calls query generation, returns natural language query
   - Includes error handling and logging

3. **Frontend API Integration**:
   - Add `generateRandomQuery()` method to `api/client.ts`
   - Method calls the new backend endpoint and returns the generated query

4. **UI Button Implementation**:
   - Add "Generate Query" button to `index.html` in the query-controls section
   - Style button in `style.css` matching Upload Data button appearance
   - Position button separately from primary buttons using `justify-content: space-between` or similar
   - Add button initialization in `main.ts`
   - Implement click handler that:
     - Calls API to generate query
     - Overwrites query input field content
     - Shows loading state during generation
     - Handles errors gracefully

### Phase 3: Integration
1. **Testing**: Create unit tests for backend query generation logic and E2E tests for full user flow
2. **Documentation**: Update README.md with the new feature description
3. **Validation**: Run all validation commands to ensure zero regressions

## Step by Step Tasks

### Task 1: Create Backend Data Models
- Add `RandomQueryRequest` model to `app/server/core/data_models.py` (optional parameters for targeting specific tables)
- Add `RandomQueryResponse` model with `query` string field and optional error field
- Ensure models follow existing patterns in the file

### Task 2: Implement Query Generation Function
- Add `generate_random_query()` function to `app/server/core/llm_processor.py`
- Function signature: `generate_random_query(schema_info: Dict[str, Any]) -> str`
- Use existing LLM routing logic (OpenAI priority, then Anthropic)
- Create prompts that generate natural language queries (NOT SQL)
- Enforce two-sentence maximum constraint in the prompt
- Generate contextually relevant queries based on table structure:
  - For single table: queries about specific columns, aggregations, filters
  - For multiple tables: queries involving joins, comparisons across tables
  - Consider column types (dates, numbers, text) for more intelligent suggestions
- Handle edge cases: no tables, empty schema
- Add error handling and logging

### Task 3: Create API Endpoint
- Add `/api/generate-query` POST endpoint to `app/server/server.py`
- Endpoint handler:
  - Calls `get_database_schema()` to retrieve current schema
  - Calls `generate_random_query()` with schema information
  - Returns `RandomQueryResponse` with generated query
  - Includes comprehensive error handling and logging
- Add endpoint to API documentation docstring

### Task 4: Create Unit Tests
- Create `app/server/tests/core/test_query_generator.py`
- Test cases:
  - Test query generation with single table
  - Test query generation with multiple tables
  - Test query generation with no tables (should handle gracefully)
  - Test two-sentence maximum constraint
  - Test with different column types (dates, numbers, text)
  - Mock LLM responses to avoid actual API calls
- Follow existing test patterns from `test_llm_processor.py`

### Task 5: Add Frontend API Client Method
- Add `generateRandomQuery()` method to `app/client/src/api/client.ts`
- Method should call `/api/generate-query` endpoint
- Return type: `Promise<RandomQueryResponse>`
- Follow existing patterns in the file (error handling, typing)

### Task 6: Update Frontend HTML
- Add "Generate Query" button to `app/client/index.html`
- Place button in `.query-controls` div after the Upload Data button
- Button ID: `generate-query-button`
- Button class: `secondary-button`
- Button text: "Generate Query"

### Task 7: Style the Button
- Update `app/client/src/style.css`
- Ensure `.query-controls` uses `justify-content: space-between` to separate buttons
- Verify button uses existing `secondary-button` class (matches Upload Data button style)
- Ensure responsive layout works with the new button

### Task 8: Implement Frontend Button Logic
- Update `app/client/src/main.ts`
- Create `initializeQueryGenerator()` function
- Add button click handler that:
  - Shows loading state (disable button, show loading spinner)
  - Calls `api.generateRandomQuery()`
  - Overwrites query input field with generated query (using `.value = generatedQuery`)
  - Removes loading state
  - Handles errors with `displayError()`
- Call `initializeQueryGenerator()` in DOMContentLoaded event

### Task 9: Create E2E Test File
- Create `.claude/commands/e2e/test_query_generator.md`
- Follow the format from `test_basic_query.md`
- Test steps should include:
  1. Navigate to application
  2. Verify Generate Query button is present
  3. Upload sample data (users.json)
  4. Click Generate Query button
  5. Verify query input field is populated with a query
  6. Verify query is two sentences or less
  7. Take screenshots at each step
  8. Execute the generated query to verify it's valid
  9. Verify results display correctly
- Include success criteria for all verification steps

### Task 10: Update Documentation
- Update `README.md` Features section
- Add bullet point: "🎲 Random query generator for data exploration"
- Update Usage section to describe the Generate Query button
- Example: "5. **Generate Query**: Click 'Generate Query' to get AI-suggested queries based on your data"

### Task 11: Run Validation Commands
- Execute all validation commands listed below
- Fix any regressions or failures
- Ensure all tests pass
- Verify E2E test passes

## Testing Strategy

### Unit Tests
- **Backend Query Generation Tests** (`test_query_generator.py`):
  - Test with empty database (no tables)
  - Test with single table (various column types)
  - Test with multiple tables
  - Test two-sentence constraint enforcement
  - Test error handling (LLM API failures)
  - Mock LLM API responses to avoid actual API calls

- **API Endpoint Tests**:
  - Test successful query generation
  - Test error responses when schema is empty
  - Test error responses when LLM fails

### Integration Tests
- Test that frontend button triggers backend endpoint correctly
- Test that generated query appears in input field
- Test loading states and error handling

### E2E Tests
- Full user flow: Load data → Click Generate Query → Query appears → Execute query → Results display
- Test multiple query generations (different queries each time)
- Test with different datasets (users, products, events)

### Edge Cases
1. **No tables loaded**: Button should be disabled or show helpful message
2. **Empty tables**: Query should still be generated but acknowledge low data
3. **Single vs multiple tables**: Different query strategies
4. **Special characters in table/column names**: Ensure proper handling
5. **LLM API failure**: Graceful error message to user
6. **Very long table/column names**: Ensure prompt doesn't exceed token limits
7. **Query input already has content**: Confirm overwrite behavior is intentional

## Acceptance Criteria
- [ ] Generate Query button is visible and styled like Upload Data button
- [ ] Button is positioned separately from Query button (space-between layout)
- [ ] Clicking button generates a natural language query (NOT SQL)
- [ ] Generated query is limited to two sentences maximum
- [ ] Generated query is contextually relevant to current database schema
- [ ] Query overwrites existing content in input field
- [ ] Loading state is shown during generation
- [ ] Errors are handled gracefully with user-friendly messages
- [ ] Button works with no tables loaded (shows appropriate message/disabled state)
- [ ] Button works with single table
- [ ] Button works with multiple tables
- [ ] Generated queries are executable (can be submitted via Query button)
- [ ] All unit tests pass
- [ ] E2E test passes
- [ ] No regressions in existing functionality
- [ ] README documentation is updated
- [ ] Feature works with both OpenAI and Anthropic LLM providers

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

1. Read `.claude/commands/test_e2e.md`, then read and execute the new `.claude/commands/e2e/test_query_generator.md` E2E test file to validate this functionality works end-to-end.

2. `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run new query generator unit tests

3. `cd app/server && uv run pytest tests/core/test_llm_processor.py -v` - Verify existing LLM processor tests still pass

4. `cd app/server && uv run pytest` - Run all server tests to validate zero regressions

5. `cd app/client && bun tsc --noEmit` - Run TypeScript type checking to ensure no type errors

6. `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

7. Manual validation steps:
   - Start the application (`./scripts/start.sh`)
   - Upload sample data (users.json)
   - Click "Generate Query" button
   - Verify generated query appears in input field
   - Verify query is two sentences or less
   - Click "Query" button to execute the generated query
   - Verify results display correctly
   - Repeat with multiple clicks to ensure different queries are generated
   - Test with different datasets (products.csv, events.jsonl)
   - Test with no tables loaded

## Notes

### LLM Prompt Design Considerations
The prompt for query generation should:
- Clearly instruct to generate natural language (NOT SQL)
- Enforce two-sentence maximum
- Provide table and column information for context
- Request "interesting" queries that showcase different SQL capabilities (aggregations, filters, joins, date operations)
- Vary query complexity based on data structure
- Avoid generating the same query repeatedly (include randomness instruction)

Example prompt structure:
```
Given the following database schema:
[formatted schema with tables, columns, types, row counts]

Generate a single interesting natural language query that a user might ask about this data.
Rules:
- Generate ONLY a natural language question (NOT SQL)
- Maximum two sentences
- Make it interesting and showcase the data's potential insights
- Vary between different types of queries (aggregations, filters, comparisons, time-based, joins)
- Be specific to the actual tables and columns available
```

### Future Enhancements
- Add query history/favorites
- Add multiple query suggestions at once
- Add difficulty levels (simple, intermediate, complex)
- Add category-based generation (aggregations, time-series, comparisons)
- Add ability to regenerate if user doesn't like the suggestion
- Add "pin" functionality to save favorite generated queries
- Add keyboard shortcut for quick generation

### Performance Considerations
- Query generation makes an LLM API call (200-500ms typical latency)
- Show loading state immediately to manage user expectations
- Consider caching recent queries to avoid repeated generations
- Schema should be fetched efficiently (already cached in frontend)

### Accessibility
- Ensure button has proper ARIA labels
- Keyboard navigation should work (Tab to button, Enter to activate)
- Screen reader should announce when query is generated
- Loading state should be announced to screen readers

### Security
- No SQL injection risk (generates natural language, not SQL)
- Rate limiting may be needed if users spam the button
- LLM responses should be sanitized (though natural language has low risk)
- API keys already secured via environment variables
