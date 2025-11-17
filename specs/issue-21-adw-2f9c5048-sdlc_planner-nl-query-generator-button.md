# Feature: Natural Language Query Generator Button

## Feature Description
A new button that automatically generates interesting natural language queries based on the existing database tables and their structures. When clicked, the button uses an LLM to analyze the available tables, columns, and data types to create compelling sample queries that users can execute. The generated query will always overwrite the current content in the query input field, providing users with instant query suggestions they can run manually. This feature helps users discover the capabilities of their data without needing to think of queries themselves.

## User Story
As a user
I want a button that generates interesting natural language queries based on my database tables
So that I can quickly explore my data without having to come up with queries myself

## Problem Statement
Users who upload data to the Natural Language SQL Interface may not immediately know what questions to ask about their data. They face a blank query input field and must think of appropriate queries on their own. This creates friction in the user experience, especially for new users or when exploring unfamiliar datasets. Additionally, users may not be aware of the full capabilities of the natural language query system and what types of questions they can ask.

## Solution Statement
Implement a "Generate Query" button positioned next to the existing primary action buttons (Query and Upload Data). This button will use the existing LLM infrastructure to analyze the current database schema and generate creative, contextually relevant natural language queries. The generated queries will be limited to two sentences maximum for brevity and clarity, and will be automatically populated into the query input field, overwriting any existing content. This provides users with instant inspiration and demonstrates the system's capabilities.

## Relevant Files
Use these files to implement the feature:

**Server-side files:**
- `app/server/server.py` - Add new endpoint for query generation
- `app/server/core/data_models.py` - Add Pydantic models for query generation request/response
- `app/server/core/llm_processor.py` - Add function to generate natural language queries based on schema
- `app/server/core/sql_processor.py` - Use existing get_database_schema function to retrieve table structures

**Client-side files:**
- `app/client/src/main.ts` - Add button event handler and API call
- `app/client/src/api/client.ts` - Add API method for query generation
- `app/client/src/types.d.ts` - Add TypeScript interface for query generation response
- `app/client/index.html` - Add the new button to the query controls section
- `app/client/src/style.css` - Add button styling matching the Upload Data button style

**Testing files:**
- `app/server/tests/core/test_llm_processor.py` - Add tests for query generation function
- Read `.claude/commands/test_e2e.md` to understand E2E test execution
- Read `.claude/commands/e2e/test_basic_query.md` to understand E2E test format

### New Files
- `.claude/commands/e2e/test_nl_query_generator.md` - E2E test file to validate the query generator button functionality

## Implementation Plan
### Phase 1: Foundation
Create the backend infrastructure for generating natural language queries. This includes implementing the LLM prompt engineering to analyze database schemas and produce relevant, interesting queries. We'll add the necessary data models and ensure proper error handling for cases where no tables exist.

### Phase 2: Core Implementation
Implement the server-side API endpoint that receives a request, fetches the current database schema, and uses the LLM to generate contextually appropriate natural language queries. The query generation should be intelligent, considering table relationships, column types, and data characteristics to produce meaningful questions.

### Phase 3: Integration
Build the client-side UI component (button) and integrate it with the backend API. Implement the logic to populate the generated query into the input field, handle loading states, and provide user feedback. Create comprehensive E2E tests to validate the feature works as expected.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Add Query Generation Data Models
- Add `QueryGenerationRequest` Pydantic model in `app/server/core/data_models.py` with optional fields for customization (e.g., query_focus, complexity_level)
- Add `QueryGenerationResponse` Pydantic model with fields: generated_query (str), tables_analyzed (List[str]), error (Optional[str])
- Update TypeScript types in `app/client/src/types.d.ts` to match the new response model

### Implement Query Generation Function
- Add `generate_natural_language_query` function to `app/server/core/llm_processor.py`
- Function should accept schema_info (Dict[str, Any]) and return a natural language query string
- Create a comprehensive LLM prompt that:
  - Describes all available tables with their columns and data types
  - Requests generation of an interesting, realistic natural language query
  - Limits output to maximum two sentences
  - Encourages variety (aggregations, filtering, joins, temporal queries, etc.)
  - Ensures queries are executable and meaningful
- Implement for both OpenAI and Anthropic providers using existing pattern
- Add proper error handling and fallback messages
- Ensure the function uses the existing LLM routing logic (OpenAI priority, then Anthropic)

### Add Server Endpoint
- Create `POST /api/generate-query` endpoint in `app/server/server.py`
- Endpoint should:
  - Call `get_database_schema()` to fetch current table structures
  - Return error if no tables exist ("Please upload data first")
  - Call `generate_natural_language_query()` with the schema info
  - Return the generated query in `QueryGenerationResponse` format
  - Log successful query generation and errors
- Add proper exception handling and error responses

### Write Unit Tests for Query Generation
- Add test cases to `app/server/tests/core/test_llm_processor.py`:
  - Test query generation with single table
  - Test query generation with multiple tables
  - Test query generation with various column types (TEXT, INTEGER, REAL, DATE)
  - Test error handling when LLM API fails
  - Test fallback behavior for both OpenAI and Anthropic
  - Mock LLM API calls to avoid real API usage in tests

### Add Client API Method
- Add `generateQuery()` method to `app/client/src/api/client.ts`
- Method should call `POST /api/generate-query` endpoint
- Return properly typed `QueryGenerationResponse`
- Handle network errors and API failures gracefully

### Add Generate Query Button to HTML
- Add new button in `app/client/index.html` in the `.query-controls` div
- Position it using `justify-content: space-between` to separate it from Query and Upload Data buttons
- Button should have:
  - id: "generate-query-button"
  - class: "secondary-button" (matching Upload Data button style)
  - text: "Generate Query"
  - Proper accessibility attributes

### Style the Generate Query Button
- Verify the button uses existing `.secondary-button` styles from `app/client/src/style.css`
- Ensure button is visually distinct but consistent with the Upload Data button
- Add hover and disabled states
- Test responsive layout to ensure all three buttons fit properly on smaller screens

### Implement Button Event Handler
- Add `initializeQueryGenerator()` function in `app/client/src/main.ts`
- Function should:
  - Get reference to the generate-query-button
  - Add click event listener
  - Show loading state (disable button, show loading spinner)
  - Call `api.generateQuery()`
  - On success: overwrite query input field with generated query
  - On error: display error message using existing `displayError()` function
  - Always re-enable button and restore text after completion
- Call `initializeQueryGenerator()` from the DOMContentLoaded event listener
- Ensure the function handles cases where no tables exist with appropriate user feedback

### Create E2E Test File
- Create `.claude/commands/e2e/test_nl_query_generator.md` following the pattern from `test_basic_query.md`
- E2E test should validate:
  - User clicks "Generate Query" button
  - Button shows loading state
  - Query input field is populated with generated query (non-empty)
  - Generated query is two sentences or less
  - Button returns to normal state
  - User can click the Query button to execute the generated query
  - Results are displayed successfully
- Include proper User Story and Success Criteria sections
- Specify screenshot requirements at key steps

### Integration Testing
- Test the full flow from button click to query population
- Verify behavior with no tables (should show error)
- Verify behavior with one table
- Verify behavior with multiple tables
- Test repeated clicks to ensure variety in generated queries
- Verify the generated query overwrites existing input content
- Test with both OpenAI and Anthropic API keys configured

### Error Handling and Edge Cases
- Add user-friendly error message when no tables exist
- Handle LLM API timeout gracefully
- Handle network failures with retry suggestion
- Ensure button cannot be clicked multiple times rapidly (debouncing)
- Test with empty database
- Test with tables that have no data (0 rows)
- Test with very complex schemas (many tables, many columns)

### Documentation and Polish
- Add code comments explaining the query generation logic
- Ensure consistent error messages across client and server
- Verify logging captures useful debugging information
- Test accessibility (keyboard navigation, screen readers)
- Ensure loading states provide clear feedback to users

### Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Fix any issues discovered during validation
- Verify E2E test passes successfully

## Testing Strategy
### Unit Tests
- Test `generate_natural_language_query()` with various schema configurations
- Test endpoint `/api/generate-query` with mocked LLM responses
- Test error conditions: no tables, LLM failure, invalid schema
- Test both OpenAI and Anthropic code paths
- Verify two-sentence limit is enforced
- Test query diversity with repeated calls

### Integration Tests
- Test full client-to-server flow with real database
- Test button interaction and UI state updates
- Test query generation with different table structures
- Test generated queries are actually executable
- Test overwriting existing query input content

### Edge Cases
- No tables in database (should show helpful error)
- Database with single empty table
- Tables with only one column
- Tables with many columns (50+)
- Tables with unusual column names or types
- LLM returns malformed response
- LLM returns query longer than two sentences (should truncate)
- Multiple rapid button clicks
- Network timeout during API call
- Invalid API keys configured

## Acceptance Criteria
- A "Generate Query" button appears in the query controls section, visually separated from Query and Upload Data buttons
- Button uses the same style as the Upload Data button (secondary-button class)
- Clicking the button generates a natural language query based on available tables
- Generated query is automatically populated into the query input field, overwriting any existing content
- Generated queries are limited to two sentences maximum
- Button shows loading state while query is being generated
- Appropriate error message displays if no tables exist
- Generated queries are varied and interesting, utilizing different types of SQL operations
- Feature works with both OpenAI and Anthropic LLM providers
- All existing functionality continues to work without regression
- E2E test validates the complete user flow

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test file `.claude/commands/e2e/test_nl_query_generator.md` to validate this functionality works.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/core/test_llm_processor.py -v` - Run specific LLM processor tests including new query generation tests
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes
- The query generation prompt should be carefully crafted to produce diverse, interesting queries that showcase the system's capabilities
- Consider adding a query focus parameter in future iterations (e.g., "aggregations", "filtering", "time-based")
- Future enhancement could allow users to regenerate queries if they don't like the first suggestion
- The two-sentence limit ensures queries are concise and easy to understand
- Generated queries should avoid overly complex joins that might confuse users
- Consider tracking which generated queries users actually execute to improve the generation algorithm
- The feature should work gracefully even with minimal data (e.g., single table with few rows)
- May want to implement caching to avoid regenerating the same query for the same schema repeatedly
- Consider adding keyboard shortcut for query generation (e.g., Ctrl+G or Cmd+G)
- Future iteration could include a "Surprise Me" mode that picks a random table focus
