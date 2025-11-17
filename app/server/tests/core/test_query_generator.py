import pytest
import os
from unittest.mock import patch, MagicMock
from core.llm_processor import (
    generate_natural_language_query_with_openai,
    generate_natural_language_query_with_anthropic,
    generate_natural_language_query
)


class TestQueryGenerator:

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_with_openai_success(self, mock_openai_class):
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "What are the top 5 products by sales?"
        mock_client.chat.completions.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'sales': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            result = generate_natural_language_query_with_openai(schema_info)

            assert result == "What are the top 5 products by sales?"
            mock_client.chat.completions.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == 'gpt-4.1-mini'
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_with_openai_truncate_long_query(self, mock_openai_class):
        # Test that queries longer than 2 sentences are truncated
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "First sentence. Second sentence. Third sentence. Fourth sentence."
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 50
                    }
                }
            }

            result = generate_natural_language_query_with_openai(schema_info)

            # Should only have 2 sentences
            assert result == "First sentence. Second sentence."

    def test_generate_query_with_openai_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {'users': {'columns': {}, 'row_count': 0}}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query_with_openai(schema_info)

            assert "OPENAI_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_with_openai_api_error(self, mock_openai_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {'users': {'columns': {}, 'row_count': 0}}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query_with_openai(schema_info)

            assert "Error generating natural language query with OpenAI" in str(exc_info.value)

    @patch('core.llm_processor.Anthropic')
    def test_generate_query_with_anthropic_success(self, mock_anthropic_class):
        # Mock Anthropic client and response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "Show me all orders from the last week."
        mock_client.messages.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'orders': {
                        'columns': {'id': 'INTEGER', 'date': 'TEXT', 'amount': 'REAL'},
                        'row_count': 200
                    }
                }
            }

            result = generate_natural_language_query_with_anthropic(schema_info)

            assert result == "Show me all orders from the last week."
            mock_client.messages.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.messages.create.call_args
            assert call_args[1]['model'] == 'claude-3-haiku-20240307'
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.Anthropic')
    def test_generate_query_with_anthropic_truncate_long_query(self, mock_anthropic_class):
        # Test that queries longer than 2 sentences are truncated
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "Sentence one. Sentence two. Sentence three."
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 30
                    }
                }
            }

            result = generate_natural_language_query_with_anthropic(schema_info)

            # Should only have 2 sentences
            assert result == "Sentence one. Sentence two."

    def test_generate_query_with_anthropic_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {'orders': {'columns': {}, 'row_count': 0}}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query_with_anthropic(schema_info)

            assert "ANTHROPIC_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.llm_processor.Anthropic')
    def test_generate_query_with_anthropic_api_error(self, mock_anthropic_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {'tables': {'orders': {'columns': {}, 'row_count': 0}}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query_with_anthropic(schema_info)

            assert "Error generating natural language query with Anthropic" in str(exc_info.value)

    def test_generate_query_no_tables(self):
        # Test error when no tables exist
        schema_info = {'tables': {}}

        with pytest.raises(ValueError) as exc_info:
            generate_natural_language_query(schema_info)

        assert "No tables available in database" in str(exc_info.value)

    def test_generate_query_empty_tables(self):
        # Test error when tables dict is empty
        schema_info = {}

        with pytest.raises(ValueError) as exc_info:
            generate_natural_language_query(schema_info)

        assert "No tables available in database" in str(exc_info.value)

    @patch('core.llm_processor.generate_natural_language_query_with_openai')
    def test_generate_query_openai_priority(self, mock_openai_func):
        # Test that OpenAI is used when OpenAI key exists
        mock_openai_func.return_value = "How many users signed up today?"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'openai-key', 'ANTHROPIC_API_KEY': 'anthropic-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'signup_date': 'TEXT'},
                        'row_count': 150
                    }
                }
            }

            result = generate_natural_language_query(schema_info)

            assert result == "How many users signed up today?"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_natural_language_query_with_anthropic')
    def test_generate_query_anthropic_fallback(self, mock_anthropic_func):
        # Test that Anthropic is used when only Anthropic key exists
        mock_anthropic_func.return_value = "What is the average order value?"

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'anthropic-key'}, clear=True):
            schema_info = {
                'tables': {
                    'orders': {
                        'columns': {'id': 'INTEGER', 'amount': 'REAL'},
                        'row_count': 80
                    }
                }
            }

            result = generate_natural_language_query(schema_info)

            assert result == "What is the average order value?"
            mock_anthropic_func.assert_called_once_with(schema_info)

    def test_generate_query_no_api_keys(self):
        # Test error when no API keys are configured
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 50
                    }
                }
            }

            with pytest.raises(ValueError) as exc_info:
                generate_natural_language_query(schema_info)

            assert "No LLM API keys configured" in str(exc_info.value)

    @patch('core.llm_processor.generate_natural_language_query_with_openai')
    def test_generate_query_multiple_tables(self, mock_openai_func):
        # Test with multiple tables to ensure schema is passed correctly
        mock_openai_func.return_value = "Which products have been ordered most frequently?"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                        'row_count': 100
                    },
                    'orders': {
                        'columns': {'id': 'INTEGER', 'product_id': 'INTEGER', 'quantity': 'INTEGER'},
                        'row_count': 500
                    }
                }
            }

            result = generate_natural_language_query(schema_info)

            assert result == "Which products have been ordered most frequently?"
            mock_openai_func.assert_called_once_with(schema_info)

            # Verify the schema passed includes both tables
            call_args = mock_openai_func.call_args[0][0]
            assert 'products' in call_args['tables']
            assert 'orders' in call_args['tables']
