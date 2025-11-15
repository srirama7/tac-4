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

def generate_natural_language_query(schema_info: Dict[str, Any]) -> str:
    """
    Generate an interesting natural language query based on database schema.
    Uses the same routing logic as generate_sql (OpenAI priority, then Anthropic).
    Returns a natural language query (max 2 sentences).
    """
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    # Check if any API key is available
    if not openai_key and not anthropic_key:
        raise ValueError("No LLM API key configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")

    # Format schema for prompt
    schema_description = format_schema_for_prompt(schema_info)

    # Create prompt for generating natural language queries
    prompt = f"""Given the following database schema:

{schema_description}

Generate an interesting natural language query that a user might want to ask about this data. The query should:
- Be specific and actionable based on the actual tables and columns available
- Be phrased as a question or request (e.g., "Show me...", "What are...", "How many...")
- Be limited to maximum 2 sentences
- Showcase the capabilities of natural language querying
- Be diverse and creative to provide variety

Examples of good queries:
- "Show me users who signed up in the last month"
- "What are the top 5 most expensive products?"
- "Count events by type and show me the distribution"
- "Find all users who haven't made a purchase yet"

Return ONLY the natural language query, no explanations or additional text.

Natural Language Query:"""

    # Route to appropriate provider (OpenAI priority)
    if openai_key:
        try:
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates natural language queries for databases."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,  # Higher temperature for more creative/diverse queries
                max_tokens=100
            )
            query_text = response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating query with OpenAI: {str(e)}")
    elif anthropic_key:
        try:
            client = Anthropic(api_key=anthropic_key)
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=100,
                temperature=0.7,  # Higher temperature for more creative/diverse queries
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            query_text = response.content[0].text.strip()
        except Exception as e:
            raise Exception(f"Error generating query with Anthropic: {str(e)}")

    # Clean up any markdown formatting
    if query_text.startswith("```"):
        lines = query_text.split("\n")
        query_text = "\n".join(lines[1:-1]) if len(lines) > 2 else query_text

    # Remove quotes if the LLM wrapped the query in quotes
    query_text = query_text.strip('"').strip("'")

    return query_text.strip()