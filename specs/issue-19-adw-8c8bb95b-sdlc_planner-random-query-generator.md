# Implementation Plan: Random Query Generator Button (Issue #19)

## Summary

This document outlines the complete implementation plan for adding a **"Generate Query" button** to the Natural Language SQL Interface. This feature will enable users to generate interesting, random natural language database queries based on their uploaded data tables, leveraging existing LLM capabilities.

## Feature Description

**Feature**: Add a "Generate Query" button that creates natural language database queries based on existing tables and their structure, using `llm_processor.py` to generate interesting queries (max 2 sentences), styled like the "Upload Data" button.

The button will:
- Appear alongside existing UI controls
- Analyze available database tables and columns
- Generate diverse, realistic queries that exercise the data
- Use the LLM processor to ensure quality and variety
- Display generated queries in the query input field
- Support multiple generations with different results

## User Story

**As a** user of the Natural Language SQL Interface
**I want to** generate random natural language queries for my data
**So that** I can explore my data interactively and understand the system's capabilities

## Problem Statement

Currently, users must manually type natural language queries to test the system. This creates friction for:
- New users learning the system
- Data exploration workflows
- Feature demonstrations
- Understanding what queries are possible with their data

## Solution Statement

Add a "Generate Query" button that automatically generates realistic, diverse natural language queries based on the current database schema. This enables frictionless data exploration and system discovery.

## Implementation Approach

### Phase 1: Foundation & Analysis
- Analyze current application architecture (client/server patterns)
- Understand "Upload Data" button styling and placement conventions
- Map how database schema introspection currently works
- Review `llm_processor.py` capabilities and query generation patterns
- Identify schema access patterns and table metadata availability

### Phase 2: Core Backend Implementation
- Extend `llm_processor.py` with `generate_query_from_schema()` function
- Create `POST /api/generate-query` endpoint that:
  - Accepts selected tables/schema information
  - Returns generated natural language query
  - Includes error handling for edge cases
- Implement database schema introspection:
  - Get available tables
  - Get column names and types for each table
  - Format schema information for LLM context

### Phase 3: Frontend Integration & Polish
- Build React component for "Generate Query" button
- Implement frontend integration:
  - Click handler to fetch generated query
  - Loading state while generating
  - Insert generated query into input field
  - Error handling and user feedback
- Add styling to match "Upload Data" button
- Implement UI feedback (success messages, loading indicators)

## Step-by-Step Implementation Tasks

### Task 1: Analyze Application Architecture
- Review `app/client/src/` structure
- Study how existing buttons trigger API calls
- Understand state management for query input
- Map data flow from UI to backend

### Task 2: Review and Extend `llm_processor.py`
- Analyze existing `llm_processor.py` functions
- Understand current query generation patterns
- Design new `generate_query_from_schema(schema_info)` function
- Add capability to generate diverse, realistic queries
- Implement query validation

### Task 3: Create Backend API Endpoint
- Add `POST /api/generate-query` to `app/server/server.py`
- Accept schema/table information in request
- Call LLM processor to generate query
- Return generated query in response
- Add comprehensive error handling

### Task 4: Implement Database Schema Introspection
- Create utility function to extract schema info
- Get list of available tables
- Get column names and types for selected tables
- Format as structured data for LLM context
- Test with sample databases

### Task 5: Create Frontend Button Component
- Build React button component
- Style to match "Upload Data" button
- Add TypeScript types for props
- Implement click handler skeleton
- Add to appropriate UI location

### Task 6: Implement Frontend API Integration
- Connect button to `/api/generate-query` endpoint
- Implement loading state during generation
- Handle API responses
- Insert generated query into input field
- Add error notifications
- Implement retry logic

### Task 7: Create E2E Test File
- Create `test_random_query_generator.md` in `.claude/commands/e2e/`
- Define comprehensive test scenarios
- Cover happy path and error cases
- Include manual testing steps

### Task 8: Run Validation and Verification
- Execute all test suites
- Verify no regressions in existing functionality
- Test with various database schemas
- Validate generated queries are realistic
- Performance testing with large schemas

## Testing Strategy

### Unit Tests
- **LLM Processor**: Test `generate_query_from_schema()` with various schema inputs
- **Backend Endpoint**: Test `/api/generate-query` with valid/invalid inputs, error cases
- **Frontend Component**: Test button rendering, click handlers, API integration
- **Schema Introspection**: Test schema extraction with different database states

### Integration Tests
- Test complete flow from UI click to generated query
- Verify generated queries can be executed
- Test with multiple tables and complex schemas
- Test error handling across all layers

### E2E Tests
- User scenario: Upload data → Generate query → View results
- Test with different file types (CSV, JSON)
- Test button behavior with no tables loaded
- Verify generated queries are diverse across multiple generations

### Edge Cases
- Empty database schema
- Very large schemas
- LLM timeout or failure
- Network errors
- Concurrent requests
- Special characters in table/column names

## Acceptance Criteria

1. ✅ "Generate Query" button appears in the UI styled like "Upload Data" button
2. ✅ Button triggers API call to generate random query from schema
3. ✅ Generated queries are natural language (max 2 sentences)
4. ✅ Generated queries are contextually relevant to available tables
5. ✅ Multiple generations produce different queries
6. ✅ Generated query appears in the query input field
7. ✅ Button is disabled when no tables are loaded
8. ✅ Loading state displays during query generation
9. ✅ Error messages display if generation fails
10. ✅ All existing tests pass (no regressions)
11. ✅ E2E test file created and passes
12. ✅ Feature works with various database schemas (CSV, JSON)

## Validation Commands

Run these commands to verify feature implementation:

```bash
# Backend tests
cd app/server && uv run pytest tests/ -v

# E2E tests
claude /e2e/test_random_query_generator

# Full validation
cd adws && uv run adw_test.py 19
```

## Files to be Modified/Created

**Modified Files:**
- `app/server/server.py` - Add `/api/generate-query` endpoint
- `app/server/core/llm_processor.py` - Add `generate_query_from_schema()` function
- `app/client/src/main.ts` - Add button to UI

**New Files:**
- `app/server/core/schema_introspection.py` - Schema extraction utilities
- `app/client/src/components/GenerateQueryButton.tsx` - Button component
- `.claude/commands/e2e/test_random_query_generator.md` - E2E test definitions

## Success Metrics

- ✅ Button generates contextually relevant queries
- ✅ Generated queries execute successfully against the data
- ✅ No regressions in existing functionality
- ✅ User can easily discover and use the feature
- ✅ Feature handles all error cases gracefully

## Timeline

**Estimated**: 2-4 hours for complete implementation including:
- Backend development: 1 hour
- Frontend development: 1 hour
- Testing and validation: 1-2 hours

## Dependencies

- Existing LLM processor infrastructure
- React/TypeScript frontend framework
- FastAPI backend
- Current database schema access patterns

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| LLM generates irrelevant queries | Implement schema context enrichment, add query validation |
| Performance with large schemas | Implement caching, limit schema complexity in prompt |
| User confusion about button behavior | Add helpful tooltip/documentation |
| API rate limits | Implement client-side debouncing, rate limiting |

---

**Plan Created**: Issue #19 - Random Query Generator Feature
**ADW ID**: 8c8bb95b
**Status**: Ready for Implementation
