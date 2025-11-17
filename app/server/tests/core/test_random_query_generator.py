import pytest
from unittest.mock import patch, MagicMock
from core.llm_processor import (
    generate_random_query,
    generate_random_query_with_openai,
    generate_random_query_with_anthropic
)


class TestRandomQueryGenerator:
    """Test suite for random query generation functionality"""

    @pytest.fixture
    def empty_schema(self):
        """Schema with no tables"""
        return {"tables": {}}

    @pytest.fixture
    def single_table_schema(self):
        """Schema with a single table containing mixed column types"""
        return {
            "tables": {
                "users": {
                    "columns": {
                        "id": "INTEGER",
                        "name": "TEXT",
                        "email": "TEXT",
                        "age": "INTEGER",
                        "created_at": "TIMESTAMP"
                    },
                    "row_count": 150
                }
            }
        }

    @pytest.fixture
    def multiple_tables_schema(self):
        """Schema with multiple tables for testing join queries"""
        return {
            "tables": {
                "users": {
                    "columns": {
                        "id": "INTEGER",
                        "name": "TEXT",
                        "email": "TEXT"
                    },
                    "row_count": 100
                },
                "orders": {
                    "columns": {
                        "id": "INTEGER",
                        "user_id": "INTEGER",
                        "total": "REAL",
                        "order_date": "TIMESTAMP"
                    },
                    "row_count": 500
                }
            }
        }

    @pytest.fixture
    def mock_openai_response(self):
        """Mock OpenAI API response"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "What is the average age of all users?"
        return mock_response

    @pytest.fixture
    def mock_anthropic_response(self):
        """Mock Anthropic API response"""
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Show me the total number of orders placed last week."
        return mock_response

    def test_generate_random_query_with_openai_single_table(self, single_table_schema, mock_openai_response):
        """Test query generation with OpenAI for single table"""
        with patch('core.llm_processor.os.environ.get') as mock_env, \
             patch('core.llm_processor.OpenAI') as mock_openai_class:

            # Setup mocks
            mock_env.return_value = "test-api-key"
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_openai_response
            mock_openai_class.return_value = mock_client

            # Generate query
            query = generate_random_query_with_openai(single_table_schema)

            # Assertions
            assert query == "What is the average age of all users?"
            mock_client.chat.completions.create.assert_called_once()
            call_args = mock_client.chat.completions.create.call_args
            assert call_args.kwargs['temperature'] == 0.9
            assert call_args.kwargs['model'] == "gpt-4.1-mini"

    def test_generate_random_query_with_anthropic_single_table(self, single_table_schema, mock_anthropic_response):
        """Test query generation with Anthropic for single table"""
        with patch('core.llm_processor.os.environ.get') as mock_env, \
             patch('core.llm_processor.Anthropic') as mock_anthropic_class:

            # Setup mocks
            mock_env.return_value = "test-api-key"
            mock_client = MagicMock()
            mock_client.messages.create.return_value = mock_anthropic_response
            mock_anthropic_class.return_value = mock_client

            # Generate query
            query = generate_random_query_with_anthropic(single_table_schema)

            # Assertions
            assert query == "Show me the total number of orders placed last week."
            mock_client.messages.create.assert_called_once()
            call_args = mock_client.messages.create.call_args
            assert call_args.kwargs['temperature'] == 0.9
            assert call_args.kwargs['model'] == "claude-3-haiku-20240307"

    def test_generate_random_query_routes_to_openai_when_key_exists(self, single_table_schema, mock_openai_response):
        """Test that generate_random_query routes to OpenAI when API key exists"""
        with patch('core.llm_processor.os.environ.get') as mock_env, \
             patch('core.llm_processor.OpenAI') as mock_openai_class:

            # Setup mocks - only OpenAI key exists
            def get_env(key):
                if key == "OPENAI_API_KEY":
                    return "openai-key"
                return None

            mock_env.side_effect = get_env
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_openai_response
            mock_openai_class.return_value = mock_client

            # Generate query
            query = generate_random_query(single_table_schema)

            # Assertions
            assert query == "What is the average age of all users?"
            mock_client.chat.completions.create.assert_called_once()

    def test_generate_random_query_routes_to_anthropic_when_no_openai_key(self, single_table_schema, mock_anthropic_response):
        """Test that generate_random_query routes to Anthropic when only Anthropic key exists"""
        with patch('core.llm_processor.os.environ.get') as mock_env, \
             patch('core.llm_processor.Anthropic') as mock_anthropic_class:

            # Setup mocks - only Anthropic key exists
            def get_env(key):
                if key == "ANTHROPIC_API_KEY":
                    return "anthropic-key"
                return None

            mock_env.side_effect = get_env
            mock_client = MagicMock()
            mock_client.messages.create.return_value = mock_anthropic_response
            mock_anthropic_class.return_value = mock_client

            # Generate query
            query = generate_random_query(single_table_schema)

            # Assertions
            assert query == "Show me the total number of orders placed last week."
            mock_client.messages.create.assert_called_once()

    def test_generate_random_query_error_when_no_api_keys(self, single_table_schema):
        """Test that generate_random_query raises error when no API keys are configured"""
        with patch('core.llm_processor.os.environ.get') as mock_env:
            # No API keys available
            mock_env.return_value = None

            # Should raise ValueError
            with pytest.raises(ValueError) as exc_info:
                generate_random_query(single_table_schema)

            assert "No LLM API key configured" in str(exc_info.value)

    def test_query_length_limitation_openai(self, single_table_schema):
        """Test that queries longer than two sentences are truncated"""
        with patch('core.llm_processor.os.environ.get') as mock_env, \
             patch('core.llm_processor.OpenAI') as mock_openai_class:

            # Setup mocks with long response
            mock_env.return_value = "test-api-key"
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "First sentence. Second sentence. Third sentence. Fourth sentence."

            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai_class.return_value = mock_client

            # Generate query
            query = generate_random_query_with_openai(single_table_schema)

            # Assertions - should only have two sentences
            sentences = query.split('. ')
            assert len(sentences) <= 3  # "First. Second." splits into 2 parts (third is empty after final .)
            assert query == "First sentence. Second sentence."

    def test_query_cleaning_removes_quotes(self, single_table_schema):
        """Test that quotes and markdown are removed from generated queries"""
        with patch('core.llm_processor.os.environ.get') as mock_env, \
             patch('core.llm_processor.OpenAI') as mock_openai_class:

            # Setup mocks with quoted response
            mock_env.return_value = "test-api-key"
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = '"What is the average age?"'

            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai_class.return_value = mock_client

            # Generate query
            query = generate_random_query_with_openai(single_table_schema)

            # Assertions - quotes should be removed
            assert query == "What is the average age?"
            assert not query.startswith('"')
            assert not query.endswith('"')

    def test_openai_error_handling(self, single_table_schema):
        """Test error handling when OpenAI API call fails"""
        with patch('core.llm_processor.os.environ.get') as mock_env, \
             patch('core.llm_processor.OpenAI') as mock_openai_class:

            # Setup mocks to raise exception
            mock_env.return_value = "test-api-key"
            mock_client = MagicMock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_openai_class.return_value = mock_client

            # Should raise exception with descriptive message
            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_openai(single_table_schema)

            assert "Error generating random query with OpenAI" in str(exc_info.value)

    def test_anthropic_error_handling(self, single_table_schema):
        """Test error handling when Anthropic API call fails"""
        with patch('core.llm_processor.os.environ.get') as mock_env, \
             patch('core.llm_processor.Anthropic') as mock_anthropic_class:

            # Setup mocks to raise exception
            mock_env.return_value = "test-api-key"
            mock_client = MagicMock()
            mock_client.messages.create.side_effect = Exception("API Error")
            mock_anthropic_class.return_value = mock_client

            # Should raise exception with descriptive message
            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_anthropic(single_table_schema)

            assert "Error generating random query with Anthropic" in str(exc_info.value)

    def test_openai_missing_api_key(self, single_table_schema):
        """Test that OpenAI function raises error when API key is missing"""
        with patch('core.llm_processor.os.environ.get') as mock_env:
            # No API key
            mock_env.return_value = None

            # Should raise Exception
            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_openai(single_table_schema)

            assert "OPENAI_API_KEY environment variable not set" in str(exc_info.value)

    def test_anthropic_missing_api_key(self, single_table_schema):
        """Test that Anthropic function raises error when API key is missing"""
        with patch('core.llm_processor.os.environ.get') as mock_env:
            # No API key
            mock_env.return_value = None

            # Should raise Exception
            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_anthropic(single_table_schema)

            assert "ANTHROPIC_API_KEY environment variable not set" in str(exc_info.value)

    def test_multiple_tables_schema(self, multiple_tables_schema, mock_openai_response):
        """Test query generation with multiple tables (for join opportunities)"""
        with patch('core.llm_processor.os.environ.get') as mock_env, \
             patch('core.llm_processor.OpenAI') as mock_openai_class:

            # Setup mocks
            mock_env.return_value = "test-api-key"
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_openai_response
            mock_openai_class.return_value = mock_client

            # Generate query
            query = generate_random_query_with_openai(multiple_tables_schema)

            # Assertions - verify function was called with multiple tables in schema
            assert query is not None
            call_args = mock_client.chat.completions.create.call_args
            prompt = call_args.kwargs['messages'][1]['content']
            assert "users" in prompt
            assert "orders" in prompt
