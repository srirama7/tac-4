import pytest
import os
from unittest.mock import patch, MagicMock
from core.llm_processor import generate_natural_language_query


class TestQueryGenerator:

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_with_openai_success(self, mock_openai_class):
        """Test successful query generation with OpenAI"""
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Show me users who signed up in the last month"
        mock_client.chat.completions.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'signup_date': 'TEXT'},
                        'row_count': 100
                    }
                }
            }

            result = generate_natural_language_query(schema_info)

            assert result == "Show me users who signed up in the last month"
            mock_client.chat.completions.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == 'gpt-4.1-mini'
            assert call_args[1]['temperature'] == 0.7  # Higher temperature for creativity
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.Anthropic')
    def test_generate_query_with_anthropic_success(self, mock_anthropic_class):
        """Test successful query generation with Anthropic"""
        # Mock Anthropic client and response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "What are the top 5 most expensive products?"
        mock_client.messages.create.return_value = mock_response

        # Mock environment variable (only Anthropic key available)
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}, clear=True):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                        'row_count': 50
                    }
                }
            }

            result = generate_natural_language_query(schema_info)

            assert result == "What are the top 5 most expensive products?"
            mock_client.messages.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.messages.create.call_args
            assert call_args[1]['model'] == 'claude-3-haiku-20240307'
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_clean_quotes(self, mock_openai_class):
        """Test that quotes are stripped from generated queries"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = '"Show me all active users"'
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {'users': {'columns': {'id': 'INTEGER'}, 'row_count': 10}}}

            result = generate_natural_language_query(schema_info)

            assert result == "Show me all active users"
            assert not result.startswith('"')
            assert not result.endswith('"')

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_clean_markdown(self, mock_openai_class):
        """Test that markdown formatting is cleaned up"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "```\nCount events by type\n```"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {'events': {'columns': {'type': 'TEXT'}, 'row_count': 20}}}

            result = generate_natural_language_query(schema_info)

            assert "```" not in result
            assert "Count events by type" in result

    def test_generate_query_no_api_keys(self):
        """Test error when no API keys are configured"""
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {'users': {'columns': {'id': 'INTEGER'}, 'row_count': 10}}}

            with pytest.raises(ValueError) as exc_info:
                generate_natural_language_query(schema_info)

            assert "No LLM API key configured" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_openai_priority(self, mock_openai_class):
        """Test that OpenAI is used when both API keys are available"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Show me recent orders"
        mock_client.chat.completions.create.return_value = mock_response

        # Both keys available - should use OpenAI
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'openai-key', 'ANTHROPIC_API_KEY': 'anthropic-key'}):
            schema_info = {'tables': {'orders': {'columns': {'id': 'INTEGER'}, 'row_count': 30}}}

            result = generate_natural_language_query(schema_info)

            assert result == "Show me recent orders"
            mock_client.chat.completions.create.assert_called_once()

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_openai_error(self, mock_openai_class):
        """Test error handling when OpenAI API fails"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {'users': {'columns': {'id': 'INTEGER'}, 'row_count': 10}}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query(schema_info)

            assert "Error generating query with OpenAI" in str(exc_info.value)

    @patch('core.llm_processor.Anthropic')
    def test_generate_query_anthropic_error(self, mock_anthropic_class):
        """Test error handling when Anthropic API fails"""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}, clear=True):
            schema_info = {'tables': {'products': {'columns': {'id': 'INTEGER'}, 'row_count': 20}}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query(schema_info)

            assert "Error generating query with Anthropic" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_multiple_tables(self, mock_openai_class):
        """Test query generation with multiple tables"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Show me users who have placed orders"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 100
                    },
                    'orders': {
                        'columns': {'id': 'INTEGER', 'user_id': 'INTEGER', 'amount': 'REAL'},
                        'row_count': 250
                    }
                }
            }

            result = generate_natural_language_query(schema_info)

            assert len(result) > 0
            mock_client.chat.completions.create.assert_called_once()

            # Verify schema was included in prompt
            call_args = mock_client.chat.completions.create.call_args
            prompt_text = call_args[1]['messages'][1]['content']
            assert 'users' in prompt_text
            assert 'orders' in prompt_text

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_single_table(self, mock_openai_class):
        """Test query generation with a single table"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Find products with prices above average"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL', 'category': 'TEXT'},
                        'row_count': 75
                    }
                }
            }

            result = generate_natural_language_query(schema_info)

            assert result == "Find products with prices above average"
            mock_client.chat.completions.create.assert_called_once()
