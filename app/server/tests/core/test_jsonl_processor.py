"""
Unit tests for JSONL file processing functionality.

Tests cover:
- Basic JSONL parsing and table creation
- Nested object flattening with '__' delimiter
- Array flattening with '_' delimiter
- Inconsistent schema handling across lines
- Error handling for malformed JSONL
- Edge cases (empty files, single line, etc.)
"""

import pytest
import json
import sqlite3
from pathlib import Path
from core.file_processor import (
    convert_jsonl_to_sqlite,
    parse_jsonl_file,
    flatten_record,
    discover_all_fields,
    sanitize_table_name
)


class TestParseJSONLFile:
    """Test JSONL file parsing functionality"""

    def test_parse_simple_jsonl(self):
        """Test parsing basic JSONL with flat objects"""
        jsonl_content = b'{"id": 1, "name": "Alice"}\n{"id": 2, "name": "Bob"}\n'
        records = parse_jsonl_file(jsonl_content)

        assert len(records) == 2
        assert records[0] == {"id": 1, "name": "Alice"}
        assert records[1] == {"id": 2, "name": "Bob"}

    def test_parse_jsonl_with_empty_lines(self):
        """Test parsing JSONL with empty lines and whitespace"""
        jsonl_content = b'{"id": 1}\n\n{"id": 2}\n   \n{"id": 3}\n'
        records = parse_jsonl_file(jsonl_content)

        assert len(records) == 3
        assert records[0]["id"] == 1
        assert records[1]["id"] == 2
        assert records[2]["id"] == 3

    def test_parse_jsonl_with_trailing_newline(self):
        """Test parsing JSONL with trailing newline"""
        jsonl_content = b'{"id": 1}\n{"id": 2}\n'
        records = parse_jsonl_file(jsonl_content)

        assert len(records) == 2

    def test_parse_jsonl_invalid_json(self):
        """Test error handling for malformed JSON line"""
        jsonl_content = b'{"id": 1}\n{invalid json}\n{"id": 3}\n'

        with pytest.raises(ValueError) as exc_info:
            parse_jsonl_file(jsonl_content)

        assert "Line 2" in str(exc_info.value)
        assert "Invalid JSON" in str(exc_info.value)

    def test_parse_jsonl_non_dict(self):
        """Test error handling when line is not a JSON object"""
        jsonl_content = b'{"id": 1}\n[1, 2, 3]\n{"id": 3}\n'

        with pytest.raises(ValueError) as exc_info:
            parse_jsonl_file(jsonl_content)

        assert "Line 2" in str(exc_info.value)
        assert "Expected JSON object" in str(exc_info.value)

    def test_parse_jsonl_invalid_utf8(self):
        """Test error handling for invalid UTF-8 encoding"""
        jsonl_content = b'\xff\xfe{"id": 1}\n'

        with pytest.raises(ValueError) as exc_info:
            parse_jsonl_file(jsonl_content)

        assert "Invalid UTF-8 encoding" in str(exc_info.value)


class TestFlattenRecord:
    """Test record flattening functionality"""

    def test_flatten_flat_record(self):
        """Test flattening already flat record"""
        record = {"id": 1, "name": "Alice", "age": 30}
        flattened = flatten_record(record)

        assert flattened == {"id": 1, "name": "Alice", "age": 30}

    def test_flatten_nested_object(self):
        """Test flattening nested objects with '__' delimiter"""
        record = {
            "user": {
                "id": 123,
                "name": "John Doe"
            },
            "active": True
        }
        flattened = flatten_record(record)

        assert flattened["user__id"] == 123
        assert flattened["user__name"] == "John Doe"
        assert flattened["active"] is True

    def test_flatten_deeply_nested_object(self):
        """Test flattening deeply nested objects"""
        record = {
            "user": {
                "address": {
                    "city": "NYC",
                    "zip": "10001"
                }
            }
        }
        flattened = flatten_record(record)

        assert flattened["user__address__city"] == "NYC"
        assert flattened["user__address__zip"] == "10001"

    def test_flatten_array(self):
        """Test flattening arrays with '_' delimiter"""
        record = {
            "id": 1,
            "tags": ["python", "sql", "data"]
        }
        flattened = flatten_record(record)

        assert flattened["id"] == 1
        assert flattened["tags_0"] == "python"
        assert flattened["tags_1"] == "sql"
        assert flattened["tags_2"] == "data"

    def test_flatten_nested_object_in_array(self):
        """Test flattening objects within arrays"""
        record = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
        flattened = flatten_record(record)

        assert flattened["users_0__id"] == 1
        assert flattened["users_0__name"] == "Alice"
        assert flattened["users_1__id"] == 2
        assert flattened["users_1__name"] == "Bob"

    def test_flatten_complex_nested_structure(self):
        """Test flattening complex nested structure"""
        record = {
            "event_id": 1,
            "user": {
                "id": 123,
                "profile": {
                    "name": "John",
                    "settings": {
                        "notifications": True
                    }
                }
            },
            "tags": ["login", "success"]
        }
        flattened = flatten_record(record)

        assert flattened["event_id"] == 1
        assert flattened["user__id"] == 123
        assert flattened["user__profile__name"] == "John"
        assert flattened["user__profile__settings__notifications"] is True
        assert flattened["tags_0"] == "login"
        assert flattened["tags_1"] == "success"

    def test_flatten_with_none_values(self):
        """Test flattening records with None values"""
        record = {"id": 1, "name": None, "active": True}
        flattened = flatten_record(record)

        assert flattened["id"] == 1
        assert flattened["name"] is None
        assert flattened["active"] is True


class TestDiscoverAllFields:
    """Test field discovery across multiple records"""

    def test_discover_fields_consistent_schema(self):
        """Test field discovery with consistent schema"""
        records = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        fields = discover_all_fields(records)

        assert fields == {"id", "name"}

    def test_discover_fields_inconsistent_schema(self):
        """Test field discovery with varying schemas"""
        records = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob", "age": 30},
            {"id": 3, "email": "charlie@example.com"}
        ]
        fields = discover_all_fields(records)

        assert fields == {"id", "name", "age", "email"}

    def test_discover_fields_nested_objects(self):
        """Test field discovery with nested objects"""
        records = [
            {"user": {"id": 1, "name": "Alice"}},
            {"user": {"id": 2, "name": "Bob", "age": 30}}
        ]
        fields = discover_all_fields(records)

        assert "user__id" in fields
        assert "user__name" in fields
        assert "user__age" in fields

    def test_discover_fields_arrays(self):
        """Test field discovery with arrays of different lengths"""
        records = [
            {"id": 1, "tags": ["python", "sql"]},
            {"id": 2, "tags": ["javascript", "react", "node"]},
            {"id": 3, "tags": ["java"]}
        ]
        fields = discover_all_fields(records)

        assert "id" in fields
        assert "tags_0" in fields
        assert "tags_1" in fields
        assert "tags_2" in fields

    def test_discover_fields_complex_structure(self):
        """Test field discovery with complex nested structures"""
        records = [
            {
                "event_id": 1,
                "user": {"id": 123, "name": "John"},
                "tags": ["login", "success"]
            },
            {
                "event_id": 2,
                "user": {"id": 456, "name": "Jane", "email": "jane@example.com"},
                "tags": ["upload"]
            }
        ]
        fields = discover_all_fields(records)

        assert "event_id" in fields
        assert "user__id" in fields
        assert "user__name" in fields
        assert "user__email" in fields
        assert "tags_0" in fields
        assert "tags_1" in fields


class TestConvertJSONLToSQLite:
    """Test end-to-end JSONL to SQLite conversion"""

    def setup_method(self):
        """Clean up database before each test"""
        db_path = Path("db/database.db")
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for (table_name,) in tables:
                cursor.execute(f"DROP TABLE IF EXISTS [{table_name}]")
            conn.commit()
            conn.close()

    def test_convert_simple_jsonl(self):
        """Test converting simple JSONL file"""
        jsonl_content = b'{"id": 1, "name": "Product A", "price": 99.99}\n{"id": 2, "name": "Product B", "price": 149.99}\n'

        result = convert_jsonl_to_sqlite(jsonl_content, "test_products")

        assert result["table_name"] == "test_products"
        assert result["row_count"] == 2
        assert "id" in result["schema"]
        assert "name" in result["schema"]
        assert "price" in result["schema"]
        assert len(result["sample_data"]) == 2

    def test_convert_nested_jsonl(self):
        """Test converting JSONL with nested objects"""
        jsonl_content = b'''{"event_id": 1, "user": {"id": 123, "name": "John"}, "timestamp": "2024-01-01T10:00:00Z"}
{"event_id": 2, "user": {"id": 456, "name": "Jane"}, "timestamp": "2024-01-01T10:15:00Z"}'''

        result = convert_jsonl_to_sqlite(jsonl_content, "test_events")

        assert result["table_name"] == "test_events"
        assert result["row_count"] == 2
        assert "event_id" in result["schema"]
        assert "user__id" in result["schema"]
        assert "user__name" in result["schema"]
        assert "timestamp" in result["schema"]

    def test_convert_jsonl_with_arrays(self):
        """Test converting JSONL with arrays"""
        jsonl_content = b'''{"id": 1, "tags": ["login", "success"]}
{"id": 2, "tags": ["upload", "file", "complete"]}
{"id": 3, "tags": ["query"]}'''

        result = convert_jsonl_to_sqlite(jsonl_content, "test_tags")

        assert result["table_name"] == "test_tags"
        assert result["row_count"] == 3
        assert "id" in result["schema"]
        assert "tags_0" in result["schema"]
        assert "tags_1" in result["schema"]
        assert "tags_2" in result["schema"]

    def test_convert_jsonl_inconsistent_schema(self):
        """Test converting JSONL with varying schemas across lines"""
        jsonl_content = b'''{"id": 1, "name": "Alice"}
{"id": 2, "name": "Bob", "age": 30}
{"id": 3, "email": "charlie@example.com"}'''

        result = convert_jsonl_to_sqlite(jsonl_content, "test_users")

        assert result["table_name"] == "test_users"
        assert result["row_count"] == 3
        assert "id" in result["schema"]
        assert "name" in result["schema"]
        assert "age" in result["schema"]
        assert "email" in result["schema"]

        # Verify that missing fields are handled (should be None/NULL)
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_users WHERE id = 1")
        row = cursor.fetchone()
        conn.close()

        # First record should have NULL for age and email
        assert row is not None

    def test_convert_empty_jsonl(self):
        """Test error handling for empty JSONL file"""
        jsonl_content = b''

        with pytest.raises(ValueError) as exc_info:
            convert_jsonl_to_sqlite(jsonl_content, "test_empty")

        assert "empty" in str(exc_info.value).lower()

    def test_convert_jsonl_only_whitespace(self):
        """Test error handling for JSONL with only whitespace"""
        jsonl_content = b'   \n\n   \n'

        with pytest.raises(ValueError) as exc_info:
            convert_jsonl_to_sqlite(jsonl_content, "test_whitespace")

        assert "empty" in str(exc_info.value).lower()

    def test_convert_jsonl_malformed(self):
        """Test error handling for malformed JSONL"""
        jsonl_content = b'{"id": 1}\n{bad json}\n{"id": 3}\n'

        with pytest.raises(ValueError) as exc_info:
            convert_jsonl_to_sqlite(jsonl_content, "test_malformed")

        assert "Invalid JSON" in str(exc_info.value)

    def test_convert_jsonl_from_test_file(self):
        """Test converting actual test_simple.jsonl file"""
        test_file = Path("tests/assets/test_simple.jsonl")

        if test_file.exists():
            with open(test_file, 'rb') as f:
                content = f.read()

            result = convert_jsonl_to_sqlite(content, "test_simple")

            assert result["table_name"] == "test_simple"
            assert result["row_count"] == 3
            assert "id" in result["schema"]
            assert "name" in result["schema"]
            assert "price" in result["schema"]

    def test_convert_jsonl_from_events_file(self):
        """Test converting actual test_events.jsonl file with nested data"""
        test_file = Path("tests/assets/test_events.jsonl")

        if test_file.exists():
            with open(test_file, 'rb') as f:
                content = f.read()

            result = convert_jsonl_to_sqlite(content, "test_events")

            assert result["table_name"] == "test_events"
            assert result["row_count"] >= 3  # At least 3 rows
            assert "event_id" in result["schema"]
            assert "user__id" in result["schema"]
            assert "user__name" in result["schema"]
            assert "tags_0" in result["schema"]
            assert "tags_1" in result["schema"]
            assert "timestamp" in result["schema"]

    def test_sanitize_table_name_from_jsonl_filename(self):
        """Test table name sanitization for JSONL files"""
        assert sanitize_table_name("test_file.jsonl") == "test_file"
        assert sanitize_table_name("My Data.jsonl") == "My_Data"
        assert sanitize_table_name("data-2024.jsonl") == "data_2024"

        # Should start with letter or underscore
        result = sanitize_table_name("123data.jsonl")
        assert result.startswith("_")

    def test_convert_jsonl_table_replacement(self):
        """Test that uploading same filename overwrites existing table"""
        jsonl_content_1 = b'{"id": 1, "value": 100}\n'
        jsonl_content_2 = b'{"id": 2, "value": 200}\n{"id": 3, "value": 300}\n'

        # First upload
        result1 = convert_jsonl_to_sqlite(jsonl_content_1, "test_replace")
        assert result1["row_count"] == 1

        # Second upload with same table name
        result2 = convert_jsonl_to_sqlite(jsonl_content_2, "test_replace")
        assert result2["row_count"] == 2

        # Verify table was replaced, not appended
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM test_replace")
        count = cursor.fetchone()[0]
        conn.close()

        assert count == 2  # Should be 2, not 3
