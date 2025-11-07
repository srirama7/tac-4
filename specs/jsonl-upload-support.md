# Feature: JSONL Upload Support

## Feature Description
Add support for uploading JSONL (JSON Lines) files to the Natural Language SQL Interface. JSONL files contain one JSON object per line, making them ideal for streaming large datasets. The feature will handle nested objects and arrays by flattening them using a configurable delimiter strategy, similar to how CSV and JSON files are currently processed. Each JSONL file will create a single new table in the SQLite database.

## User Story
As a data analyst
I want to upload JSONL files to the application
So that I can query streaming data and large datasets that are commonly stored in JSONL format without needing to convert them to CSV or JSON first

## Problem Statement
Currently, the application only supports CSV and JSON file uploads. However, JSONL (JSON Lines) is a popular format for:
- Log files and event streams
- Large datasets that don't fit in memory as a single JSON array
- Data exports from APIs and databases
- Machine learning datasets

Users with JSONL data must manually convert their files to JSON or CSV before uploading, creating unnecessary friction.

## Solution Statement
Implement a JSONL file processor that:
1. Reads JSONL files line-by-line to handle large files efficiently
2. Flattens nested JSON objects using the `__` delimiter (e.g., `user.address.city` → `user__address__city`)
3. Flattens arrays using index notation with `_` delimiter (e.g., `tags[0]` → `tags_0`)
4. Uses the existing constants from `core/constants.py` for delimiter configuration
5. Creates a single SQLite table per JSONL file, just like CSV and JSON uploads
6. Updates the UI to indicate JSONL support in file upload areas
7. Provides sample JSONL test files for validation

## Relevant Files

### Existing Files to Modify

**app/server/core/file_processor.py** - Core file processing module
- Add `convert_jsonl_to_sqlite()` function to handle JSONL file parsing and conversion
- Implement nested object flattening logic using `NESTED_FIELD_DELIMITER`
- Implement array flattening logic using `LIST_INDEX_DELIMITER`
- Parse JSONL format (one JSON object per line) and collect all possible fields across all lines
- Leverage existing `sanitize_table_name()` function for table naming

**app/server/core/constants.py** - Configuration constants
- Already contains `NESTED_FIELD_DELIMITER = "__"` and `LIST_INDEX_DELIMITER = "_"`
- No changes needed, but will be imported and used by the JSONL processor

**app/server/server.py** - FastAPI server endpoints
- Update `/api/upload` endpoint to accept `.jsonl` file extension
- Add JSONL file type to validation logic (line 77: change to `.endswith(('.csv', '.json', '.jsonl'))`)
- Add conditional logic to route JSONL files to `convert_jsonl_to_sqlite()`

**app/client/index.html** - Frontend HTML template
- Update line 80: change "Drag and drop .csv or .json files here" to "Drag and drop .csv, .json, or .jsonl files here"
- Update line 81: change `accept=".csv,.json"` to `accept=".csv,.json,.jsonl"`

**app/client/src/main.ts** - Frontend TypeScript main file
- No functional changes needed (file upload logic is generic)
- Existing upload handling will work with new file type

**README.md** - Project documentation
- Update line 8: change "Drag-and-drop file upload (.csv and .json)" to "Drag-and-drop file upload (.csv, .json, and .jsonl)"
- Update line 78: add note about JSONL format support and nested field flattening
- Update line 86-87: document that JSONL files can be uploaded
- Update line 138: change "Upload CSV/JSON file" to "Upload CSV/JSON/JSONL file"
- Update line 196: change "File upload validation (CSV and JSON only)" to "File upload validation (CSV, JSON, and JSONL only)"

### New Files to Create

**app/server/tests/assets/test_events.jsonl** - Sample JSONL file for testing
- Contains nested objects and arrays to test flattening logic
- Represents event log data with user actions, timestamps, and metadata

**app/server/tests/assets/test_simple.jsonl** - Simple JSONL file for testing
- Contains flat objects without nesting for basic validation
- Smaller dataset for quick smoke tests

**app/server/tests/core/test_jsonl_processor.py** - Unit tests for JSONL processing
- Test successful JSONL parsing and table creation
- Test nested object flattening with `__` delimiter
- Test array flattening with `_` delimiter
- Test handling of inconsistent fields across lines (schema inference)
- Test error handling for malformed JSONL
- Test edge cases (empty file, single line, mixed data types)

## Implementation Plan

### Phase 1: Foundation
Set up the core JSONL processing infrastructure:
1. Review existing CSV/JSON processors to understand the pattern
2. Design the flattening algorithm for nested objects and arrays
3. Ensure the constants file (`NESTED_FIELD_DELIMITER` and `LIST_INDEX_DELIMITER`) is properly configured
4. Create test JSONL files with various data structures (nested, arrays, mixed)

### Phase 2: Core Implementation
Implement the JSONL file processor:
1. Add `convert_jsonl_to_sqlite()` function in `core/file_processor.py`
   - Read JSONL file line-by-line (handle large files)
   - Parse each line as a JSON object
   - Collect all unique field names across all lines (schema inference)
   - Flatten nested objects recursively using `__` delimiter
   - Flatten arrays using index notation with `_` delimiter
   - Convert to pandas DataFrame and write to SQLite
   - Return schema, row count, and sample data (same format as CSV/JSON)
2. Import and use constants from `core/constants.py`
3. Handle edge cases: empty files, malformed JSON lines, inconsistent schemas

### Phase 3: Integration
Integrate JSONL support into the existing application:
1. Update server endpoint to accept `.jsonl` files
2. Add routing logic to call `convert_jsonl_to_sqlite()` for JSONL files
3. Update frontend UI to indicate JSONL support
4. Update documentation to reflect new file format support
5. Create comprehensive tests to validate end-to-end functionality

## Step by Step Tasks

### 1. Create Test JSONL Files
- Create `app/server/tests/assets/test_events.jsonl` with nested objects and arrays
  - Include fields like: `{"event_id": 1, "user": {"id": 123, "name": "John"}, "tags": ["login", "success"], "timestamp": "2024-01-01T10:00:00Z"}`
  - Include at least 5-10 diverse records
- Create `app/server/tests/assets/test_simple.jsonl` with flat objects
  - Include fields like: `{"id": 1, "name": "Product A", "price": 99.99}`
  - Include 3-5 simple records

### 2. Implement JSONL Processor Function
- Open `app/server/core/file_processor.py`
- Import constants: `from .constants import NESTED_FIELD_DELIMITER, LIST_INDEX_DELIMITER`
- Implement `flatten_json_object(obj, parent_key='', sep=NESTED_FIELD_DELIMITER)` helper function
  - Recursively flatten nested dictionaries
  - Handle lists by creating indexed fields (e.g., `tags_0`, `tags_1`)
  - Return a flat dictionary with concatenated keys
- Implement `convert_jsonl_to_sqlite(jsonl_content: bytes, table_name: str) -> Dict[str, Any]` function
  - Decode bytes to string
  - Split by newlines to get individual JSON objects
  - Parse each line with `json.loads()`
  - Flatten each object using helper function
  - Collect all flattened objects into a list
  - Convert to pandas DataFrame (handles inconsistent schemas automatically)
  - Follow the same pattern as `convert_json_to_sqlite()` for the rest
  - Use `sanitize_table_name()` for table name safety
  - Return schema, row count, and sample data

### 3. Update Server Endpoint
- Open `app/server/server.py`
- Update line 77: change validation to `if not file.filename.endswith(('.csv', '.json', '.jsonl')):`
- Update error message on line 78: `"Only .csv, .json, and .jsonl files are supported"`
- Add import: `from core.file_processor import convert_csv_to_sqlite, convert_json_to_sqlite, convert_jsonl_to_sqlite`
- Add conditional logic after line 89:
  ```python
  elif file.filename.endswith('.jsonl'):
      result = convert_jsonl_to_sqlite(content, table_name)
  ```

### 4. Update Frontend UI
- Open `app/client/index.html`
- Update line 80: change text to "Drag and drop .csv, .json, or .jsonl files here"
- Update line 81: change `accept=".csv,.json"` to `accept=".csv,.json,.jsonl"`

### 5. Update Documentation
- Open `README.md`
- Update line 8: change to "Drag-and-drop file upload (.csv, .json, and .jsonl)"
- Update line 86-87: add note about JSONL upload support in the Usage section
- Update line 138: change API endpoint description to "Upload CSV/JSON/JSONL file"
- Update line 196: change validation description to "File upload validation (CSV, JSON, and JSONL only)"
- Add a new section under "Features" explaining nested field flattening:
  ```markdown
  - 📊 Automatic nested field flattening for JSONL files
    - Nested objects: `user.address.city` → `user__address__city`
    - Arrays: `tags[0]` → `tags_0`, `tags[1]` → `tags_1`
  ```

### 6. Create Unit Tests
- Create `app/server/tests/core/test_jsonl_processor.py`
- Import test fixtures and the new function
- Test `test_convert_jsonl_to_sqlite_success()` with `test_simple.jsonl`
  - Verify table creation, schema, row count, sample data
- Test `test_convert_jsonl_to_sqlite_nested_flattening()` with `test_events.jsonl`
  - Verify nested fields are flattened with `__` delimiter
  - Verify schema contains flattened field names (e.g., `user__id`, `user__name`)
- Test `test_convert_jsonl_to_sqlite_array_flattening()` with array data
  - Verify arrays are indexed with `_` delimiter (e.g., `tags_0`, `tags_1`)
- Test `test_convert_jsonl_to_sqlite_inconsistent_schema()`
  - Create JSONL with different fields per line
  - Verify pandas handles missing fields gracefully (fills with NaN)
- Test `test_convert_jsonl_to_sqlite_invalid_jsonl()`
  - Test with malformed JSON line
  - Verify appropriate error is raised
- Test `test_convert_jsonl_to_sqlite_empty_file()`
  - Test with empty JSONL content
  - Verify appropriate error is raised

### 7. Integration Testing
- Run the server: `cd app/server && uv run python server.py`
- Run the client: `cd app/client && npm run dev`
- Manually test JSONL upload through the UI
  - Upload `test_events.jsonl` and verify table creation
  - Check that nested fields are properly flattened in the schema display
  - Query the table with natural language to verify data accessibility
  - Upload `test_simple.jsonl` and verify basic functionality
  - Verify that uploading a JSONL file with the same name overwrites the existing table

### 8. Run All Validation Commands
- Execute all validation commands listed in the "Validation Commands" section
- Ensure zero errors and zero regressions
- Verify all existing CSV and JSON upload functionality still works
- Verify new JSONL upload functionality works end-to-end

## Testing Strategy

### Unit Tests
- **JSONL Parsing**: Verify correct parsing of JSONL format (one JSON per line)
- **Nested Flattening**: Verify nested objects are flattened with `__` delimiter
- **Array Flattening**: Verify arrays are indexed with `_` delimiter
- **Schema Inference**: Verify all fields across all lines are captured
- **Error Handling**: Verify malformed JSONL raises appropriate errors
- **Edge Cases**: Empty files, single line, mixed types, inconsistent schemas

### Integration Tests
- **End-to-End Upload**: Upload JSONL file through UI, verify table creation
- **Query Integration**: Query JSONL-created tables with natural language
- **File Type Validation**: Verify only valid file types are accepted
- **Table Replacement**: Verify uploading same filename overwrites table
- **UI Updates**: Verify UI correctly shows JSONL support

### Edge Cases
- **Empty JSONL file**: Should raise error or create empty table gracefully
- **Single line JSONL**: Should work like single-object JSON
- **Malformed JSON line**: Should raise clear error with line number
- **Deeply nested objects**: Should flatten correctly (e.g., `a.b.c.d.e`)
- **Large arrays**: Should handle many array elements (e.g., 100 items)
- **Inconsistent schemas**: Lines with different fields should merge schemas
- **Mixed data types**: Same field with different types across lines
- **Special characters in keys**: Should sanitize field names
- **Very large files**: Should handle files with thousands of lines efficiently

## Acceptance Criteria
- [ ] Users can upload `.jsonl` files through the drag-and-drop interface
- [ ] JSONL files are correctly parsed (one JSON object per line)
- [ ] Nested objects are flattened using `__` delimiter (e.g., `user__address__city`)
- [ ] Arrays are flattened using `_` delimiter with indices (e.g., `tags_0`, `tags_1`)
- [ ] All fields across all JSONL lines are discovered and included in schema
- [ ] Each JSONL file creates one new SQLite table
- [ ] Table schema, row count, and sample data are returned correctly
- [ ] UI indicates JSONL support in file upload areas
- [ ] Error messages are clear for malformed JSONL files
- [ ] Existing CSV and JSON upload functionality continues to work
- [ ] Sample JSONL test files are available in `tests/assets/` directory
- [ ] Unit tests cover all core functionality and edge cases
- [ ] Documentation is updated to reflect JSONL support
- [ ] All existing tests continue to pass (zero regressions)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/core/test_jsonl_processor.py -v` - Run JSONL-specific tests with verbose output
- `cd app/server && uv run pytest tests/core/test_file_processor.py -v` - Verify existing file processor tests still pass
- `cd app/server && uv run python server.py` - Start server and manually test JSONL upload through UI
- `cd app/client && npm run dev` - Start client and verify UI shows JSONL support

## Notes

### Design Decisions
- **Use stdlib only**: The feature uses only Python standard library (`json`) and existing dependencies (`pandas`, `sqlite3`), no new libraries required
- **Delimiter strategy**: Using existing `NESTED_FIELD_DELIMITER = "__"` and `LIST_INDEX_DELIMITER = "_"` from `core/constants.py` for consistency
- **Schema inference**: Parse entire JSONL file first to discover all possible fields, similar to how pandas handles CSV with inconsistent columns
- **Flattening approach**: Recursive flattening ensures deeply nested structures are handled correctly
- **Error handling**: Follow existing pattern from `convert_json_to_sqlite()` - wrap in try/except and raise descriptive errors

### Future Considerations
- **Performance optimization**: For very large JSONL files (GB+), consider streaming to SQLite instead of loading entire file into pandas
- **Array flattening options**: Consider alternative strategies like JSON serialization for complex arrays instead of indexing
- **Custom delimiters**: Could expose delimiter configuration in UI for power users
- **JSONL export**: Add ability to export tables back to JSONL format
- **Streaming support**: Add WebSocket support for real-time JSONL streaming uploads

### Implementation Notes
- The flattening logic should be tested with the actual test files before integration
- Pandas automatically handles inconsistent schemas by filling missing fields with NaN
- Column names should be cleaned the same way as CSV/JSON (lowercase, replace spaces/dashes with underscores)
- The `sanitize_table_name()` function will handle any special characters in the filename
- Security: JSONL parsing uses the same security measures as JSON (no code execution, just data parsing)
