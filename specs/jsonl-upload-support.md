# Feature: JSONL (JSON Lines) Upload Support

## Feature Description
Add support for uploading JSONL (JSON Lines) files to the Natural Language SQL Interface application. JSONL is a convenient format for streaming large datasets where each line is a valid JSON object, making it particularly useful for log files, event streams, and large datasets that would be unwieldy as a single JSON array. This feature will enable users to upload .jsonl files alongside the existing .csv and .json formats, automatically converting them to SQLite tables for querying.

## User Story
As a data analyst or developer
I want to upload JSONL (.jsonl) files to the application
So that I can query streaming data formats, log files, and large datasets using natural language without having to manually convert them to CSV or JSON array formats

## Problem Statement
The application currently only supports CSV and JSON array formats for data upload. However, many modern data sources (log aggregators, event streams, data pipelines) export data in JSONL format where each line represents a separate JSON object. Users currently have to manually convert JSONL files to JSON arrays or CSV before uploading, which is time-consuming and error-prone, especially for large files. This creates friction in the data analysis workflow and limits the application's usability for real-world streaming data scenarios.

## Solution Statement
Extend the existing file processing pipeline to detect and handle .jsonl file extensions. The solution will add a new `convert_jsonl_to_sqlite` function that reads the file line-by-line, parses each line as a JSON object, and converts the collection into a pandas DataFrame (similar to the existing JSON processing). This approach leverages the existing SQLite table creation infrastructure while adding minimal complexity. The solution maintains consistency with existing security measures, validation, and error handling patterns.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py:72-109` - Upload endpoint that validates file extensions and routes to appropriate converter functions. This is where we'll add .jsonl to the allowed extensions list and route to the new converter function.

- `app/server/core/file_processor.py:104-174` - Contains `convert_json_to_sqlite` function which provides the template for our JSONL converter. We'll add a new `convert_jsonl_to_sqlite` function here that follows the same pattern but handles line-by-line JSON parsing.

- `app/server/core/data_models.py:6-15` - Defines the `FileUploadResponse` model used by the upload endpoint. No changes needed, but we need to understand this model to ensure our new function returns the correct structure.

- `app/server/core/sql_security.py` - Security utilities for safe SQL operations. Our new function will use the same security measures (`validate_identifier`, `execute_query_safely`, `sanitize_table_name`) as existing converters.

- `app/client/src/main.ts:54-90` - Frontend file upload handler that validates file types. We'll update the file validation to accept .jsonl extensions.

- `README.md:8` - Documentation that lists supported file formats. Update to include .jsonl in the feature list.

### New Files

- `app/server/tests/core/test_file_processor_jsonl.py` - New test file specifically for JSONL processing functionality with comprehensive test cases including valid JSONL, empty files, malformed lines, and edge cases.

- `app/server/tests/assets/sample.jsonl` - Sample JSONL test data file for use in unit tests.

## Implementation Plan

### Phase 1: Foundation
Before implementing the main feature, we need to prepare the test infrastructure and understand the JSONL format requirements:

1. Create test assets directory structure if not exists
2. Create sample JSONL test files with various scenarios (valid data, empty lines, malformed JSON, mixed data types)
3. Review pandas DataFrame creation from list of dictionaries to ensure our approach will work
4. Verify that the existing JSON converter's approach can be adapted for line-by-line processing

### Phase 2: Core Implementation
Implement the JSONL file processing functionality:

1. Add `convert_jsonl_to_sqlite` function in `app/server/core/file_processor.py` that:
   - Reads the file content line-by-line
   - Parses each non-empty line as a JSON object
   - Collects all objects into a list
   - Converts the list to a pandas DataFrame
   - Follows the same table creation, schema extraction, and sample data pattern as `convert_json_to_sqlite`
   - Uses identical security measures and validation

2. Update the upload endpoint in `app/server/server.py` to:
   - Accept .jsonl file extensions in validation
   - Route .jsonl files to the new `convert_jsonl_to_sqlite` function

3. Create comprehensive unit tests in `app/server/tests/core/test_file_processor_jsonl.py` covering:
   - Valid JSONL files with multiple objects
   - Empty files
   - Files with blank lines (should be skipped)
   - Files with malformed JSON on some lines
   - Files with inconsistent schemas across lines
   - Large files with many objects
   - Security edge cases (SQL injection attempts in data)

### Phase 3: Integration
Integrate the feature with the frontend and documentation:

1. Update frontend validation in `app/client/src/main.ts`:
   - Add .jsonl to accepted file extensions in the drop zone validation
   - Update any UI text that mentions supported formats

2. Update `README.md`:
   - Add .jsonl to the list of supported file formats
   - Optionally add a brief explanation of JSONL format

3. Verify end-to-end workflow:
   - Upload JSONL file through UI
   - Verify table creation and schema detection
   - Query the uploaded data using natural language
   - Test with real-world JSONL files (e.g., exported logs)

## Step by Step Tasks

### Step 1: Create Test Infrastructure
- Create `app/server/tests/assets/` directory if it doesn't exist
- Create `app/server/tests/assets/sample.jsonl` with valid test data (5-10 user objects with fields like id, name, email, age)
- Create `app/server/tests/assets/empty.jsonl` with empty content
- Create `app/server/tests/assets/malformed.jsonl` with some invalid JSON lines
- Create `app/server/tests/assets/blank_lines.jsonl` with blank lines between valid JSON objects

### Step 2: Implement JSONL Converter Function
- Add `convert_jsonl_to_sqlite` function to `app/server/core/file_processor.py`
- Function should accept `jsonl_content: bytes` and `table_name: str` parameters
- Decode bytes to UTF-8 string and split by newlines
- Parse each non-empty line as JSON object using `json.loads()`
- Handle parse errors gracefully with informative error messages
- Collect all valid objects into a list
- Validate that at least one valid object was parsed
- Convert list to pandas DataFrame
- Clean column names (lowercase, replace spaces/hyphens with underscores)
- Use `sanitize_table_name()` to validate table name
- Create SQLite table using `df.to_sql()` with `if_exists='replace'`
- Extract schema using `execute_query_safely()` with PRAGMA table_info
- Get sample data (first 5 rows) using safe query execution
- Get row count using safe query execution
- Return dictionary matching the format of `convert_json_to_sqlite()`
- Wrap in try/except with descriptive error messages

### Step 3: Update Server Upload Endpoint
- Modify `app/server/server.py` line 77 to accept .jsonl extension
- Change condition from `if not file.filename.endswith(('.csv', '.json'))` to include '.jsonl'
- Add conditional routing around line 87-90 to handle .jsonl files
- Add elif branch: `elif file.filename.endswith('.jsonl'): result = convert_jsonl_to_sqlite(content, table_name)`
- Import the new function at the top of the file

### Step 4: Create Unit Tests for JSONL Processing
- Create `app/server/tests/core/test_file_processor_jsonl.py`
- Add imports for pytest, file_processor, sqlite3, json
- Test valid JSONL file parsing and table creation
- Test empty JSONL file handling (should raise appropriate error)
- Test JSONL with blank lines (should skip blank lines)
- Test malformed JSON lines (should raise error with line number)
- Test inconsistent schemas (pandas should handle with NaN values)
- Test table name sanitization with special characters
- Test SQL injection attempts in data values (should be safely parameterized)
- Each test should verify: table creation, row count, schema structure, sample data
- Use temporary database file for each test with proper cleanup

### Step 5: Update Frontend File Validation
- Update `app/client/src/main.ts` line 77 (file extension validation in server) is already done
- Note: The frontend doesn't have explicit file extension validation in the drag-and-drop handler
- Verify that the browser's file input accepts .jsonl files by testing
- If needed, update any displayed text that mentions supported formats

### Step 6: Update Documentation
- Update `README.md` line 8 in Features section
- Change "Drag-and-drop file upload (.csv and .json)" to "Drag-and-drop file upload (.csv, .json, and .jsonl)"
- Optionally add a brief note in the Usage section explaining JSONL format (one JSON object per line)

### Step 7: Run Validation Commands
- Run full test suite to ensure no regressions
- Test with real JSONL files through the complete upload flow
- Verify table creation, schema detection, and querying works correctly
- Test with various edge cases (large files, special characters in data, different data types)

## Testing Strategy

### Unit Tests
- **Valid JSONL Parsing**: Test file with 5 user objects, verify all rows are imported correctly
- **Empty File Handling**: Test empty file raises appropriate ValueError
- **Blank Line Skipping**: Test file with blank lines between objects, verify blank lines are ignored
- **Malformed JSON Detection**: Test file with invalid JSON on line 3, verify error message includes line number
- **Schema Consistency**: Test objects with different fields, verify pandas handles missing fields with NULL
- **Column Name Sanitization**: Test objects with special characters in keys, verify column names are cleaned
- **Table Name Security**: Test with SQL injection attempt in filename, verify sanitization prevents injection
- **Data Type Handling**: Test objects with mixed types (string, int, float, boolean, null), verify SQLite type inference
- **Large File Handling**: Test file with 1000+ objects, verify memory-efficient processing
- **Unicode Support**: Test objects with Unicode characters in values, verify proper UTF-8 handling

### Integration Tests
- **End-to-End Upload**: Upload JSONL via API, verify FileUploadResponse structure
- **Query After Upload**: Upload JSONL file, then query the table using natural language
- **Table Overwrite**: Upload same filename twice, verify table is replaced
- **Multiple Format Support**: Upload CSV, JSON, and JSONL files sequentially, verify all work
- **Schema Endpoint**: Upload JSONL file, call /api/schema, verify table appears in response
- **Table Deletion**: Upload JSONL file, delete the table, verify successful removal
- **Sample Data Display**: Verify that sample_data in response contains first 5 rows with correct structure

### Edge Cases
- Empty JSONL file (0 bytes)
- JSONL with only blank lines or whitespace
- Single JSON object (1 line)
- Extremely long lines (objects with large text fields)
- JSONL with trailing newline vs no trailing newline
- Objects with nested structures (should flatten or store as TEXT)
- Objects with array values (should serialize appropriately)
- File with Windows line endings (CRLF) vs Unix (LF)
- File with BOM (Byte Order Mark) at start
- Filename with special characters (spaces, hyphens, unicode)

## Acceptance Criteria
1. Users can successfully upload .jsonl files through the drag-and-drop interface
2. .jsonl files are converted to SQLite tables with correct schema detection
3. Each line in the JSONL file becomes a row in the database table
4. Blank lines in JSONL files are automatically skipped
5. Column names from JSON keys are sanitized (lowercase, underscores)
6. Table names are sanitized to prevent SQL injection
7. Files with malformed JSON lines provide clear error messages indicating which line failed
8. Uploaded JSONL data can be queried using natural language queries
9. The schema endpoint correctly lists tables created from JSONL files
10. Sample data (first 5 rows) is returned in the upload response
11. All existing functionality (CSV and JSON uploads) continues to work without regression
12. Unit tests achieve 100% code coverage for the new JSONL processing function
13. Documentation reflects the new .jsonl format support

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/core/test_file_processor_jsonl.py -v` - Run JSONL-specific tests to validate the new functionality
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Run security tests to ensure no regressions in SQL injection protection
- `cd app/server && uv run pytest -v` - Run full server test suite to validate zero regressions across all functionality
- `cd app/server && uv run python server.py` - Start the server and manually test uploading a .jsonl file through the UI at http://localhost:5173

## Notes
- **JSONL Format**: JSONL (JSON Lines) is a format where each line is a valid JSON object. It's commonly used for streaming data and log files. Unlike regular JSON arrays, JSONL files can be processed line-by-line without loading the entire file into memory.

- **Error Handling**: The implementation should handle partial failures gracefully. If line 5 of a 100-line file has malformed JSON, the error message should clearly indicate "Error on line 5" to help users debug their data.

- **Memory Efficiency**: While the current implementation loads all objects into memory before creating the DataFrame, this is acceptable for typical file sizes. For future optimization, consider streaming approaches for very large files (GB+).

- **Schema Inconsistencies**: When JSONL objects have different keys, pandas will create columns for all keys found across all objects, filling missing values with NULL. This is expected behavior and matches how real-world streaming data often works.

- **Nested Objects**: If JSON objects contain nested structures or arrays, pandas will attempt to serialize them as strings. For future enhancement, consider flattening nested structures or using JSON columns.

- **Dependencies**: No new dependencies required. The implementation uses existing libraries (json, pandas, sqlite3) that are already in the project.

- **Performance**: JSONL processing should have similar performance characteristics to JSON array processing since both ultimately create a pandas DataFrame from a list of dictionaries.

- **Future Enhancements**:
  - Add support for .ndjson extension (alias for JSONL)
  - Implement streaming processing for very large files
  - Add progress indicators for large file uploads
  - Support schema validation/enforcement across lines
  - Add option to skip malformed lines instead of failing completely
