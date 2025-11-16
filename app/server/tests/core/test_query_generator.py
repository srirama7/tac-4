import pytest
import os
from unittest.mock import patch, MagicMock
from core.query_generator import (
    generate_query_suggestion_with_openai,
    generate_query_suggestion_with_anthropic,
    format_schema_for_suggestion_prompt,
    generate_query_suggestion
)


class TestQueryGenerator:

    @patch('core.query_generator.OpenAI')
    def test_generate_query_suggestion_with_openai_success(self, mock_openai_class):
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "What are the most common names in the user database?"
        mock_client.chat.completions.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'age': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            result = generate_query_suggestion_with_openai(schema_info)

            assert result == "What are the most common names in the user database?"
            mock_client.chat.completions.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == 'gpt-4.1-mini'
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['max_tokens'] == 150

    @patch('core.query_generator.OpenAI')
    def test_generate_query_suggestion_with_openai_removes_quotes(self, mock_openai_class):
        # Test quote removal
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = '"Show me all users"'
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {'users': {'columns': {}, 'row_count': 10}}}

            result = generate_query_suggestion_with_openai(schema_info)

            assert result == "Show me all users"

    def test_generate_query_suggestion_with_openai_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_query_suggestion_with_openai(schema_info)

            assert "OPENAI_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.query_generator.OpenAI')
    def test_generate_query_suggestion_with_openai_api_error(self, mock_openai_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_query_suggestion_with_openai(schema_info)

            assert "Error generating query suggestion with OpenAI" in str(exc_info.value)

    @patch('core.query_generator.Anthropic')
    def test_generate_query_suggestion_with_anthropic_success(self, mock_anthropic_class):
        # Mock Anthropic client and response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "Which products have the highest prices?"
        mock_client.messages.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                        'row_count': 50
                    }
                }
            }

            result = generate_query_suggestion_with_anthropic(schema_info)

            assert result == "Which products have the highest prices?"
            mock_client.messages.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.messages.create.call_args
            assert call_args[1]['model'] == 'claude-3-haiku-20240307'
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['max_tokens'] == 150

    @patch('core.query_generator.Anthropic')
    def test_generate_query_suggestion_with_anthropic_removes_quotes(self, mock_anthropic_class):
        # Test quote removal
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "'Show me all orders'"
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {'tables': {'orders': {'columns': {}, 'row_count': 10}}}

            result = generate_query_suggestion_with_anthropic(schema_info)

            assert result == "Show me all orders"

    def test_generate_query_suggestion_with_anthropic_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_query_suggestion_with_anthropic(schema_info)

            assert "ANTHROPIC_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.query_generator.Anthropic')
    def test_generate_query_suggestion_with_anthropic_api_error(self, mock_anthropic_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_query_suggestion_with_anthropic(schema_info)

            assert "Error generating query suggestion with Anthropic" in str(exc_info.value)

    def test_format_schema_for_suggestion_prompt(self):
        # Test schema formatting for query suggestion prompt
        schema_info = {
            'tables': {
                'users': {
                    'columns': {'id': 'INTEGER', 'name': 'TEXT', 'age': 'INTEGER'},
                    'row_count': 100
                },
                'products': {
                    'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                    'row_count': 50
                }
            }
        }

        result = format_schema_for_suggestion_prompt(schema_info)

        assert "Table: users" in result
        assert "Table: products" in result
        assert "- id (INTEGER)" in result
        assert "- name (TEXT)" in result
        assert "- age (INTEGER)" in result
        assert "- price (REAL)" in result
        assert "Row count: 100" in result
        assert "Row count: 50" in result

    def test_format_schema_for_suggestion_prompt_empty(self):
        # Test with empty schema
        schema_info = {'tables': {}}

        result = format_schema_for_suggestion_prompt(schema_info)

        assert result == "No tables available"

    def test_generate_query_suggestion_empty_schema(self):
        # Test error when schema is empty
        schema_info = {'tables': {}}

        with pytest.raises(ValueError) as exc_info:
            generate_query_suggestion(schema_info)

        assert "Database is empty" in str(exc_info.value)

    def test_generate_query_suggestion_no_api_keys(self):
        # Test error when no API keys are configured
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 10
                    }
                }
            }

            with pytest.raises(ValueError) as exc_info:
                generate_query_suggestion(schema_info)

            assert "No LLM API keys configured" in str(exc_info.value)

    @patch('core.query_generator.generate_query_suggestion_with_openai')
    def test_generate_query_suggestion_openai_key_priority(self, mock_openai_func):
        # Test that OpenAI is used when OpenAI key exists
        mock_openai_func.return_value = "What are the most popular products?"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'openai-key', 'ANTHROPIC_API_KEY': 'anthropic-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 50
                    }
                }
            }

            result = generate_query_suggestion(schema_info, llm_provider="anthropic")

            assert result == "What are the most popular products?"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.query_generator.generate_query_suggestion_with_anthropic')
    def test_generate_query_suggestion_anthropic_fallback(self, mock_anthropic_func):
        # Test that Anthropic is used when only Anthropic key exists
        mock_anthropic_func.return_value = "Show me recent orders"

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'anthropic-key'}, clear=True):
            schema_info = {
                'tables': {
                    'orders': {
                        'columns': {'id': 'INTEGER', 'date': 'TEXT'},
                        'row_count': 100
                    }
                }
            }

            result = generate_query_suggestion(schema_info, llm_provider="openai")

            assert result == "Show me recent orders"
            mock_anthropic_func.assert_called_once_with(schema_info)

    @patch('core.query_generator.generate_query_suggestion_with_openai')
    def test_generate_query_suggestion_single_table(self, mock_openai_func):
        # Test with single table schema
        mock_openai_func.return_value = "What is the average age of users?"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'age': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            result = generate_query_suggestion(schema_info)

            assert result == "What is the average age of users?"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.query_generator.generate_query_suggestion_with_openai')
    def test_generate_query_suggestion_multiple_tables(self, mock_openai_func):
        # Test with multiple tables schema
        mock_openai_func.return_value = "Show me users who have placed orders in the last month"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'email': 'TEXT'},
                        'row_count': 100
                    },
                    'orders': {
                        'columns': {'id': 'INTEGER', 'user_id': 'INTEGER', 'date': 'TEXT', 'total': 'REAL'},
                        'row_count': 500
                    }
                }
            }

            result = generate_query_suggestion(schema_info)

            assert result == "Show me users who have placed orders in the last month"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.query_generator.generate_query_suggestion_with_openai')
    def test_generate_query_suggestion_only_openai_key(self, mock_openai_func):
        # Test when only OpenAI key exists
        mock_openai_func.return_value = "Which products have low inventory?"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'openai-key'}, clear=True):
            schema_info = {
                'tables': {
                    'inventory': {
                        'columns': {'product_id': 'INTEGER', 'quantity': 'INTEGER'},
                        'row_count': 200
                    }
                }
            }

            result = generate_query_suggestion(schema_info, llm_provider="anthropic")

            assert result == "Which products have low inventory?"
            mock_openai_func.assert_called_once_with(schema_info)
