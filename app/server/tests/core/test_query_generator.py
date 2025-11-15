import pytest
from unittest.mock import patch, MagicMock
from core.llm_processor import generate_query_suggestion, generate_query_suggestion_with_openai, generate_query_suggestion_with_anthropic


@pytest.fixture
def sample_schema_multiple_tables():
    """Sample schema with multiple tables"""
    return {
        'tables': {
            'users': {
                'columns': {
                    'id': 'INTEGER',
                    'name': 'TEXT',
                    'email': 'TEXT',
                    'created_at': 'TEXT'
                },
                'row_count': 100
            },
            'products': {
                'columns': {
                    'id': 'INTEGER',
                    'name': 'TEXT',
                    'price': 'REAL',
                    'category': 'TEXT'
                },
                'row_count': 50
            }
        }
    }


@pytest.fixture
def sample_schema_single_table():
    """Sample schema with single table"""
    return {
        'tables': {
            'users': {
                'columns': {
                    'id': 'INTEGER',
                    'name': 'TEXT',
                    'email': 'TEXT'
                },
                'row_count': 25
            }
        }
    }


@pytest.fixture
def empty_schema():
    """Empty schema with no tables"""
    return {
        'tables': {}
    }


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "What are the top 5 most expensive products?"
    return mock_response


@pytest.fixture
def mock_anthropic_response():
    """Mock Anthropic API response"""
    mock_response = MagicMock()
    mock_response.content = [MagicMock()]
    mock_response.content[0].text = "Show me all users who created accounts in the last month."
    return mock_response


class TestQueryGenerationWithOpenAI:
    """Test query generation with OpenAI provider"""

    @patch('core.llm_processor.OpenAI')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_generate_query_with_multiple_tables(self, mock_openai_class, sample_schema_multiple_tables, mock_openai_response):
        """Test generating query with multiple tables"""
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client

        result = generate_query_suggestion_with_openai(sample_schema_multiple_tables)

        assert result == "What are the top 5 most expensive products?"
        assert isinstance(result, str)
        assert len(result) > 0
        mock_client.chat.completions.create.assert_called_once()

    @patch('core.llm_processor.OpenAI')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_generate_query_with_single_table(self, mock_openai_class, sample_schema_single_table, mock_openai_response):
        """Test generating query with single table"""
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client

        result = generate_query_suggestion_with_openai(sample_schema_single_table)

        assert isinstance(result, str)
        assert len(result) > 0

    @patch.dict('os.environ', {}, clear=True)
    def test_generate_query_missing_api_key(self, sample_schema_multiple_tables):
        """Test that missing API key raises appropriate error"""
        with pytest.raises(Exception) as exc_info:
            generate_query_suggestion_with_openai(sample_schema_multiple_tables)

        assert "OPENAI_API_KEY" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_generate_query_removes_quotes(self, mock_openai_class, sample_schema_multiple_tables):
        """Test that quotes are stripped from generated queries"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '"What are the top products?"'
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        result = generate_query_suggestion_with_openai(sample_schema_multiple_tables)

        assert result == "What are the top products?"
        assert not result.startswith('"')
        assert not result.endswith('"')


class TestQueryGenerationWithAnthropic:
    """Test query generation with Anthropic provider"""

    @patch('core.llm_processor.Anthropic')
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    def test_generate_query_with_multiple_tables(self, mock_anthropic_class, sample_schema_multiple_tables, mock_anthropic_response):
        """Test generating query with Anthropic API"""
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_anthropic_response
        mock_anthropic_class.return_value = mock_client

        result = generate_query_suggestion_with_anthropic(sample_schema_multiple_tables)

        assert result == "Show me all users who created accounts in the last month."
        assert isinstance(result, str)
        assert len(result) > 0
        mock_client.messages.create.assert_called_once()

    @patch.dict('os.environ', {}, clear=True)
    def test_generate_query_missing_api_key(self, sample_schema_multiple_tables):
        """Test that missing API key raises appropriate error"""
        with pytest.raises(Exception) as exc_info:
            generate_query_suggestion_with_anthropic(sample_schema_multiple_tables)

        assert "ANTHROPIC_API_KEY" in str(exc_info.value)


class TestQueryGenerationRouting:
    """Test LLM provider routing logic"""

    @patch('core.llm_processor.generate_query_suggestion_with_openai')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_routes_to_openai_when_key_exists(self, mock_openai_gen, sample_schema_multiple_tables):
        """Test that OpenAI is preferred when API key exists"""
        mock_openai_gen.return_value = "Test query"

        result = generate_query_suggestion(sample_schema_multiple_tables, "openai")

        mock_openai_gen.assert_called_once_with(sample_schema_multiple_tables)
        assert result == "Test query"

    @patch('core.llm_processor.generate_query_suggestion_with_anthropic')
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    def test_routes_to_anthropic_when_key_exists(self, mock_anthropic_gen, sample_schema_multiple_tables):
        """Test that Anthropic is used when only Anthropic key exists"""
        mock_anthropic_gen.return_value = "Test query"

        result = generate_query_suggestion(sample_schema_multiple_tables, "anthropic")

        mock_anthropic_gen.assert_called_once_with(sample_schema_multiple_tables)
        assert result == "Test query"

    @patch('core.llm_processor.generate_query_suggestion_with_openai')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'openai-key', 'ANTHROPIC_API_KEY': 'anthropic-key'})
    def test_prefers_openai_when_both_keys_exist(self, mock_openai_gen, sample_schema_multiple_tables):
        """Test that OpenAI is preferred when both API keys exist"""
        mock_openai_gen.return_value = "Test query"

        result = generate_query_suggestion(sample_schema_multiple_tables, "anthropic")

        # Should still call OpenAI despite requesting Anthropic, because OpenAI has priority
        mock_openai_gen.assert_called_once_with(sample_schema_multiple_tables)


class TestEdgeCases:
    """Test edge cases and error handling"""

    @patch('core.llm_processor.OpenAI')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_handles_api_error_gracefully(self, mock_openai_class, sample_schema_multiple_tables):
        """Test that API errors are handled gracefully"""
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai_class.return_value = mock_client

        with pytest.raises(Exception) as exc_info:
            generate_query_suggestion_with_openai(sample_schema_multiple_tables)

        assert "Error generating query suggestion" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_handles_empty_response(self, mock_openai_class, sample_schema_multiple_tables):
        """Test handling of empty response from LLM"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "   "  # Empty/whitespace
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        result = generate_query_suggestion_with_openai(sample_schema_multiple_tables)

        assert result == ""

    @patch('core.llm_processor.OpenAI')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_strips_various_quote_types(self, mock_openai_class, sample_schema_multiple_tables):
        """Test that various quote types are stripped"""
        mock_client = MagicMock()

        # Test double quotes
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '"Query with double quotes"'
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        result = generate_query_suggestion_with_openai(sample_schema_multiple_tables)
        assert result == "Query with double quotes"

        # Test single quotes
        mock_response.choices[0].message.content = "'Query with single quotes'"
        result = generate_query_suggestion_with_openai(sample_schema_multiple_tables)
        assert result == "Query with single quotes"

        # Test backticks
        mock_response.choices[0].message.content = "`Query with backticks`"
        result = generate_query_suggestion_with_openai(sample_schema_multiple_tables)
        assert result == "Query with backticks"
