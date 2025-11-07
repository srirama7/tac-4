import pytest
import json
import pandas as pd
import sqlite3
import os
import io
from pathlib import Path
from unittest.mock import patch
from core.file_processor import (
    convert_csv_to_sqlite,
    convert_json_to_sqlite,
    convert_jsonl_to_sqlite,
    parse_jsonl_file,
    flatten_record,
    discover_all_fields
)


@pytest.fixture
def test_db():
    """Create an in-memory test database"""
    # Create in-memory database
    conn = sqlite3.connect(':memory:')
    
    # Patch the database connection to use our in-memory database
    with patch('core.file_processor.sqlite3.connect') as mock_connect:
        mock_connect.return_value = conn
        yield conn
    
    conn.close()


@pytest.fixture
def test_assets_dir():
    """Get the path to test assets directory"""
    return Path(__file__).parent.parent / "assets"


class TestFileProcessor:
    
    def test_convert_csv_to_sqlite_success(self, test_db, test_assets_dir):
        # Load real CSV file
        csv_file = test_assets_dir / "test_users.csv"
        with open(csv_file, 'rb') as f:
            csv_data = f.read()
        
        table_name = "users"
        result = convert_csv_to_sqlite(csv_data, table_name)
        
        # Verify return structure
        assert result['table_name'] == table_name
        assert 'schema' in result
        assert 'row_count' in result
        assert 'sample_data' in result
        
        # Test the returned data
        assert result['row_count'] == 4  # 4 users in test file
        assert len(result['sample_data']) <= 5  # Should return up to 5 samples
        
        # Verify schema has expected columns (cleaned names)
        assert 'name' in result['schema']
        assert 'age' in result['schema'] 
        assert 'city' in result['schema']
        assert 'email' in result['schema']
        
        # Verify sample data structure and content
        john_data = next((item for item in result['sample_data'] if item['name'] == 'John Doe'), None)
        assert john_data is not None
        assert john_data['age'] == 25
        assert john_data['city'] == 'New York'
        assert john_data['email'] == 'john@example.com'
    
    def test_convert_csv_to_sqlite_column_cleaning(self, test_db, test_assets_dir):
        # Test column name cleaning with real file
        csv_file = test_assets_dir / "column_names.csv"
        with open(csv_file, 'rb') as f:
            csv_data = f.read()
        
        table_name = "test_users"
        result = convert_csv_to_sqlite(csv_data, table_name)
        
        # Verify columns were cleaned in the schema
        assert 'full_name' in result['schema']
        assert 'birth_date' in result['schema']
        assert 'email_address' in result['schema']
        assert 'phone_number' in result['schema']
        
        # Verify sample data has cleaned column names and actual content
        sample = result['sample_data'][0]
        assert 'full_name' in sample
        assert 'birth_date' in sample
        assert 'email_address' in sample
        assert sample['full_name'] == 'John Doe'
        assert sample['birth_date'] == '1990-01-15'
    
    def test_convert_csv_to_sqlite_with_inconsistent_data(self, test_db, test_assets_dir):
        # Test with CSV that has inconsistent row lengths - should raise error
        csv_file = test_assets_dir / "invalid.csv"
        with open(csv_file, 'rb') as f:
            csv_data = f.read()
        
        table_name = "inconsistent_table"
        
        # Pandas will fail on inconsistent CSV data
        with pytest.raises(Exception) as exc_info:
            convert_csv_to_sqlite(csv_data, table_name)
        
        assert "Error converting CSV to SQLite" in str(exc_info.value)
    
    def test_convert_json_to_sqlite_success(self, test_db, test_assets_dir):
        # Load real JSON file
        json_file = test_assets_dir / "test_products.json"
        with open(json_file, 'rb') as f:
            json_data = f.read()
        
        table_name = "products"
        result = convert_json_to_sqlite(json_data, table_name)
        
        # Verify return structure
        assert result['table_name'] == table_name
        assert 'schema' in result
        assert 'row_count' in result
        assert 'sample_data' in result
        
        # Test the returned data
        assert result['row_count'] == 3  # 3 products in test file
        assert len(result['sample_data']) == 3
        
        # Verify schema has expected columns
        assert 'id' in result['schema']
        assert 'name' in result['schema']
        assert 'price' in result['schema']
        assert 'category' in result['schema']
        assert 'in_stock' in result['schema']
        
        # Verify sample data structure and content
        laptop_data = next((item for item in result['sample_data'] if item['name'] == 'Laptop'), None)
        assert laptop_data is not None
        assert laptop_data['price'] == 999.99
        assert laptop_data['category'] == 'Electronics'
        assert laptop_data['in_stock'] == True
    
    def test_convert_json_to_sqlite_invalid_json(self):
        # Test with invalid JSON
        json_data = b'invalid json'
        table_name = "test_table"
        
        with pytest.raises(Exception) as exc_info:
            convert_json_to_sqlite(json_data, table_name)
        
        assert "Error converting JSON to SQLite" in str(exc_info.value)
    
    def test_convert_json_to_sqlite_not_array(self):
        # Test with JSON that's not an array
        json_data = b'{"name": "John", "age": 25}'
        table_name = "test_table"
        
        with pytest.raises(Exception) as exc_info:
            convert_json_to_sqlite(json_data, table_name)
        
        assert "JSON must be an array of objects" in str(exc_info.value)
    
    def test_convert_json_to_sqlite_empty_array(self):
        # Test with empty JSON array
        json_data = b'[]'
        table_name = "test_table"
        
        with pytest.raises(Exception) as exc_info:
            convert_json_to_sqlite(json_data, table_name)
        
        assert "JSON array is empty" in str(exc_info.value)

    # JSONL Tests

    def test_parse_jsonl_file_success(self):
        jsonl_data = b'{"name": "John", "age": 30}\n{"name": "Jane", "age": 25}\n'
        records = parse_jsonl_file(jsonl_data)

        assert len(records) == 2
        assert records[0]['name'] == 'John'
        assert records[0]['age'] == 30

    def test_flatten_record_nested_objects(self):
        record = {"user": {"name": "John", "address": {"city": "NYC"}}, "active": True}
        flattened = flatten_record(record)

        assert flattened['user__name'] == 'John'
        assert flattened['user__address__city'] == 'NYC'
        assert flattened['active'] == True

    def test_flatten_record_arrays(self):
        record = {"name": "Product", "tags": ["python", "sql", "data"]}
        flattened = flatten_record(record)

        assert flattened['name'] == 'Product'
        assert flattened['tags_0'] == 'python'
        assert flattened['tags_1'] == 'sql'

    def test_discover_all_fields_varying_schemas(self):
        records = [
            {"name": "John", "age": 30, "city": "NYC"},
            {"name": "Jane", "age": 25, "country": "USA"}
        ]
        fields = discover_all_fields(records)

        assert 'name' in fields
        assert 'age' in fields
        assert 'city' in fields
        assert 'country' in fields

    def test_convert_jsonl_to_sqlite_success(self, test_db, test_assets_dir):
        jsonl_file = test_assets_dir / "test_events.jsonl"
        with open(jsonl_file, 'rb') as f:
            jsonl_data = f.read()

        result = convert_jsonl_to_sqlite(jsonl_data, "events")

        assert result['table_name'] == "events"
        assert result['row_count'] == 4
        assert any('user__' in key for key in result['schema'])

    def test_convert_jsonl_to_sqlite_empty_file(self, test_db):
        jsonl_data = b''

        with pytest.raises(ValueError) as exc_info:
            convert_jsonl_to_sqlite(jsonl_data, "empty")

        assert "empty" in str(exc_info.value).lower()

    def test_convert_jsonl_to_sqlite_invalid_format(self, test_db, test_assets_dir):
        jsonl_file = test_assets_dir / "invalid.jsonl"
        with open(jsonl_file, 'rb') as f:
            jsonl_data = f.read()

        with pytest.raises(ValueError) as exc_info:
            convert_jsonl_to_sqlite(jsonl_data, "invalid")

        assert "Line 2" in str(exc_info.value)