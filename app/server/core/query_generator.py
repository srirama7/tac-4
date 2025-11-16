import os
from typing import Dict, Any
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai


def generate_query_suggestion_with_openai(schema_info: Dict[str, Any]) -> str:
    """
    Generate natural language query suggestion using OpenAI API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        client = OpenAI(api_key=api_key)

        # Format schema for prompt
        schema_description = format_schema_for_suggestion_prompt(schema_info)

        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Generate an interesting natural language question that a user might want to ask about this data.

Rules:
- Maximum 2 sentences
- Use natural, conversational language
- Make it relevant to the actual columns and tables present
- Focus on practical, insightful queries
- For multiple tables, consider both single-table and join queries
- Avoid questions that are too simple (like "show all records")
- Create questions that demonstrate the power of natural language querying

Natural language query:"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates interesting natural language questions about database data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Higher temperature for more creative suggestions
            max_tokens=150
        )

        query = response.choices[0].message.content.strip()

        # Remove quotes if present
        if query.startswith('"') and query.endswith('"'):
            query = query[1:-1]
        if query.startswith("'") and query.endswith("'"):
            query = query[1:-1]

        return query

    except Exception as e:
        raise Exception(f"Error generating query suggestion with OpenAI: {str(e)}")


def generate_query_suggestion_with_anthropic(schema_info: Dict[str, Any]) -> str:
    """
    Generate natural language query suggestion using Anthropic API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        client = Anthropic(api_key=api_key)

        # Format schema for prompt
        schema_description = format_schema_for_suggestion_prompt(schema_info)

        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Generate an interesting natural language question that a user might want to ask about this data.

Rules:
- Maximum 2 sentences
- Use natural, conversational language
- Make it relevant to the actual columns and tables present
- Focus on practical, insightful queries
- For multiple tables, consider both single-table and join queries
- Avoid questions that are too simple (like "show all records")
- Create questions that demonstrate the power of natural language querying

Natural language query:"""

        # Call Anthropic API
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            temperature=0.7,  # Higher temperature for more creative suggestions
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        query = response.content[0].text.strip()

        # Remove quotes if present
        if query.startswith('"') and query.endswith('"'):
            query = query[1:-1]
        if query.startswith("'") and query.endswith("'"):
            query = query[1:-1]

        return query

    except Exception as e:
        raise Exception(f"Error generating query suggestion with Anthropic: {str(e)}")


def generate_query_suggestion_with_gemini(schema_info: Dict[str, Any]) -> str:
    """
    Generate natural language query suggestion using Google Gemini API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Format schema for prompt
        schema_description = format_schema_for_suggestion_prompt(schema_info)

        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Generate an interesting natural language question that a user might want to ask about this data.

Rules:
- Maximum 2 sentences
- Use natural, conversational language
- Make it relevant to the actual columns and tables present
- Focus on practical, insightful queries
- For multiple tables, consider both single-table and join queries
- Avoid questions that are too simple (like "show all records")
- Create questions that demonstrate the power of natural language querying

Natural language query:"""

        # Call Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,  # Higher temperature for more creative suggestions
                max_output_tokens=150,
            )
        )

        query = response.text.strip()

        # Remove quotes if present
        if query.startswith('"') and query.endswith('"'):
            query = query[1:-1]
        if query.startswith("'") and query.endswith("'"):
            query = query[1:-1]

        return query

    except Exception as e:
        raise Exception(f"Error generating query suggestion with Gemini: {str(e)}")


def format_schema_for_suggestion_prompt(schema_info: Dict[str, Any]) -> str:
    """
    Format database schema for query suggestion prompt
    """
    lines = []

    tables = schema_info.get('tables', {})

    if not tables:
        return "No tables available"

    for table_name, table_info in tables.items():
        lines.append(f"Table: {table_name}")
        lines.append("Columns:")

        columns = table_info.get('columns', {})
        for col_name, col_type in columns.items():
            lines.append(f"  - {col_name} ({col_type})")

        row_count = table_info.get('row_count', 0)
        lines.append(f"Row count: {row_count}")
        lines.append("")

    return "\n".join(lines)


def generate_query_suggestion(schema_info: Dict[str, Any], llm_provider: str = "gemini") -> str:
    """
    Generate a natural language query suggestion based on database schema.
    Routes to appropriate LLM provider based on API key availability.
    Priority: 1) Gemini API key (recommended for SQL), 2) OpenAI, 3) Anthropic, 4) llm_provider parameter

    Args:
        schema_info: Database schema information with tables, columns, and row counts
        llm_provider: Preferred LLM provider ("gemini", "openai", or "anthropic")

    Returns:
        Natural language query suggestion (max 2 sentences)

    Raises:
        ValueError: If schema is empty or no API keys are configured
        Exception: If LLM API call fails
    """
    # Validate schema
    if not schema_info or not schema_info.get('tables'):
        raise ValueError("Database is empty. Please upload data first.")

    # Check API key availability
    gemini_key = os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    if not gemini_key and not openai_key and not anthropic_key:
        raise ValueError("No LLM API keys configured. Please set GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY.")

    # Route to appropriate provider (Gemini priority for SQL operations)
    if gemini_key:
        return generate_query_suggestion_with_gemini(schema_info)
    elif openai_key:
        return generate_query_suggestion_with_openai(schema_info)
    elif anthropic_key:
        return generate_query_suggestion_with_anthropic(schema_info)

    # Fall back to request preference if multiple keys available
    if llm_provider == "gemini":
        return generate_query_suggestion_with_gemini(schema_info)
    elif llm_provider == "openai":
        return generate_query_suggestion_with_openai(schema_info)
    else:
        return generate_query_suggestion_with_anthropic(schema_info)
