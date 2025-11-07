import json
import pandas as pd
import sqlite3
import io
import re
from typing import Dict, Any, List, Set
from .sql_security import (
    execute_query_safely,
    validate_identifier,
    SQLSecurityError
)
from .constants import NESTED_FIELD_DELIMITER, LIST_INDEX_DELIMITER

def sanitize_table_name(table_name: str) -> str:
    """
    Sanitize table name for SQLite by removing/replacing bad characters
    and validating against SQL injection
    """
    # Remove file extension if present
    if '.' in table_name:
        table_name = table_name.rsplit('.', 1)[0]
    
    # Replace bad characters with underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', table_name)
    
    # Ensure it starts with a letter or underscore
    if sanitized and not sanitized[0].isalpha() and sanitized[0] != '_':
        sanitized = '_' + sanitized
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = 'table'
    
    # Validate the sanitized name
    try:
        validate_identifier(sanitized, "table")
    except SQLSecurityError:
        # If validation fails, use a safe default
        sanitized = f"table_{hash(table_name) % 100000}"
    
    return sanitized

def convert_csv_to_sqlite(csv_content: bytes, table_name: str) -> Dict[str, Any]:
    """
    Convert CSV file content to SQLite table
    """
    try:
        # Sanitize table name
        table_name = sanitize_table_name(table_name)
        
        # Read CSV into pandas DataFrame
        df = pd.read_csv(io.BytesIO(csv_content))
        
        # Clean column names
        df.columns = [col.lower().replace(' ', '_').replace('-', '_') for col in df.columns]
        
        # Connect to SQLite database
        conn = sqlite3.connect("db/database.db")
        
        # Write DataFrame to SQLite
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # Get schema information using safe query execution
        cursor_info = execute_query_safely(
            conn,
            "PRAGMA table_info({table})",
            identifier_params={'table': table_name}
        )
        columns_info = cursor_info.fetchall()
        
        schema = {}
        for col in columns_info:
            schema[col[1]] = col[2]  # column_name: data_type
        
        # Get sample data using safe query execution
        cursor_sample = execute_query_safely(
            conn,
            "SELECT * FROM {table} LIMIT 5",
            identifier_params={'table': table_name}
        )
        sample_rows = cursor_sample.fetchall()
        column_names = [col[1] for col in columns_info]
        sample_data = [dict(zip(column_names, row)) for row in sample_rows]
        
        # Get row count using safe query execution
        cursor_count = execute_query_safely(
            conn,
            "SELECT COUNT(*) FROM {table}",
            identifier_params={'table': table_name}
        )
        row_count = cursor_count.fetchone()[0]
        
        conn.close()
        
        return {
            'table_name': table_name,
            'schema': schema,
            'row_count': row_count,
            'sample_data': sample_data
        }
        
    except Exception as e:
        raise Exception(f"Error converting CSV to SQLite: {str(e)}")

def convert_json_to_sqlite(json_content: bytes, table_name: str) -> Dict[str, Any]:
    """
    Convert JSON file content to SQLite table
    """
    try:
        # Sanitize table name
        table_name = sanitize_table_name(table_name)
        
        # Parse JSON
        data = json.loads(json_content.decode('utf-8'))
        
        # Ensure it's a list of objects
        if not isinstance(data, list):
            raise ValueError("JSON must be an array of objects")
        
        if not data:
            raise ValueError("JSON array is empty")
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        
        # Clean column names
        df.columns = [col.lower().replace(' ', '_').replace('-', '_') for col in df.columns]
        
        # Connect to SQLite database
        conn = sqlite3.connect("db/database.db")
        
        # Write DataFrame to SQLite
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # Get schema information using safe query execution
        cursor_info = execute_query_safely(
            conn,
            "PRAGMA table_info({table})",
            identifier_params={'table': table_name}
        )
        columns_info = cursor_info.fetchall()
        
        schema = {}
        for col in columns_info:
            schema[col[1]] = col[2]  # column_name: data_type
        
        # Get sample data using safe query execution
        cursor_sample = execute_query_safely(
            conn,
            "SELECT * FROM {table} LIMIT 5",
            identifier_params={'table': table_name}
        )
        sample_rows = cursor_sample.fetchall()
        column_names = [col[1] for col in columns_info]
        sample_data = [dict(zip(column_names, row)) for row in sample_rows]
        
        # Get row count using safe query execution
        cursor_count = execute_query_safely(
            conn,
            "SELECT COUNT(*) FROM {table}",
            identifier_params={'table': table_name}
        )
        row_count = cursor_count.fetchone()[0]
        
        conn.close()
        
        return {
            'table_name': table_name,
            'schema': schema,
            'row_count': row_count,
            'sample_data': sample_data
        }

    except Exception as e:
        raise Exception(f"Error converting JSON to SQLite: {str(e)}")


def discover_all_fields(records: List[Dict[str, Any]], prefix: str = "") -> Set[str]:
    """
    Discover all unique field paths across all records by recursively traversing
    nested objects and arrays.

    This function scans through all records to find every possible field, handling
    cases where different records have different schemas. It flattens nested structures
    using delimiter-based naming (e.g., 'user__address__city', 'tags_0', 'tags_1').

    Args:
        records: List of dictionary records to scan for fields
        prefix: Current field path prefix (used in recursion)

    Returns:
        Set of all unique field paths discovered across all records

    Example:
        >>> records = [
        ...     {"name": "John", "address": {"city": "NYC"}},
        ...     {"name": "Jane", "address": {"city": "LA", "zip": "90001"}},
        ...     {"name": "Bob", "tags": ["python", "sql"]}
        ... ]
        >>> fields = discover_all_fields(records)
        >>> sorted(fields)
        ['address__city', 'address__zip', 'name', 'tags_0', 'tags_1']
    """
    fields = set()

    for record in records:
        if not isinstance(record, dict):
            continue

        for key, value in record.items():
            # Build the field path with prefix
            field_path = f"{prefix}{NESTED_FIELD_DELIMITER}{key}" if prefix else key

            if isinstance(value, dict):
                # Recursively discover fields in nested objects
                nested_fields = discover_all_fields([value], field_path)
                fields.update(nested_fields)
            elif isinstance(value, list):
                # For arrays, create indexed fields for each item
                for i, item in enumerate(value):
                    indexed_field = f"{field_path}{LIST_INDEX_DELIMITER}{i}"
                    if isinstance(item, dict):
                        # Recursively discover fields in nested objects within arrays
                        nested_fields = discover_all_fields([item], indexed_field)
                        fields.update(nested_fields)
                    else:
                        # Primitive value in array
                        fields.add(indexed_field)
            else:
                # Primitive value
                fields.add(field_path)

    return fields


def flatten_record(record: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    """
    Flatten a nested dictionary/record into a single-level dictionary with
    concatenated field names.

    Nested objects are flattened using NESTED_FIELD_DELIMITER ('__'), and arrays
    are flattened using indexed notation with LIST_INDEX_DELIMITER ('_').

    Args:
        record: The dictionary record to flatten
        prefix: Current field path prefix (used in recursion)

    Returns:
        Flattened dictionary with concatenated field names as keys

    Example:
        >>> record = {
        ...     "user": {
        ...         "name": "John",
        ...         "address": {"city": "NYC", "zip": "10001"}
        ...     },
        ...     "tags": ["python", "sql"],
        ...     "active": True
        ... }
        >>> flattened = flatten_record(record)
        >>> flattened
        {
            'user__name': 'John',
            'user__address__city': 'NYC',
            'user__address__zip': '10001',
            'tags_0': 'python',
            'tags_1': 'sql',
            'active': True
        }
    """
    flattened = {}

    for key, value in record.items():
        # Build the field path with prefix
        field_path = f"{prefix}{NESTED_FIELD_DELIMITER}{key}" if prefix else key

        if isinstance(value, dict):
            # Recursively flatten nested objects
            nested_flat = flatten_record(value, field_path)
            flattened.update(nested_flat)
        elif isinstance(value, list):
            # Flatten arrays with indexed notation
            for i, item in enumerate(value):
                indexed_field = f"{field_path}{LIST_INDEX_DELIMITER}{i}"
                if isinstance(item, dict):
                    # Recursively flatten nested objects within arrays
                    nested_flat = flatten_record(item, indexed_field)
                    flattened.update(nested_flat)
                else:
                    # Convert primitive values to strings for SQLite compatibility
                    flattened[indexed_field] = str(item) if item is not None else None
        else:
            # Handle primitive values - convert to string if needed for SQLite compatibility
            if isinstance(value, (str, int, float, bool)) or value is None:
                flattened[field_path] = value
            else:
                flattened[field_path] = str(value)

    return flattened


def parse_jsonl_file(jsonl_content: bytes) -> List[Dict[str, Any]]:
    """
    Parse a JSONL (JSON Lines) file where each line is a separate JSON object.

    JSONL format contains one JSON object per line, commonly used for streaming
    data, logs, and large datasets. This function handles empty lines, trailing
    newlines, and provides clear error messages with line numbers for malformed JSON.

    Args:
        jsonl_content: The raw bytes content of the JSONL file

    Returns:
        List of parsed JSON objects (dictionaries)

    Raises:
        ValueError: If the file contains malformed JSON with line number information

    Example:
        >>> content = b'{"name": "John", "age": 30}\\n{"name": "Jane", "age": 25}\\n'
        >>> records = parse_jsonl_file(content)
        >>> len(records)
        2
        >>> records[0]
        {'name': 'John', 'age': 30}
    """
    try:
        # Decode bytes to UTF-8 text
        text = jsonl_content.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid UTF-8 encoding in JSONL file: {str(e)}")

    records = []
    lines = text.split('\n')

    for line_num, line in enumerate(lines, 1):
        # Skip empty lines and lines with only whitespace
        line = line.strip()
        if not line:
            continue

        try:
            # Parse each line as a separate JSON object
            obj = json.loads(line)
            if not isinstance(obj, dict):
                raise ValueError(f"Line {line_num}: Expected JSON object, got {type(obj).__name__}")
            records.append(obj)
        except json.JSONDecodeError as e:
            raise ValueError(f"Line {line_num}: Invalid JSON - {str(e)}")

    return records


def convert_jsonl_to_sqlite(jsonl_content: bytes, table_name: str) -> Dict[str, Any]:
    """
    Convert JSONL (JSON Lines) file content to SQLite table with flattened nested structures.

    This function parses a JSONL file where each line is a separate JSON object, discovers
    all possible fields across all records (handling varying schemas), flattens nested objects
    and arrays using delimiter-based naming, and creates a comprehensive SQLite table.

    Nested objects are flattened using '__' delimiter (e.g., 'user__address__city')
    Arrays are flattened using indexed notation (e.g., 'tags_0', 'tags_1')

    Args:
        jsonl_content: The raw bytes content of the JSONL file
        table_name: The desired name for the SQLite table

    Returns:
        Dictionary containing:
            - table_name: Sanitized table name used in SQLite
            - schema: Dictionary mapping column names to SQLite data types
            - row_count: Total number of rows in the table
            - sample_data: List of up to 5 sample records from the table

    Raises:
        ValueError: If file is empty or contains invalid JSONL format
        Exception: If any other error occurs during processing

    Example:
        >>> jsonl_content = b'''{"user": {"name": "John"}, "tags": ["python"]}
        ... {"user": {"name": "Jane", "age": 25}, "tags": ["sql", "data"]}'''
        >>> result = convert_jsonl_to_sqlite(jsonl_content, "events")
        >>> result['table_name']
        'events'
        >>> 'user__name' in result['schema']
        True
        >>> 'tags_0' in result['schema']
        True
    """
    try:
        # Sanitize table name
        table_name = sanitize_table_name(table_name)

        # Parse JSONL file line by line
        records = parse_jsonl_file(jsonl_content)

        # Validate that file is not empty
        if not records:
            raise ValueError("JSONL file is empty or contains no valid JSON objects")

        # Discover all possible fields across all records
        all_fields = discover_all_fields(records)
        all_fields_sorted = sorted(all_fields)  # Sort for consistent column ordering

        # Flatten all records
        flattened_records = []
        for record in records:
            flat_record = flatten_record(record)
            # Ensure all discovered fields exist in each record (fill with None if missing)
            complete_record = {field: flat_record.get(field, None) for field in all_fields_sorted}
            flattened_records.append(complete_record)

        # Convert to pandas DataFrame
        df = pd.DataFrame(flattened_records)

        # Clean column names (lowercase, replace spaces and hyphens with underscores)
        df.columns = [col.lower().replace(' ', '_').replace('-', '_') for col in df.columns]

        # Connect to SQLite database
        conn = sqlite3.connect("db/database.db")

        # Write DataFrame to SQLite
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        # Get schema information using safe query execution
        cursor_info = execute_query_safely(
            conn,
            "PRAGMA table_info({table})",
            identifier_params={'table': table_name}
        )
        columns_info = cursor_info.fetchall()

        schema = {}
        for col in columns_info:
            schema[col[1]] = col[2]  # column_name: data_type

        # Get sample data using safe query execution
        cursor_sample = execute_query_safely(
            conn,
            "SELECT * FROM {table} LIMIT 5",
            identifier_params={'table': table_name}
        )
        sample_rows = cursor_sample.fetchall()
        column_names = [col[1] for col in columns_info]
        sample_data = [dict(zip(column_names, row)) for row in sample_rows]

        # Get row count using safe query execution
        cursor_count = execute_query_safely(
            conn,
            "SELECT COUNT(*) FROM {table}",
            identifier_params={'table': table_name}
        )
        row_count = cursor_count.fetchone()[0]

        conn.close()

        return {
            'table_name': table_name,
            'schema': schema,
            'row_count': row_count,
            'sample_data': sample_data
        }

    except ValueError as e:
        # Re-raise ValueError with original message (already user-friendly)
        raise e
    except Exception as e:
        raise Exception(f"Error converting JSONL to SQLite: {str(e)}")