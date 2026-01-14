# Feature: Nested JSON Flattening and Schema Validation

## Feature Description
Extend the JSON and JSONL upload capabilities to support deeply nested JSON structures and provide optional JSON schema validation. Currently, the application only handles flat JSON objects (arrays of simple key-value pairs). Real-world JSON data often contains nested objects, arrays, and complex hierarchical structures that are common in API responses, configuration files, and NoSQL database exports. This feature will automatically flatten nested JSON structures into relational table columns using configurable delimiters, and optionally validate data against JSON schemas before import to ensure data quality and consistency.

## User Story
As a data analyst or developer
I want to upload JSON/JSONL files with nested objects and arrays
So that I can query complex API responses, hierarchical data, and nested configurations using natural language without manually flattening the data structure

## Problem Statement
The application currently rejects or mishandles JSON files containing nested objects or arrays. When users upload real-world JSON data from APIs (e.g., `{"user": {"name": "John", "address": {"city": "NYC"}}}`) or NoSQL exports, the pandas DataFrame conversion either fails or stores nested structures as serialized strings, making them unqueryable. This forces users to manually flatten complex JSON structures before upload, which is time-consuming and requires technical expertise. Additionally, there's no way to validate data quality before import, leading to issues with malformed or inconsistent data only being discovered during querying.

## Solution Statement
Implement a recursive JSON flattening algorithm that transforms nested objects into flat column names using configurable delimiters (e.g., `user__address__city`). Arrays will be handled by either creating indexed columns (`items__0`, `items__1`) or expanding into separate rows based on user preference. Add an optional JSON Schema validation step that checks uploaded data against a user-provided schema before conversion, providing clear error messages for validation failures. The solution maintains backward compatibility with existing flat JSON uploads while seamlessly handling complex nested structures. All flattening logic will be centralized in a new `json_utils.py` module to ensure consistency across JSON and JSONL processing.

## Relevant Files
Use these files to implement the feature:

- `app/server/core/file_processor.py:104-174` - Contains `convert_json_to_sqlite` and will contain `convert_jsonl_to_sqlite`. We'll modify both functions to use the new flattening utilities before DataFrame creation, enabling nested structure support for all JSON formats.

- `app/server/core/data_models.py:6-15` - Contains API request/response models. We'll add a new `JSONUploadOptions` model to allow users to configure flattening behavior (delimiter, array handling mode) and optionally provide a JSON schema for validation.

- `app/server/server.py:72-109` - Upload endpoint that processes file uploads. We'll extend this endpoint to accept optional configuration parameters for nested JSON handling and schema validation via request body or query parameters.

- `app/server/core/sql_security.py` - Security utilities used throughout. The flattened column names will pass through the same validation as current column names to prevent SQL injection through nested keys.

- `README.md:8-45` - Documentation of features and usage. We'll add a section explaining nested JSON support, configuration options, and schema validation with examples.

### New Files

- `app/server/core/json_utils.py` - New utility module containing all JSON processing logic:
  - `flatten_json_object(obj, delimiter, array_mode)` - Recursively flattens nested dicts/lists
  - `normalize_schema(records)` - Ensures all records have same fields for consistent DataFrame creation
  - `validate_json_schema(data, schema)` - Validates JSON data against JSON Schema specification
  - `unflatten_column_name(column_name, delimiter)` - Utility to reverse flattening for display purposes (future use)

- `app/server/tests/core/test_json_utils.py` - Comprehensive unit tests for JSON utilities:
  - Test nested object flattening at various depths (2-5 levels)
  - Test array handling in both "index" and "explode" modes
  - Test schema normalization with missing/extra fields
  - Test JSON schema validation with valid/invalid data
  - Test edge cases (circular references, null values, empty objects)

- `app/server/tests/assets/nested_*.json` - Test data files:
  - `nested_simple.json` - 2-level nesting (user with address)
  - `nested_deep.json` - 5-level nesting to test recursion limits
  - `nested_arrays.json` - Objects containing arrays of primitives
  - `nested_array_objects.json` - Arrays of nested objects
  - `schema_valid.json` - Sample JSON Schema definition
  - `schema_invalid_data.json` - Data that fails schema validation

- `app/server/tests/core/test_file_processor_nested.py` - Integration tests for nested JSON upload:
  - Test end-to-end upload of nested JSON via API
  - Test schema validation rejection of invalid data
  - Test querying flattened nested data
  - Test configuration options (different delimiters, array modes)

## Implementation Plan

### Phase 1: Foundation
Before implementing the main feature, establish the JSON processing utilities and testing infrastructure:

1. Create `app/server/core/json_utils.py` with stub functions and comprehensive docstrings
2. Create test asset directory and sample nested JSON test files covering various nesting scenarios
3. Research pandas JSON normalization capabilities (`pd.json_normalize()`) to determine if we should use it or implement custom flattening
4. Review JSON Schema validation libraries (jsonschema, pydantic) and select the most appropriate for our use case
5. Define the configuration schema for flattening options (delimiter choice, array handling mode, max depth)

### Phase 2: Core Implementation
Implement the flattening and validation logic with comprehensive error handling:

1. Implement `flatten_json_object()` function that:
   - Recursively traverses nested dictionaries and lists
   - Builds flattened keys using configurable delimiter (default: `__`)
   - Handles arrays in two modes: "index" (create `key__0`, `key__1` columns) or "explode" (create separate rows)
   - Respects max depth limit to prevent infinite recursion (default: 10 levels)
   - Handles edge cases (None values, empty objects/arrays, mixed types)
   - Returns a flat dictionary

2. Implement `normalize_schema()` function that:
   - Scans all records to discover all unique field names across the dataset
   - Creates normalized records where each has all fields (missing fields = None)
   - Preserves data types and doesn't coerce inappropriately
   - Returns a list of normalized dictionaries ready for DataFrame conversion

3. Implement `validate_json_schema()` function that:
   - Accepts a JSON Schema definition and data to validate
   - Uses jsonschema library to perform validation
   - Returns detailed validation errors with field paths and constraint violations
   - Handles schema validation gracefully (invalid schema returns error)

4. Create comprehensive unit tests in `test_json_utils.py` covering:
   - Simple 2-level nesting (user.address.city)
   - Deep nesting (5+ levels)
   - Arrays of primitives ([1,2,3] → col__0, col__1, col__2)
   - Arrays of objects (explode mode creates new rows)
   - Mixed nesting (objects containing arrays containing objects)
   - Null/None value handling at various levels
   - Empty objects and arrays
   - Schema validation success and failure cases
   - Max depth protection (error when exceeding limit)

### Phase 3: Integration
Integrate flattening and validation into existing file upload workflow:

1. Update `convert_json_to_sqlite()` in `file_processor.py`:
   - Add optional parameters: `flatten=True`, `delimiter='__'`, `array_mode='index'`, `schema=None`
   - Before DataFrame creation, check if flattening is enabled
   - If enabled, apply `flatten_json_object()` to each record in the data list
   - Apply `normalize_schema()` to ensure consistent fields
   - If schema is provided, run `validate_json_schema()` and raise error on failure
   - Then proceed with existing DataFrame conversion logic

2. Update `convert_jsonl_to_sqlite()` (once implemented) with same flattening parameters

3. Update `upload` endpoint in `server.py`:
   - Accept optional JSON configuration in request body alongside file upload
   - Parse configuration: `flatten_nested`, `delimiter`, `array_mode`, `json_schema`
   - Pass these parameters to converter functions
   - Return enhanced error messages for schema validation failures

4. Update `data_models.py`:
   - Add `JSONUploadOptions` Pydantic model with validation for delimiter format, array_mode enum, etc.
   - Update `FileUploadResponse` to include `flattened_columns` count and `validation_errors` list

5. Create integration tests in `test_file_processor_nested.py`:
   - Upload nested JSON through API with flattening enabled
   - Verify flattened column names in table schema
   - Query flattened data using natural language
   - Upload with schema validation enabled and invalid data
   - Verify appropriate error response
   - Test backward compatibility (flat JSON still works)

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Set Up JSON Utilities Module and Test Infrastructure
- Create `app/server/core/json_utils.py` with module docstring explaining purpose
- Add imports: `json`, `typing`, `jsonschema`, `copy` for deep copying
- Create function stubs for `flatten_json_object`, `normalize_schema`, `validate_json_schema` with detailed docstrings
- Create `app/server/tests/core/test_json_utils.py` with pytest imports and test structure
- Create `app/server/tests/assets/` directory if it doesn't exist
- Create sample test files:
  - `nested_simple.json`: Array of 3 user objects with 2-level nesting (name, address.city, address.zip)
  - `nested_deep.json`: Single object with 5 levels of nesting to test depth limits
  - `nested_arrays.json`: Objects containing arrays of primitive values
  - `nested_array_objects.json`: Array of objects where each object contains array of sub-objects
  - `schema_example.json`: Sample JSON Schema defining required user fields

### Step 2: Implement JSON Flattening Logic
- Implement `flatten_json_object(obj, parent_key='', delimiter='__', array_mode='index', max_depth=10, current_depth=0)`:
  - Base case: if `obj` is not dict/list, return `{parent_key: obj}`
  - Recursive case for dict: iterate over key-value pairs, build new keys with delimiter
  - Recursive case for list in "index" mode: enumerate items, create keys like `parent__0`, `parent__1`
  - Recursive case for list in "explode" mode: mark for later expansion (requires different handling)
  - Depth protection: raise error if `current_depth >= max_depth`
  - Handle None/null values appropriately (preserve as None, not flatten further)
  - Return flat dictionary with all leaf values
- Write unit tests for `flatten_json_object`:
  - Test simple nested dict: `{"a": {"b": 1}}` → `{"a__b": 1}`
  - Test 3-level nesting: `{"a": {"b": {"c": 1}}}` → `{"a__b__c": 1}`
  - Test array with index mode: `{"items": [1,2,3]}` → `{"items__0": 1, "items__1": 2, "items__2": 3}`
  - Test custom delimiter: same nested dict with delimiter="." → `{"a.b": 1}`
  - Test max depth exceeded: 11-level nesting should raise error
  - Test mixed types: dict containing string, int, float, bool, null
  - Test empty objects and arrays: `{"a": {}}` → `{}` or `{"a": None}`
- Run tests: `cd app/server && uv run pytest tests/core/test_json_utils.py::test_flatten_json_object -v`

### Step 3: Implement Schema Normalization
- Implement `normalize_schema(records: List[Dict]) -> List[Dict]`:
  - Create set of all unique keys across all records
  - Iterate through records, create new dict with all keys (missing keys get None)
  - Preserve original values where they exist
  - Return list of normalized records with consistent schema
- Write unit tests for `normalize_schema`:
  - Test records with missing fields: `[{"a": 1}, {"b": 2}]` → `[{"a": 1, "b": None}, {"a": None, "b": 2}]`
  - Test records with extra fields: verify all unique fields are captured
  - Test empty records list: return empty list
  - Test single record: should return same record in list
  - Test all records identical: should return unchanged
- Run tests: `cd app/server && uv run pytest tests/core/test_json_utils.py::test_normalize_schema -v`

### Step 4: Implement JSON Schema Validation
- Add `jsonschema` library to dependencies: `cd app/server && uv add jsonschema`
- Implement `validate_json_schema(data: List[Dict], schema: Dict) -> Optional[str]`:
  - Import `jsonschema.validate` and `jsonschema.ValidationError`
  - Iterate through each record in data
  - Call `validate(instance=record, schema=schema)` for each
  - Catch `ValidationError` and return formatted error message with record index
  - If all records valid, return None (no error)
  - Handle invalid schema gracefully (return error about schema itself)
- Write unit tests for `validate_json_schema`:
  - Test valid data against schema: returns None
  - Test invalid data (missing required field): returns error message with details
  - Test invalid data (wrong type): returns error message about type mismatch
  - Test multiple records with one invalid: returns error with record index
  - Test invalid schema definition: returns schema error
  - Test empty data list: should return None (vacuous truth - no records to invalidate)
- Create `app/server/tests/assets/user_schema.json`: JSON Schema requiring fields "id" (integer), "name" (string), "email" (string, email format)
- Create `app/server/tests/assets/invalid_user.json`: User data missing required "email" field
- Run tests: `cd app/server && uv run pytest tests/core/test_json_utils.py::test_validate_json_schema -v`

### Step 5: Update Data Models for Configuration
- Modify `app/server/core/data_models.py`:
  - Add import: `from typing import Literal, Optional`
  - Create `JSONUploadOptions` Pydantic model:
    - `flatten_nested: bool = True` - Whether to flatten nested structures
    - `delimiter: str = Field(default='__', regex=r'^[_\-\.]$')` - Delimiter for flattened keys (must be _, -, or .)
    - `array_mode: Literal['index', 'explode'] = 'index'` - How to handle arrays
    - `max_depth: int = Field(default=10, ge=1, le=20)` - Maximum nesting depth
    - `json_schema: Optional[Dict] = None` - Optional JSON Schema for validation
  - Update `FileUploadResponse` model:
    - Add `flattened_columns: Optional[int] = None` - Count of columns created by flattening
    - Add `validation_errors: Optional[List[str]] = None` - Schema validation errors if any
- Write unit tests for data model validation in existing test file
- Run tests: `cd app/server && uv run pytest tests/test_*.py -k JSONUploadOptions -v`

### Step 6: Integrate Flattening into File Processor
- Modify `app/server/core/file_processor.py`:
  - Import new utilities: `from .json_utils import flatten_json_object, normalize_schema, validate_json_schema`
  - Update `convert_json_to_sqlite` signature to accept `options: Optional[JSONUploadOptions] = None`
  - After parsing JSON array but before DataFrame creation:
    - If `options` is provided and `options.json_schema` exists, validate data
    - If validation fails, raise ValueError with validation error message
    - If `options` is provided and `options.flatten_nested` is True:
      - Apply `flatten_json_object` to each record with provided delimiter and array_mode
      - Apply `normalize_schema` to flattened records
    - Replace original data list with flattened/normalized version
  - Continue with existing DataFrame creation and table insertion logic
  - Update return value to include flattened column count
- Write focused unit tests in existing `test_file_processor.py`:
  - Test nested JSON upload with flattening enabled: verify flattened column names in schema
  - Test nested JSON upload with flattening disabled: verify error or string serialization
  - Test schema validation success: nested JSON passes validation
  - Test schema validation failure: nested JSON fails validation, error returned
  - Test custom delimiter: verify column names use custom delimiter
  - Test backward compatibility: flat JSON still works exactly as before
- Run tests: `cd app/server && uv run pytest tests/core/test_file_processor.py -v`

### Step 7: Update Upload API Endpoint
- Modify `app/server/server.py`:
  - Import `JSONUploadOptions` from `data_models`
  - Update `/api/upload` endpoint to accept optional JSON configuration:
    - Change from simple file upload to multipart with optional config JSON
    - Parse `config` field from request body if present
    - Validate config using `JSONUploadOptions` Pydantic model
    - Pass parsed options to `convert_json_to_sqlite()` and `convert_jsonl_to_sqlite()`
  - Update error handling to include validation errors in response
  - Ensure backward compatibility: requests without config still work with defaults
- Test manually with curl:
  - `curl -F "file=@nested.json" http://localhost:8000/api/upload` - Basic upload
  - `curl -F "file=@nested.json" -F "config={\"flatten_nested\": true}" http://localhost:8000/api/upload` - With config
- Write integration test in new `test_file_processor_nested.py`:
  - Test API upload of nested JSON with default options
  - Test API upload with custom delimiter configuration
  - Test API upload with schema validation (valid and invalid cases)
  - Verify response includes flattened_columns count
  - Verify table creation and queryability of flattened data

### Step 8: Create Comprehensive Integration Tests
- Create `app/server/tests/core/test_file_processor_nested.py`:
  - Test end-to-end nested JSON upload workflow:
    - Upload `nested_simple.json` with flattening enabled
    - Verify table schema contains flattened columns (e.g., `address__city`)
    - Query the table using SQL to verify data integrity
    - Verify sample_data in response shows flattened structure
  - Test deep nesting:
    - Upload `nested_deep.json` with 5 levels of nesting
    - Verify all levels are flattened correctly
  - Test array handling in index mode:
    - Upload JSON with arrays: `[{"tags": ["a", "b", "c"]}]`
    - Verify columns `tags__0`, `tags__1`, `tags__2` are created
  - Test schema validation integration:
    - Upload data that matches schema: success
    - Upload data that violates schema: failure with clear error message
  - Test backward compatibility:
    - Upload flat JSON without config: works as before
    - Upload flat JSON with `flatten_nested=false`: works identically to old behavior
  - Test error cases:
    - Nested depth exceeds max_depth: returns error
    - Invalid delimiter in config: validation error
    - Invalid schema definition: clear error message
- Run all integration tests: `cd app/server && uv run pytest tests/core/test_file_processor_nested.py -v`

### Step 9: Update Frontend (Optional Enhancement)
- This step is optional since backend API is backward compatible:
  - Current UI will work without changes using default flattening behavior
  - Future enhancement: Add UI controls for flattening options
  - For now: Document API configuration parameters for advanced users
- Update `app/client/src/main.ts` (optional):
  - Add UI toggle: "Flatten nested JSON" checkbox (default: checked)
  - Add delimiter selector: dropdown with _, -, . options
  - Send configuration in upload request if non-default options selected
- Note: This step can be skipped for MVP; backend alone provides full functionality

### Step 10: Update Documentation
- Update `README.md`:
  - Line 8: Change "Drag-and-drop file upload (.csv, .json, and .jsonl)" to "Drag-and-drop file upload (.csv, .json, and .jsonl with nested structure support)"
  - Add new section "Advanced JSON Features" after "Quick Start":
    - Explain nested JSON flattening with example
    - Show delimiter options and array handling modes
    - Provide JSON Schema validation example
    - Include sample API request with configuration
  - Add troubleshooting section for common nested JSON issues:
    - "Deep nesting exceeds limit" → increase max_depth
    - "Schema validation failed" → check error message for specific field issues
- Create `docs/nested-json-guide.md` (optional advanced guide):
  - Detailed explanation of flattening algorithm
  - Best practices for complex JSON structures
  - Examples of schema validation patterns
  - Performance considerations for large nested files

### Step 11: Run Validation Commands
- Run full test suite to ensure zero regressions:
  - `cd app/server && uv run pytest tests/core/test_json_utils.py -v` - JSON utilities tests
  - `cd app/server && uv run pytest tests/core/test_file_processor.py -v` - File processor tests
  - `cd app/server && uv run pytest tests/core/test_file_processor_nested.py -v` - Nested JSON integration tests
  - `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Security regression tests
  - `cd app/server && uv run pytest -v` - Full test suite
- Manual end-to-end testing:
  - Start server: `cd app/server && uv run python server.py`
  - Upload nested JSON file through UI at http://localhost:5173
  - Verify flattened table creation in database
  - Query flattened data using natural language
  - Test schema validation by uploading invalid data
  - Verify error messages are clear and actionable

## Testing Strategy

### Unit Tests

**JSON Flattening (`test_json_utils.py::test_flatten_json_object`)**
- Simple 2-level nesting: `{"user": {"name": "John"}}` → `{"user__name": "John"}`
- Deep 5-level nesting: verify recursive flattening to depth 5
- Array handling (index mode): `{"items": [1, 2, 3]}` → `{"items__0": 1, "items__1": 2, "items__2": 3}`
- Array of objects (index mode): `{"users": [{"name": "A"}, {"name": "B"}]}` → `{"users__0__name": "A", "users__1__name": "B"}`
- Custom delimiter: verify `.` and `-` delimiters work correctly
- Max depth protection: 11-level nesting should raise `ValueError` with "exceeds max depth" message
- Mixed types: dict containing string, int, float, bool, None - all preserved correctly
- Empty objects: `{"a": {}}` handled gracefully
- Empty arrays: `{"a": []}` handled gracefully
- Null values at various levels: `{"a": {"b": null}}` → `{"a__b": None}`

**Schema Normalization (`test_json_utils.py::test_normalize_schema`)**
- Inconsistent fields: `[{"a": 1}, {"b": 2}]` → `[{"a": 1, "b": None}, {"a": None, "b": 2}]`
- All fields present: no changes, return identical records
- Empty record list: return `[]`
- Single record: return `[record]` unchanged
- Large record set: 1000 records with varying fields, verify all fields discovered

**Schema Validation (`test_json_utils.py::test_validate_json_schema`)**
- Valid data: returns `None` (no errors)
- Missing required field: returns error message with field name
- Wrong type: returns error about type mismatch (expected string, got int)
- Invalid format: email field with non-email value returns format error
- Multiple records, one invalid: error message includes record index
- Invalid schema definition: returns error about schema itself
- Empty schema (allows anything): all data passes
- Strict schema: verify constraints are enforced

### Integration Tests

**File Processor Integration (`test_file_processor_nested.py`)**
- End-to-end nested JSON upload: upload nested JSON, verify table created with flattened columns
- Query flattened data: upload nested JSON, query using SQL, verify results are correct
- Schema validation success: upload valid nested JSON with schema, succeeds
- Schema validation failure: upload invalid nested JSON with schema, fails with clear error
- Custom delimiter: upload with `delimiter='.'`, verify column names use dots
- Array index mode: upload JSON with arrays, verify indexed columns created
- Max depth limit: upload JSON exceeding depth limit, verify error
- Backward compatibility: upload flat JSON with no config, verify works identically to before
- Large file: upload 10,000 nested records, verify performance acceptable (<5 seconds)

**API Endpoint Integration**
- Upload without config: works with default flattening behavior
- Upload with config JSON: respects flatten_nested, delimiter, array_mode options
- Upload with invalid config: returns 422 validation error with details
- Upload with schema validation: valid data succeeds, invalid data fails
- Response format: verify `flattened_columns` count is accurate
- Error responses: verify validation_errors list is populated correctly

### Edge Cases

**Nested Structure Edge Cases**
- Circular references: (if possible in JSON) should be detected and rejected
- Extremely deep nesting: 20+ levels (at max_depth limit)
- Wide objects: object with 500+ keys at same level
- Mixed nesting patterns: object → array → object → array → primitives
- Unicode in nested keys: `{"用户": {"名称": "测试"}}` should flatten correctly
- Special characters in keys: `{"user.name": "test"}` - key already contains delimiter
- Numeric string keys: `{"1": {"2": "value"}}` should not be confused with array indices

**Array Handling Edge Cases**
- Empty arrays in nested structure: `{"data": {"items": []}}`
- Arrays with null elements: `{"items": [1, null, 3]}`
- Arrays with mixed types: `{"items": [1, "string", true, null]}`
- Nested arrays: `{"matrix": [[1, 2], [3, 4]]}`
- Large arrays: array with 100+ elements in index mode

**Schema Validation Edge Cases**
- Schema with nested object requirements: verify nested validation works
- Schema with array constraints: minItems, maxItems, uniqueItems
- Schema with complex types: oneOf, anyOf, allOf
- Schema with pattern matching: regex validation on string fields
- Schema with custom formats: date-time, uuid, uri, etc.

**Performance and Scale**
- File with 1,000 deeply nested records (3+ levels)
- File with 10,000 flat records (baseline comparison)
- File with 100 records each having 50+ nested fields
- Memory usage monitoring during large file processing
- Comparison: nested JSON vs. equivalent flat JSON processing time

## Acceptance Criteria

1. Users can upload JSON and JSONL files containing nested objects (2+ levels deep) without preprocessing
2. Nested structures are automatically flattened into column names using configurable delimiters (default: `__`)
3. Arrays within JSON objects can be handled in "index" mode (creating `key__0`, `key__1` columns)
4. Users can optionally provide a JSON Schema to validate data before upload
5. Schema validation failures return clear, actionable error messages indicating which fields and constraints failed
6. Flattened column names pass through existing SQL injection protection
7. The `FileUploadResponse` includes `flattened_columns` count for transparency
8. Configuration options (delimiter, array_mode, max_depth) can be passed via API request
9. Default behavior (flattening enabled with `__` delimiter) works without requiring configuration
10. Existing flat JSON and CSV upload functionality has zero regressions
11. All new code has 100% unit test coverage
12. Integration tests verify end-to-end workflow including upload, flattening, and querying
13. Documentation clearly explains nested JSON support with examples
14. Performance remains acceptable: 10,000 nested records process in under 10 seconds

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/core/test_json_utils.py -v` - Run JSON utilities unit tests to validate flattening and validation logic
- `cd app/server && uv run pytest tests/core/test_file_processor.py -v` - Run file processor tests to ensure nested JSON integration works
- `cd app/server && uv run pytest tests/core/test_file_processor_nested.py -v` - Run nested JSON integration tests for end-to-end validation
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Run security tests to ensure flattened column names don't introduce SQL injection vulnerabilities
- `cd app/server && uv run pytest -v --cov=app.server.core --cov-report=term` - Run full test suite with coverage report to ensure 100% coverage of new code
- `cd app/server && uv run python server.py` - Start the server and manually test uploading nested JSON files through the UI at http://localhost:5173
- Upload test files with various nesting patterns and verify table creation and queryability
- Test schema validation by uploading data that violates a provided schema and verify clear error messages

## Notes

### Flattening Algorithm Details
The flattening algorithm uses recursive traversal to convert nested structures like:
```json
{"user": {"name": "John", "address": {"city": "NYC", "zip": "10001"}}}
```
Into flat dictionaries:
```python
{"user__name": "John", "user__address__city": "NYC", "user__address__zip": "10001"}
```

This approach preserves all data while making it queryable in a relational database structure.

### Array Handling Modes

**Index Mode (default)**: Arrays become indexed columns
```json
{"tags": ["python", "sql", "api"]}
```
Becomes:
```python
{"tags__0": "python", "tags__1": "sql", "tags__2": "api"}
```

**Explode Mode (future enhancement)**: Arrays create multiple rows (not in initial implementation)

### JSON Schema Validation
Uses the [JSON Schema](https://json-schema.org/) standard. Example schema:
```json
{
  "type": "object",
  "required": ["id", "name", "email"],
  "properties": {
    "id": {"type": "integer", "minimum": 1},
    "name": {"type": "string", "minLength": 1},
    "email": {"type": "string", "format": "email"}
  }
}
```

### Performance Considerations
- Flattening is O(n*m) where n=records, m=average nesting depth
- Acceptable for typical datasets (<100,000 records, <10 levels deep)
- For very large files (1M+ records), consider streaming approach in future
- Schema normalization requires full scan of all records to discover fields

### Dependencies
- **jsonschema**: Industry-standard JSON Schema validation library (MIT license)
  - Add with: `uv add jsonschema`
  - Size: ~100KB, no additional dependencies
  - Well-maintained, 10M+ downloads/month

### Backward Compatibility
This feature is **fully backward compatible**:
- Existing flat JSON uploads work identically (flattening no-ops on flat structures)
- Default behavior applies flattening automatically (can be disabled)
- API endpoint accepts files with or without configuration
- No breaking changes to existing functionality

### Security Considerations
- Flattened column names pass through `sanitize_table_name()` validation
- Nested keys like `{"'; DROP TABLE users--": "value"}` are sanitized to safe column names
- Schema validation prevents injection of malicious data through type enforcement
- Max depth limit (10 by default) prevents resource exhaustion from deeply nested structures

### Future Enhancements
- **Array explode mode**: Create separate rows for array elements (e.g., one row per tag)
- **Custom flattening rules**: User-defined flattening strategies for specific key patterns
- **Nested query support**: Allow querying nested paths directly without flattening (JSON1 extension)
- **Streaming processing**: Handle very large files (GB+) with constant memory usage
- **Schema inference**: Automatically generate JSON Schema from uploaded data
- **Unflatten on export**: Reverse flattening when exporting data back to JSON format
- **UI configuration**: Add frontend controls for flattening options (currently API-only)
