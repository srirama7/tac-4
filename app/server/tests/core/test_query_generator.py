import pytest
import os
from unittest.mock import patch, MagicMock
from core.llm_processor import (
    generate_random_nl_query_with_openai,
    generate_random_nl_query_with_anthropic,
    generate_random_nl_query
)


class TestQueryGenerator:

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_with_single_table(self, mock_openai_class):
        """Test query generation with a single table"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Show me the top 10 users by age"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'age': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            result = generate_random_nl_query_with_openai(schema_info)

            assert result == "Show me the top 10 users by age"
            mock_client.chat.completions.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == 'gpt-4o-mini'
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['max_tokens'] == 150

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_with_multiple_tables(self, mock_openai_class):
        """Test query generation with multiple tables"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "What is the average price of products by category?"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL', 'category_id': 'INTEGER'},
                        'row_count': 50
                    },
                    'categories': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 10
                    }
                }
            }

            result = generate_random_nl_query_with_openai(schema_info)

            assert result == "What is the average price of products by category?"
            mock_client.chat.completions.create.assert_called_once()

    def test_generate_query_no_tables(self):
        """Test error handling when no tables exist"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {}}

            with pytest.raises(ValueError) as exc_info:
                generate_random_nl_query(schema_info)

            assert "No tables found in database" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_removes_quotes(self, mock_openai_class):
        """Test that wrapping quotes are removed from the generated query"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Test with double quotes
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '"Show me all users"'
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 100
                    }
                }
            }

            result = generate_random_nl_query_with_openai(schema_info)
            assert result == "Show me all users"

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_uses_actual_schema(self, mock_openai_class):
        """Test that the prompt includes actual schema information"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Show me orders from the last week"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'orders': {
                        'columns': {'id': 'INTEGER', 'user_id': 'INTEGER', 'total': 'REAL', 'created_at': 'TEXT'},
                        'row_count': 200
                    }
                }
            }

            generate_random_nl_query_with_openai(schema_info)

            # Verify that the prompt includes schema information
            call_args = mock_client.chat.completions.create.call_args
            prompt = call_args[1]['messages'][1]['content']
            assert 'orders' in prompt
            assert 'id' in prompt
            assert 'user_id' in prompt
            assert 'total' in prompt
            assert 'created_at' in prompt
            assert 'Row count: 200' in prompt

    @patch('core.llm_processor.Anthropic')
    def test_generate_query_with_anthropic(self, mock_anthropic_class):
        """Test query generation with Anthropic API"""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "How many products are in each category?"
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'category': 'TEXT'},
                        'row_count': 75
                    }
                }
            }

            result = generate_random_nl_query_with_anthropic(schema_info)

            assert result == "How many products are in each category?"
            mock_client.messages.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.messages.create.call_args
            assert call_args[1]['model'] == 'claude-3-haiku-20240307'
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['max_tokens'] == 150

    def test_generate_query_with_anthropic_no_api_key(self):
        """Test error when Anthropic API key is not set"""
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            with pytest.raises(Exception) as exc_info:
                generate_random_nl_query_with_anthropic(schema_info)

            assert "ANTHROPIC_API_KEY environment variable not set" in str(exc_info.value)

    def test_generate_query_with_openai_no_api_key(self):
        """Test error when OpenAI API key is not set"""
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            with pytest.raises(Exception) as exc_info:
                generate_random_nl_query_with_openai(schema_info)

            assert "OPENAI_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.llm_processor.generate_random_nl_query_with_openai')
    def test_generate_query_openai_priority(self, mock_openai_func):
        """Test that OpenAI is used when OpenAI key exists"""
        mock_openai_func.return_value = "Show me all users"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'openai-key', 'ANTHROPIC_API_KEY': 'anthropic-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            result = generate_random_nl_query(schema_info)

            assert result == "Show me all users"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_random_nl_query_with_anthropic')
    def test_generate_query_anthropic_fallback(self, mock_anthropic_func):
        """Test that Anthropic is used when only Anthropic key exists"""
        mock_anthropic_func.return_value = "Show me all products"

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'anthropic-key'}, clear=True):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER'},
                        'row_count': 50
                    }
                }
            }

            result = generate_random_nl_query(schema_info)

            assert result == "Show me all products"
            mock_anthropic_func.assert_called_once_with(schema_info)

    def test_generate_query_no_api_keys(self):
        """Test error when no API keys are available"""
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            with pytest.raises(ValueError) as exc_info:
                generate_random_nl_query(schema_info)

            assert "No LLM API keys found" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_api_error(self, mock_openai_class):
        """Test error handling when API call fails"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            with pytest.raises(Exception) as exc_info:
                generate_random_nl_query_with_openai(schema_info)

            assert "Error generating query with OpenAI" in str(exc_info.value)
