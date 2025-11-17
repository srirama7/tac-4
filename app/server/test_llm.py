import os
import sys
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Import the actual module
from core.llm_processor import generate_sql
from core.data_models import QueryRequest

# Create a simple test request
request = QueryRequest(query="Show me all users")

# Print environment check
gemini_key = os.environ.get("GEMINI_API_KEY")
openai_key = os.environ.get("OPENAI_API_KEY")

print(f"GEMINI_API_KEY: {'SET' if gemini_key else 'NOT SET'}")
print(f"OPENAI_API_KEY: {'SET' if openai_key else 'NOT SET'}")
print()

# Try to call generate_sql with a dummy schema
schema_info = {
    'tables': {
        'users': {
            'columns': {'id': 'INTEGER', 'name': 'TEXT'},
            'row_count': 3
        }
    }
}

try:
    sql = generate_sql(request, schema_info)
    print(f"SUCCESS! Generated SQL: {sql}")
except Exception as e:
    print(f"ERROR: {str(e)}")
