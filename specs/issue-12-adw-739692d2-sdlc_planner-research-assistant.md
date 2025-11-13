# Feature: AI-Powered Research Assistant (Colligence Research)

## Feature Description
An intelligent research assistant that leverages collective intelligence (colligence) to help users explore, analyze, and understand their data through AI-powered insights. This feature provides automated data analysis, discovers hidden patterns and relationships between tables, generates comprehensive research reports, and suggests relevant follow-up queries to enable deeper data exploration.

The Research Assistant acts as a collaborative intelligence layer that augments the user's data exploration capabilities by:
- Automatically analyzing table relationships and suggesting meaningful JOIN queries
- Generating comprehensive research reports summarizing key findings across all tables
- Providing contextual query suggestions based on the current data landscape
- Identifying anomalies, trends, and interesting patterns worth investigating
- Creating a research session history that builds on previous discoveries

## User Story
As a data analyst or researcher
I want an AI-powered research assistant that automatically analyzes my data and suggests insights
So that I can discover hidden patterns, relationships, and valuable information without manually writing complex queries or knowing SQL

## Problem Statement
Currently, users must manually:
1. Write their own natural language queries or SQL without guidance
2. Understand table relationships and structure to perform multi-table analysis
3. Remember previous queries and manually build on past discoveries
4. Identify interesting patterns or anomalies through trial and error
5. Generate their own insights without AI-powered recommendations

This creates barriers for non-technical users and slows down the research process, limiting the application's value for exploratory data analysis and research workflows.

## Solution Statement
Implement an AI-powered Research Assistant panel that:
1. Analyzes the database schema to understand table relationships automatically
2. Generates intelligent research reports highlighting key findings, patterns, and anomalies
3. Suggests contextual queries based on available data and previous exploration
4. Provides one-click query execution for suggested research paths
5. Maintains a research session showing the progression of discoveries
6. Uses LLM capabilities to provide natural language summaries and insights

The solution integrates seamlessly with existing query functionality while adding a new research-focused workflow that guides users through data exploration.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py:1-280` - Main FastAPI application; add new `/api/research/*` endpoints for research assistant functionality
- `app/server/core/llm_processor.py:1-162` - LLM integration module; extend to support research report generation and query suggestion
- `app/server/core/sql_processor.py:1-117` - SQL execution module; use for analyzing table relationships and executing research queries
- `app/server/core/insights.py:1-124` - Data insights module; extend to support cross-table analysis and pattern detection
- `app/server/core/data_models.py:1-82` - Pydantic models; add new models for research requests/responses
- `app/client/src/main.ts:1-423` - Main client application; add research panel UI and interactions
- `app/client/src/api/client.ts` - API client; add research endpoint methods
- `app/client/src/style.css` - CSS styles; add research panel styling
- `app/client/index.html` - HTML template; add research panel HTML structure
- `README.md:1-264` - Project documentation; update with research assistant feature description

### New Files
- `app/server/core/research.py` - New module for research assistant logic (relationship discovery, report generation, query suggestions)
- `app/server/tests/core/test_research.py` - Unit tests for research module
- `app/server/tests/test_research_api.py` - API integration tests for research endpoints
- `.claude/commands/e2e/test_research_assistant.md` - E2E test specification for research assistant feature

## Implementation Plan

### Phase 1: Foundation
1. Create the core research module (`app/server/core/research.py`) with functions for:
   - Table relationship discovery (analyze foreign key patterns, common column names)
   - Data pattern detection (identify trends, anomalies, distributions)
   - Query suggestion generation based on schema and existing data

2. Define new Pydantic models in `app/server/core/data_models.py`:
   - `ResearchReportRequest` - Request parameters for generating research reports
   - `ResearchReportResponse` - Comprehensive research findings and insights
   - `QuerySuggestion` - Model for suggested queries with rationale
   - `TableRelationship` - Model for discovered table relationships
   - `ResearchSessionItem` - Model for tracking research exploration history

3. Extend `app/server/core/llm_processor.py` to support:
   - Research report generation using LLM with schema and data samples
   - Intelligent query suggestion based on current database state
   - Natural language summaries of complex data patterns

### Phase 2: Core Implementation
1. Implement backend API endpoints in `app/server/server.py`:
   - `POST /api/research/report` - Generate comprehensive research report
   - `POST /api/research/suggest-queries` - Get intelligent query suggestions
   - `GET /api/research/relationships` - Discover table relationships
   - `POST /api/research/execute-suggestion` - Execute a suggested query and add to session

2. Build the Research Assistant panel in the client:
   - Create collapsible research panel in `app/client/index.html`
   - Add research panel initialization and event handlers in `app/client/src/main.ts`
   - Implement research API calls in `app/client/src/api/client.ts`
   - Style the research panel with modern, intuitive design in `app/client/src/style.css`

3. Implement research workflow:
   - "Generate Research Report" button that analyzes all tables
   - Query suggestions list with one-click execution
   - Research session history showing exploration path
   - Relationship visualization (text-based list with descriptions)

### Phase 3: Integration
1. Integrate research panel with existing query functionality:
   - When user executes suggested query, populate main query input
   - Add research findings to results display context
   - Link table relationship discoveries to schema display

2. Add research session persistence:
   - Track user's research exploration within the browser session
   - Show progression of discoveries and insights
   - Allow users to revisit previous research queries

3. Enhance user experience:
   - Add loading states for research report generation
   - Provide clear explanations of discovered relationships
   - Enable copy-to-clipboard for insights and suggestions

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Core Research Module
- Create `app/server/core/research.py` with foundational functions:
  - `discover_table_relationships()` - Analyze schema to find potential foreign key relationships
  - `detect_data_patterns()` - Identify interesting patterns in numeric/text columns
  - `generate_relationship_queries()` - Create JOIN queries based on discovered relationships
  - `analyze_data_quality()` - Check for nulls, duplicates, data type consistency

### Step 2: Add Research Data Models
- Update `app/server/core/data_models.py` to add:
  - `TableRelationship` model with source/target tables and relationship type
  - `QuerySuggestion` model with query text, rationale, and category
  - `ResearchReportRequest` model with optional focus areas
  - `ResearchReportResponse` model with insights, suggestions, and relationships
  - `DataPattern` model for identified patterns (trends, anomalies, distributions)

### Step 3: Extend LLM Processor for Research
- Update `app/server/core/llm_processor.py` to add:
  - `generate_research_report()` - Use LLM to create comprehensive data analysis
  - `generate_query_suggestions()` - Use LLM to suggest interesting queries
  - `summarize_table_relationships()` - Create natural language relationship descriptions
  - Include schema, sample data, and discovered patterns in LLM prompts

### Step 4: Implement Research API Endpoints
- Update `app/server/server.py` to add research endpoints:
  - `POST /api/research/report` - Generate full research report
  - `POST /api/research/suggest-queries` - Get 5-10 intelligent query suggestions
  - `GET /api/research/relationships` - Return discovered table relationships
  - Include comprehensive error handling and logging for each endpoint

### Step 5: Create Research Panel HTML Structure
- Update `app/client/index.html` to add:
  - Research panel section with collapsible design
  - "Generate Research Report" button
  - Section for displaying research insights
  - Section for query suggestions with execute buttons
  - Section for table relationships
  - Research session history container

### Step 6: Implement Research Panel Client Logic
- Update `app/client/src/main.ts` to add:
  - `initializeResearchPanel()` - Set up research panel event handlers
  - `generateResearchReport()` - Call research API and display results
  - `displayQuerySuggestions()` - Render suggestions with execute buttons
  - `displayTableRelationships()` - Show discovered relationships
  - `executeSuggestedQuery()` - Run suggestion and update session history
  - Call `initializeResearchPanel()` from DOMContentLoaded

### Step 7: Add Research API Client Methods
- Update `app/client/src/api/client.ts` to add:
  - `generateResearchReport()` method
  - `getSuggestedQueries()` method
  - `getTableRelationships()` method
  - Export methods in api object

### Step 8: Style Research Panel
- Update `app/client/src/style.css` to add:
  - `.research-panel` - Main panel container styling
  - `.research-section` - Individual section styling (insights, suggestions, relationships)
  - `.query-suggestion` - Suggestion card with hover effects
  - `.suggestion-execute-btn` - Execute button styling
  - `.relationship-item` - Relationship display styling
  - `.research-session-item` - Session history item styling
  - Ensure responsive design and accessibility

### Step 9: Create E2E Test Specification
- Create `.claude/commands/e2e/test_research_assistant.md` with:
  - Test steps to verify research panel initialization
  - Test steps to generate research report and verify insights appear
  - Test steps to execute suggested query and verify results
  - Test steps to view table relationships
  - Screenshot capture at each major step
  - Success criteria validating all features work correctly

### Step 10: Write Unit Tests
- Create `app/server/tests/core/test_research.py` with tests for:
  - Table relationship discovery with sample schemas
  - Data pattern detection with sample datasets
  - Query suggestion generation
  - Data quality analysis
  - Edge cases (empty tables, single table, no relationships)

### Step 11: Write API Integration Tests
- Create `app/server/tests/test_research_api.py` with tests for:
  - Research report generation endpoint
  - Query suggestion endpoint
  - Table relationships endpoint
  - Error handling (no tables, invalid requests)
  - Response structure validation

### Step 12: Update Documentation
- Update `README.md` to document:
  - Research Assistant feature description
  - How to use the research panel
  - Example research workflows
  - API endpoints for research functionality

### Step 13: Run Validation Commands
- Execute all validation commands to ensure feature works correctly:
  - Run server tests: `cd app/server && uv run pytest`
  - Run type checking: `cd app/client && bun tsc --noEmit`
  - Run build: `cd app/client && bun run build`
  - Read and execute E2E test: `.claude/commands/e2e/test_research_assistant.md`
  - Verify zero regressions in existing functionality

## Testing Strategy

### Unit Tests
- Test `discover_table_relationships()` with various schema configurations:
  - Tables with matching column names (e.g., `user_id` in multiple tables)
  - Tables with no obvious relationships
  - Single table database
  - Multiple potential relationship paths

- Test `detect_data_patterns()` with diverse datasets:
  - Numeric columns with trends (increasing, decreasing, cyclical)
  - Text columns with common values
  - Date columns with temporal patterns
  - Columns with anomalies (outliers, nulls)

- Test `generate_query_suggestions()` for quality and relevance:
  - Suggestions cover different analysis types (aggregation, filtering, joining)
  - Suggestions are executable SQL
  - Rationale is clear and helpful

- Test LLM integration functions:
  - Mock LLM responses for consistent testing
  - Validate prompt formatting
  - Test error handling for LLM failures

### Integration Tests
- Test research API endpoints end-to-end:
  - Upload sample data (multiple related tables)
  - Generate research report and validate response structure
  - Get query suggestions and verify they're executable
  - Execute suggested queries and verify results
  - Check table relationships are discovered correctly

- Test research workflow in real scenarios:
  - E-commerce dataset (users, products, orders)
  - Event log dataset (events, users, sessions)
  - Single table analytical queries

### Edge Cases
- Empty database (no tables) - should return helpful message
- Single table - should focus on single-table insights
- Very large tables (>10k rows) - should sample data appropriately
- Tables with no obvious relationships - should suggest single-table analyses
- Missing LLM API keys - should provide graceful degradation
- Malformed table/column names - should handle with security validation
- Concurrent research requests - should handle properly
- Browser session persistence - should maintain research history

## Acceptance Criteria
1. Research panel is visible and collapsible in the UI
2. "Generate Research Report" button successfully generates comprehensive insights
3. Research report includes:
   - Summary of all tables and their contents
   - Discovered relationships between tables
   - At least 5 intelligent query suggestions
   - Data quality observations
   - Interesting patterns or anomalies
4. Query suggestions are displayed with clear rationale
5. Clicking a suggestion executes the query and shows results
6. Table relationships are displayed with clear descriptions
7. Research session history tracks user's exploration path
8. All existing functionality continues to work (zero regressions)
9. Research features work with both OpenAI and Anthropic LLM providers
10. Unit tests achieve >80% code coverage for research module
11. E2E test validates complete research workflow
12. Documentation clearly explains how to use the research assistant

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_research_assistant.md` to validate the research assistant functionality works end-to-end with screenshots proving the feature.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes
- This feature significantly enhances the value proposition by moving from reactive (user asks query) to proactive (system suggests insights)
- The research assistant should use sampling for large tables (e.g., LIMIT 100) to avoid performance issues
- Consider adding a configuration option for "depth" of analysis (quick scan vs. deep dive)
- Future enhancement: Allow users to save research sessions and return to them later
- Future enhancement: Add visualization of table relationships (graph/diagram)
- Future enhancement: Export research reports as PDF or markdown
- Future enhancement: Enable natural language conversations about the data ("tell me more about X")
- Security: All research queries must go through existing SQL security validation
- Performance: Research report generation may take 5-15 seconds; ensure good loading UX
- The LLM context for research reports should include schema + sample rows (not entire tables)
- Consider rate limiting research report generation to prevent API cost overruns
- Add telemetry to track which suggestions users find most valuable
