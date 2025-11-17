import os
from typing import Dict, Any
from openai import OpenAI
from anthropic import Anthropic
from core.data_models import QueryRequest

def generate_sql_with_openai(query_text: str, schema_info: Dict[str, Any]) -> str:
    """
    Generate SQL query using OpenAI API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        client = OpenAI(api_key=api_key)
        
        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)
        
        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Convert this natural language query to SQL: "{query_text}"

Rules:
- Return ONLY the SQL query, no explanations
- Use proper SQLite syntax
- Handle date/time queries appropriately (e.g., "last week" = date('now', '-7 days'))
- Be careful with column names and table names
- If the query is ambiguous, make reasonable assumptions
- For multi-table queries, use proper JOIN conditions to avoid Cartesian products
- Limit results to reasonable amounts (e.g., add LIMIT 100 for large result sets)
- When joining tables, use meaningful relationships between tables

SQL Query:"""
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a SQL expert. Convert natural language to SQL queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        sql = response.choices[0].message.content.strip()
        
        # Clean up the SQL (remove markdown if present)
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]
        
        return sql.strip()
        
    except Exception as e:
        raise Exception(f"Error generating SQL with OpenAI: {str(e)}")

def generate_sql_with_anthropic(query_text: str, schema_info: Dict[str, Any]) -> str:
    """
    Generate SQL query using Anthropic API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        client = Anthropic(api_key=api_key)
        
        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)
        
        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Convert this natural language query to SQL: "{query_text}"

Rules:
- Return ONLY the SQL query, no explanations
- Use proper SQLite syntax
- Handle date/time queries appropriately (e.g., "last week" = date('now', '-7 days'))
- Be careful with column names and table names
- If the query is ambiguous, make reasonable assumptions
- For multi-table queries, use proper JOIN conditions to avoid Cartesian products
- Limit results to reasonable amounts (e.g., add LIMIT 100 for large result sets)
- When joining tables, use meaningful relationships between tables

SQL Query:"""
        
        # Call Anthropic API
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        sql = response.content[0].text.strip()
        
        # Clean up the SQL (remove markdown if present)
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]
        
        return sql.strip()
        
    except Exception as e:
        raise Exception(f"Error generating SQL with Anthropic: {str(e)}")

def format_schema_for_prompt(schema_info: Dict[str, Any]) -> str:
    """
    Format database schema for LLM prompt
    """
    lines = []
    
    for table_name, table_info in schema_info.get('tables', {}).items():
        lines.append(f"Table: {table_name}")
        lines.append("Columns:")
        
        for col_name, col_type in table_info['columns'].items():
            lines.append(f"  - {col_name} ({col_type})")
        
        lines.append(f"Row count: {table_info['row_count']}")
        lines.append("")
    
    return "\n".join(lines)

def generate_sql(request: QueryRequest, schema_info: Dict[str, Any]) -> str:
    """
    Route to appropriate LLM provider based on API key availability and request preference.
    Priority: 1) OpenAI API key exists, 2) Anthropic API key exists, 3) request.llm_provider
    """
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    # Check API key availability first (OpenAI priority)
    if openai_key:
        return generate_sql_with_openai(request.query, schema_info)
    elif anthropic_key:
        return generate_sql_with_anthropic(request.query, schema_info)

    # Fall back to request preference if both keys available or neither available
    if request.llm_provider == "openai":
        return generate_sql_with_openai(request.query, schema_info)
    else:
        return generate_sql_with_anthropic(request.query, schema_info)

def generate_random_nl_query_with_openai(schema_info: Dict[str, Any]) -> str:
    """
    Generate a random natural language query using OpenAI API based on database schema
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        client = OpenAI(api_key=api_key)

        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)

        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Generate an interesting and contextually-relevant natural language query that could be asked about this data.

Requirements:
- The query should reference actual table and column names from the schema
- Create queries that demonstrate various capabilities like aggregations, filtering, sorting, or joins
- Make the query interesting and useful, not just "show all records"
- Limit your response to a maximum of TWO sentences
- Return ONLY the natural language query, no explanations or additional text
- Use conversational language that a non-technical user would use

Examples of good queries:
- "Show me the top 5 users who signed up most recently"
- "What's the average price of products in each category?"
- "How many orders were placed last month?"

Natural Language Query:"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates natural language database queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )

        query = response.choices[0].message.content.strip()

        # Remove any quotes that might wrap the query
        if query.startswith('"') and query.endswith('"'):
            query = query[1:-1]
        if query.startswith("'") and query.endswith("'"):
            query = query[1:-1]

        return query

    except Exception as e:
        raise Exception(f"Error generating query with OpenAI: {str(e)}")

def generate_random_nl_query_with_anthropic(schema_info: Dict[str, Any]) -> str:
    """
    Generate a random natural language query using Anthropic API based on database schema
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        client = Anthropic(api_key=api_key)

        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)

        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Generate an interesting and contextually-relevant natural language query that could be asked about this data.

Requirements:
- The query should reference actual table and column names from the schema
- Create queries that demonstrate various capabilities like aggregations, filtering, sorting, or joins
- Make the query interesting and useful, not just "show all records"
- Limit your response to a maximum of TWO sentences
- Return ONLY the natural language query, no explanations or additional text
- Use conversational language that a non-technical user would use

Examples of good queries:
- "Show me the top 5 users who signed up most recently"
- "What's the average price of products in each category?"
- "How many orders were placed last month?"

Natural Language Query:"""

        # Call Anthropic API
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        query = response.content[0].text.strip()

        # Remove any quotes that might wrap the query
        if query.startswith('"') and query.endswith('"'):
            query = query[1:-1]
        if query.startswith("'") and query.endswith("'"):
            query = query[1:-1]

        return query

    except Exception as e:
        raise Exception(f"Error generating query with Anthropic: {str(e)}")

def generate_random_nl_query(schema_info: Dict[str, Any]) -> str:
    """
    Generate a random natural language query based on database schema.
    Routes to appropriate LLM provider based on API key availability.
    Priority: 1) OpenAI API key exists, 2) Anthropic API key exists
    """
    # Check if schema has tables
    if not schema_info.get('tables') or len(schema_info['tables']) == 0:
        raise ValueError("No tables found in database. Please upload data first.")

    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    # Check API key availability (OpenAI priority)
    if openai_key:
        return generate_random_nl_query_with_openai(schema_info)
    elif anthropic_key:
        return generate_random_nl_query_with_anthropic(schema_info)
    else:
        raise ValueError("No LLM API keys found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY.")