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
        mock_response.choices[0].message.content = "What is the average age of users"
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

            result = generate_natural_language_query_with_openai(schema_info)

            # Verify question mark is added
            assert result == "What is the average age of users?"
            mock_client.chat.completions.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == 'gpt-4.1-mini'
            assert call_args[1]['temperature'] == 0.8
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_with_openai_question_mark_already_present(self, mock_openai_class):
        # Test when question mark is already in the response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "How many products cost more than $100?"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                        'row_count': 50
                    }
                }
            }

            result = generate_natural_language_query_with_openai(schema_info)

            assert result == "How many products cost more than $100?"

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_with_openai_two_sentence_limit(self, mock_openai_class):
        # Test that queries exceeding two sentences are truncated
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        # Three sentences
        mock_response.choices[0].message.content = "What is the total count? How many are active. What about inactive"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {'users': {'columns': {'id': 'INTEGER'}, 'row_count': 10}}}

            result = generate_natural_language_query_with_openai(schema_info)

            # Should keep only first two sentences
            assert result.count('. ') <= 1  # At most one period separator (two sentences)

    def test_generate_query_with_openai_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

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
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query_with_openai(schema_info)

            assert "Error generating query with OpenAI" in str(exc_info.value)

    @patch('core.llm_processor.Anthropic')
    def test_generate_query_with_anthropic_success(self, mock_anthropic_class):
        # Mock Anthropic client and response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "Which products have the highest sales"
        mock_client.messages.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'sales': 'INTEGER'},
                        'row_count': 50
                    }
                }
            }

            result = generate_natural_language_query_with_anthropic(schema_info)

            # Verify question mark is added
            assert result == "Which products have the highest sales?"
            mock_client.messages.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.messages.create.call_args
            assert call_args[1]['model'] == 'claude-3-haiku-20240307'
            assert call_args[1]['temperature'] == 0.8
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.Anthropic')
    def test_generate_query_with_anthropic_question_mark_already_present(self, mock_anthropic_class):
        # Test when question mark is already in the response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "How many orders were placed today?"
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {'tables': {'orders': {'columns': {'id': 'INTEGER'}, 'row_count': 10}}}

            result = generate_natural_language_query_with_anthropic(schema_info)

            assert result == "How many orders were placed today?"

    @patch('core.llm_processor.Anthropic')
    def test_generate_query_with_anthropic_two_sentence_limit(self, mock_anthropic_class):
        # Test that queries exceeding two sentences are truncated
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        # Three sentences
        mock_response.content[0].text = "What is the average price. How many items. What about categories"
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {'tables': {'products': {'columns': {'id': 'INTEGER'}, 'row_count': 10}}}

            result = generate_natural_language_query_with_anthropic(schema_info)

            # Should keep only first two sentences
            assert result.count('. ') <= 1  # At most one period separator (two sentences)

    def test_generate_query_with_anthropic_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

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
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_natural_language_query_with_anthropic(schema_info)

            assert "Error generating query with Anthropic" in str(exc_info.value)

    @patch('core.llm_processor.generate_natural_language_query_with_openai')
    def test_generate_query_openai_key_priority(self, mock_openai_func):
        # Test that OpenAI is used when OpenAI key exists (regardless of preference)
        mock_openai_func.return_value = "What are the top selling products?"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'openai-key', 'ANTHROPIC_API_KEY': 'anthropic-key'}):
            schema_info = {'tables': {}}

            result = generate_natural_language_query("anthropic", schema_info)

            assert result == "What are the top selling products?"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_natural_language_query_with_anthropic')
    def test_generate_query_anthropic_fallback(self, mock_anthropic_func):
        # Test that Anthropic is used when only Anthropic key exists
        mock_anthropic_func.return_value = "How many active users are there?"

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'anthropic-key'}, clear=True):
            schema_info = {'tables': {}}

            result = generate_natural_language_query("openai", schema_info)

            assert result == "How many active users are there?"
            mock_anthropic_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_natural_language_query_with_openai')
    def test_generate_query_provider_preference_openai(self, mock_openai_func):
        # Test provider preference when no keys available
        mock_openai_func.return_value = "What is the total revenue?"

        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            result = generate_natural_language_query("openai", schema_info)

            assert result == "What is the total revenue?"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_natural_language_query_with_anthropic')
    def test_generate_query_provider_preference_anthropic(self, mock_anthropic_func):
        # Test provider preference when no keys available
        mock_anthropic_func.return_value = "Which category has the most items?"

        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            result = generate_natural_language_query("anthropic", schema_info)

            assert result == "Which category has the most items?"
            mock_anthropic_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_single_table(self, mock_openai_class):
        # Test query generation with single table
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "What is the average price in the products table?"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                        'row_count': 50
                    }
                }
            }

            result = generate_natural_language_query_with_openai(schema_info)

            assert "?" in result
            assert isinstance(result, str)
            assert len(result) > 0

    @patch('core.llm_processor.OpenAI')
    def test_generate_query_multiple_tables(self, mock_openai_class):
        # Test query generation with multiple tables
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "How many users have placed orders?"
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
                        'row_count': 250
                    }
                }
            }

            result = generate_natural_language_query_with_openai(schema_info)

            assert "?" in result
            assert isinstance(result, str)
            assert len(result) > 0
