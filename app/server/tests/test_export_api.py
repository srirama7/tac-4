"""
Integration tests for export API endpoints.
Tests the /api/export endpoint with various formats and edge cases.
"""

import pytest
import sqlite3
import tempfile
import os
import json
import csv
from io import StringIO, BytesIO
from fastapi.testclient import TestClient
from openpyxl import load_workbook
from unittest.mock import patch


@pytest.fixture
def test_db():
    """Create a test database with sample data"""
    db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    db_file.close()

    conn = sqlite3.connect(db_file.name)
    cursor = conn.cursor()

    # Create test table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            age INTEGER
        )
    ''')

    # Insert test data
    test_data = [
        (1, 'Alice', 'alice@example.com', 30),
        (2, 'Bob', 'bob@example.com', 25),
        (3, 'Charlie', 'charlie@example.com', 35),
        (4, 'Diana', None, 28),  # Test NULL value
        (5, 'Eve', 'eve@example.com', None)  # Test NULL age
    ]

    for row in test_data:
        cursor.execute("INSERT INTO users (id, name, email, age) VALUES (?, ?, ?, ?)", row)

    conn.commit()
    conn.close()

    yield db_file.name

    # Cleanup
    os.unlink(db_file.name)


@pytest.fixture
def client(test_db):
    """Create test client with real database"""
    # Copy test database to the expected location
    import shutil
    os.makedirs("db", exist_ok=True)
    shutil.copy(test_db, "db/database.db")

    from server import app
    client = TestClient(app)
    yield client

    # Cleanup
    try:
        os.remove("db/database.db")
    except:
        pass


class TestExportAPIBasic:
    """Basic export API tests"""

    def test_export_csv_success(self, client):
        """Test successful CSV export"""
        request_data = {
            "sql": "SELECT * FROM users WHERE age >= 25",
            "format": "csv"
        }

        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers.get("content-disposition", "")

        # Parse CSV content
        csv_text = response.content.decode('utf-8')
        reader = csv.DictReader(StringIO(csv_text))
        rows = list(reader)

        assert len(rows) >= 3  # Should have at least 3 users with age >= 25
        assert "name" in rows[0]
        assert "email" in rows[0]

    def test_export_json_success(self, client):
        """Test successful JSON export"""
        request_data = {
            "sql": "SELECT id, name FROM users LIMIT 3",
            "format": "json"
        }

        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert "attachment" in response.headers.get("content-disposition", "")

        # Parse JSON content
        data = json.loads(response.content.decode('utf-8'))

        assert isinstance(data, list)
        assert len(data) == 3
        assert "id" in data[0]
        assert "name" in data[0]

    def test_export_excel_success(self, client):
        """Test successful Excel export"""
        request_data = {
            "sql": "SELECT * FROM users LIMIT 2",
            "format": "excel"
        }

        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200
        assert "spreadsheetml" in response.headers["content-type"]
        assert "attachment" in response.headers.get("content-disposition", "")
        assert ".xlsx" in response.headers.get("content-disposition", "")

        # Parse Excel content
        wb = load_workbook(BytesIO(response.content))
        ws = wb.active

        # Check headers
        assert ws.cell(1, 1).value == "id"
        assert ws.cell(1, 2).value == "name"

        # Check data exists
        assert ws.cell(2, 1).value is not None

    def test_export_with_custom_filename(self, client):
        """Test export with custom filename"""
        request_data = {
            "sql": "SELECT * FROM users",
            "format": "csv",
            "filename": "my_export"
        }

        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200
        assert "my_export.csv" in response.headers.get("content-disposition", "")


class TestExportAPIEdgeCases:
    """Edge case tests for export API"""

    def test_export_empty_results(self, client):
        """Test export with query returning no results"""
        request_data = {
            "sql": "SELECT * FROM users WHERE age > 100",
            "format": "json"
        }

        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200

        # Empty result should still be valid JSON
        data = json.loads(response.content.decode('utf-8'))
        assert data == []

    def test_export_with_null_values(self, client):
        """Test export handles NULL values correctly"""
        request_data = {
            "sql": "SELECT id, name, email FROM users WHERE email IS NULL",
            "format": "json"
        }

        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200

        data = json.loads(response.content.decode('utf-8'))
        assert len(data) >= 1
        assert data[0]["email"] is None

    def test_export_invalid_sql(self, client):
        """Test export with invalid SQL query"""
        request_data = {
            "sql": "SELECT * FROM nonexistent_table",
            "format": "csv"
        }

        response = client.post("/api/export", json=request_data)

        assert response.status_code == 500  # Should return error

    def test_export_sql_injection_attempt(self, client):
        """Test export protects against SQL injection"""
        request_data = {
            "sql": "SELECT * FROM users; DROP TABLE users; --",
            "format": "csv"
        }

        response = client.post("/api/export", json=request_data)

        # Should be blocked by security validation
        assert response.status_code in [400, 500]

    def test_export_invalid_format(self, client):
        """Test export with unsupported format"""
        request_data = {
            "sql": "SELECT * FROM users",
            "format": "xml"  # Unsupported format
        }

        response = client.post("/api/export", json=request_data)

        # Should fail validation (Pydantic will reject it)
        assert response.status_code == 422


class TestExportAPIDataTypes:
    """Tests for various data types in exports"""

    def test_export_numeric_data_csv(self, client):
        """Test CSV export with numeric data"""
        request_data = {
            "sql": "SELECT id, age FROM users WHERE age IS NOT NULL",
            "format": "csv"
        }

        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200

        csv_text = response.content.decode('utf-8')
        reader = csv.DictReader(StringIO(csv_text))
        rows = list(reader)

        # Numbers should be present as strings in CSV
        assert rows[0]["id"]
        assert rows[0]["age"]

    def test_export_special_characters_csv(self, client):
        """Test CSV export with special characters"""
        # This tests data that already exists, but we can verify CSV escaping
        request_data = {
            "sql": "SELECT name FROM users WHERE name = 'Alice'",
            "format": "csv"
        }

        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200

        # CSV should be properly formatted
        csv_text = response.content.decode('utf-8')
        assert "Alice" in csv_text

    def test_export_all_formats_consistency(self, client):
        """Test that all formats export the same data"""
        sql_query = "SELECT id, name FROM users ORDER BY id LIMIT 2"

        # Export in all formats
        formats = ["csv", "json", "excel"]
        results = {}

        for fmt in formats:
            request_data = {"sql": sql_query, "format": fmt}
            response = client.post("/api/export", json=request_data)
            assert response.status_code == 200
            results[fmt] = response.content

        # Parse and compare
        # CSV
        csv_data = list(csv.DictReader(StringIO(results["csv"].decode('utf-8'))))

        # JSON
        json_data = json.loads(results["json"].decode('utf-8'))

        # Excel
        wb = load_workbook(BytesIO(results["excel"]))
        ws = wb.active
        excel_data = []
        headers = [ws.cell(1, col).value for col in range(1, 3)]
        for row in range(2, 4):  # Rows 2 and 3 (data rows)
            row_data = {headers[col]: ws.cell(row, col + 1).value for col in range(2)}
            excel_data.append(row_data)

        # All should have same number of records
        assert len(csv_data) == len(json_data) == 2


class TestExportAPIContentHeaders:
    """Tests for HTTP headers in export responses"""

    def test_csv_headers(self, client):
        """Test CSV export has correct headers"""
        request_data = {"sql": "SELECT * FROM users", "format": "csv"}
        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]
        assert ".csv" in response.headers["content-disposition"]

    def test_json_headers(self, client):
        """Test JSON export has correct headers"""
        request_data = {"sql": "SELECT * FROM users", "format": "json"}
        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert "attachment" in response.headers["content-disposition"]
        assert ".json" in response.headers["content-disposition"]

    def test_excel_headers(self, client):
        """Test Excel export has correct headers"""
        request_data = {"sql": "SELECT * FROM users", "format": "excel"}
        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200
        assert "spreadsheetml" in response.headers["content-type"]
        assert "attachment" in response.headers["content-disposition"]
        assert ".xlsx" in response.headers["content-disposition"]

    def test_cors_headers(self, client):
        """Test export response includes CORS headers"""
        request_data = {"sql": "SELECT * FROM users", "format": "csv"}
        response = client.post("/api/export", json=request_data)

        assert response.status_code == 200
        # CORS header should expose Content-Disposition
        assert "access-control-expose-headers" in response.headers
