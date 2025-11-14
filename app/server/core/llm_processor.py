import os
from typing import Dict, Any
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
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

def generate_sql_with_gemini(query_text: str, schema_info: Dict[str, Any]) -> str:
    """
    Generate SQL query using Google Gemini API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

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

        # Call Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=500
            )
        )

        sql = response.text.strip()

        # Clean up the SQL (remove markdown if present)
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]

        return sql.strip()

    except Exception as e:
        raise Exception(f"Error generating SQL with Gemini: {str(e)}")

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
    Priority: 1) Gemini API key exists, 2) OpenAI API key exists, 3) Anthropic API key exists, 4) request.llm_provider
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    # Check API key availability first (Gemini priority)
    if gemini_key:
        return generate_sql_with_gemini(request.query, schema_info)
    elif openai_key:
        return generate_sql_with_openai(request.query, schema_info)
    elif anthropic_key:
        return generate_sql_with_anthropic(request.query, schema_info)

    # Fall back to request preference if multiple keys available or none available
    if hasattr(request, 'llm_provider'):
        if request.llm_provider == "gemini":
            return generate_sql_with_gemini(request.query, schema_info)
        elif request.llm_provider == "openai":
            return generate_sql_with_openai(request.query, schema_info)
        else:
            return generate_sql_with_anthropic(request.query, schema_info)

    # Default fallback
    raise ValueError("No LLM API key available. Please set GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY environment variable.")

def generate_random_query_with_openai(schema_info: Dict[str, Any]) -> str:
    """
    Generate a random natural language query using OpenAI API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        client = OpenAI(api_key=api_key)

        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)

        # Create prompt for natural language query generation
        prompt = f"""Given the following database schema:

{schema_description}

Generate a single interesting natural language query that a user might ask about this data.

Rules:
- Generate ONLY a natural language question (NOT SQL)
- Maximum two sentences
- Make it interesting and showcase the data's potential insights
- Vary between different types of queries (aggregations, filters, comparisons, time-based analysis, joins)
- Be specific to the actual tables and columns available
- Make each query different and creative
- Focus on actionable insights that would be useful to a data analyst

Natural language query:"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a data analyst expert. Generate interesting natural language questions about data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,  # Higher temperature for more variety
            max_tokens=100
        )

        query = response.choices[0].message.content.strip()

        # Remove any markdown formatting or quotes
        query = query.replace("```", "").replace('"', '').replace("'", "").strip()

        return query

    except Exception as e:
        raise Exception(f"Error generating random query with OpenAI: {str(e)}")

def generate_random_query_with_anthropic(schema_info: Dict[str, Any]) -> str:
    """
    Generate a random natural language query using Anthropic API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        client = Anthropic(api_key=api_key)

        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)

        # Create prompt for natural language query generation
        prompt = f"""Given the following database schema:

{schema_description}

Generate a single interesting natural language query that a user might ask about this data.

Rules:
- Generate ONLY a natural language question (NOT SQL)
- Maximum two sentences
- Make it interesting and showcase the data's potential insights
- Vary between different types of queries (aggregations, filters, comparisons, time-based analysis, joins)
- Be specific to the actual tables and columns available
- Make each query different and creative
- Focus on actionable insights that would be useful to a data analyst

Natural language query:"""

        # Call Anthropic API
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            temperature=0.8,  # Higher temperature for more variety
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        query = response.content[0].text.strip()

        # Remove any markdown formatting or quotes
        query = query.replace("```", "").replace('"', '').replace("'", "").strip()

        return query

    except Exception as e:
        raise Exception(f"Error generating random query with Anthropic: {str(e)}")

def generate_random_query_with_gemini(schema_info: Dict[str, Any]) -> str:
    """
    Generate a random natural language query using Google Gemini API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)

        # Create prompt for natural language query generation
        prompt = f"""Given the following database schema:

{schema_description}

Generate a single interesting natural language query that a user might ask about this data.

Rules:
- Generate ONLY a natural language question (NOT SQL)
- Maximum two sentences
- Make it interesting and showcase the data's potential insights
- Vary between different types of queries (aggregations, filters, comparisons, time-based analysis, joins)
- Be specific to the actual tables and columns available
- Make each query different and creative
- Focus on actionable insights that would be useful to a data analyst

Natural language query:"""

        # Call Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,  # Higher temperature for more variety
                max_output_tokens=100
            )
        )

        query = response.text.strip()

        # Remove any markdown formatting or quotes
        query = query.replace("```", "").replace('"', '').replace("'", "").strip()

        return query

    except Exception as e:
        raise Exception(f"Error generating random query with Gemini: {str(e)}")

def generate_random_query(schema_info: Dict[str, Any]) -> str:
    """
    Generate a random natural language query based on database schema.
    Routes to appropriate LLM provider (Gemini priority, then OpenAI, then Anthropic).
    """
    # Handle empty schema
    if not schema_info or not schema_info.get('tables') or len(schema_info.get('tables', {})) == 0:
        return "Please upload some data first to generate queries."

    # Route to appropriate provider based on API key availability
    gemini_key = os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    if gemini_key:
        return generate_random_query_with_gemini(schema_info)
    elif openai_key:
        return generate_random_query_with_openai(schema_info)
    elif anthropic_key:
        return generate_random_query_with_anthropic(schema_info)
    else:
        raise ValueError("No LLM API key available. Please set GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY environment variable.")