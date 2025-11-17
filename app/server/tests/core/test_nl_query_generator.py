import pytest
import os
from unittest.mock import patch, MagicMock
from core.llm_processor import (
    generate_natural_language_query_with_openai,
    generate_natural_language_query_with_anthropic,
    generate_natural_language_query
)


class TestNLQueryGenerator:

    @patch('core.llm_processor.OpenAI')
    def test_generate_nl_query_with_openai_success(self, mock_openai_class):
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "What are the most popular products by sales count?"
        mock_client.chat.completions.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                        'row_count': 100
                    }
                }
            }

            result = generate_natural_language_query_with_openai(schema_info)

            assert result == "What are the most popular products by sales count?"
            mock_client.chat.completions.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == 'gpt-4.1-mini'
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.OpenAI')
    def test_generate_nl_query_with_openai_remove_quotes(self, mock_openai_class):
        # Test quote removal
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = '"How many users are active?"'
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {}}

            result = generate_natural_language_query_with_openai(schema_info)

            assert result == "How many users are active?"

    def test_generate_nl_query_with_openai_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query_with_openai(schema_info)

            assert "OPENAI_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    def test_generate_nl_query_with_openai_api_error(self, mock_openai_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query_with_openai(schema_info)

            assert "Error generating natural language query with OpenAI" in str(exc_info.value)

    @patch('core.llm_processor.Anthropic')
    def test_generate_nl_query_with_anthropic_success(self, mock_anthropic_class):
        # Mock Anthropic client and response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "Which customers have spent the most in the last month?"
        mock_client.messages.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'customers': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'total_spent': 'REAL'},
                        'row_count': 50
                    }
                }
            }

            result = generate_natural_language_query_with_anthropic(schema_info)

            assert result == "Which customers have spent the most in the last month?"
            mock_client.messages.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.messages.create.call_args
            assert call_args[1]['model'] == 'claude-3-haiku-20240307'
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.Anthropic')
    def test_generate_nl_query_with_anthropic_remove_quotes(self, mock_anthropic_class):
        # Test quote removal
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "'What is the average order value?'"
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {'tables': {}}

            result = generate_natural_language_query_with_anthropic(schema_info)

            assert result == "What is the average order value?"

    def test_generate_nl_query_with_anthropic_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query_with_anthropic(schema_info)

            assert "ANTHROPIC_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.llm_processor.Anthropic')
    def test_generate_nl_query_with_anthropic_api_error(self, mock_anthropic_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query_with_anthropic(schema_info)

            assert "Error generating natural language query with Anthropic" in str(exc_info.value)

    @patch('core.llm_processor.generate_natural_language_query_with_openai')
    def test_generate_nl_query_openai_key_priority(self, mock_openai_func):
        # Test that OpenAI is used when OpenAI key exists
        mock_openai_func.return_value = "What are the top selling items?"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'openai-key', 'ANTHROPIC_API_KEY': 'anthropic-key'}):
            schema_info = {'tables': {}}

            result = generate_natural_language_query(schema_info, llm_provider="anthropic")

            assert result == "What are the top selling items?"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_natural_language_query_with_anthropic')
    def test_generate_nl_query_anthropic_fallback(self, mock_anthropic_func):
        # Test that Anthropic is used when only Anthropic key exists
        mock_anthropic_func.return_value = "How many orders were placed this week?"

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'anthropic-key'}, clear=True):
            schema_info = {'tables': {}}

            result = generate_natural_language_query(schema_info, llm_provider="openai")

            assert result == "How many orders were placed this week?"
            mock_anthropic_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_natural_language_query_with_openai')
    def test_generate_nl_query_request_preference_openai(self, mock_openai_func):
        # Test request preference when no keys available
        mock_openai_func.return_value = "What is the average customer age?"

        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            result = generate_natural_language_query(schema_info, llm_provider="openai")

            assert result == "What is the average customer age?"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_natural_language_query_with_anthropic')
    def test_generate_nl_query_request_preference_anthropic(self, mock_anthropic_func):
        # Test request preference when no keys available
        mock_anthropic_func.return_value = "Which products have the highest profit margin?"

        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            result = generate_natural_language_query(schema_info, llm_provider="anthropic")

            assert result == "Which products have the highest profit margin?"
            mock_anthropic_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.OpenAI')
    def test_generate_nl_query_multiple_tables(self, mock_openai_class):
        # Test with multiple tables
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Which users have the most orders?"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 100
                    },
                    'orders': {
                        'columns': {'id': 'INTEGER', 'user_id': 'INTEGER', 'total': 'REAL'},
                        'row_count': 500
                    }
                }
            }

            result = generate_natural_language_query_with_openai(schema_info)

            assert result == "Which users have the most orders?"
