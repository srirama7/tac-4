import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.llm_processor import generate_random_sql_description
from core.data_models import RandomSQLResponse
from core.gemini_processor import generate_with_gemini


class TestRandomSQLGeneration:
    """Tests for random SQL description generation"""

    @pytest.fixture
    def sample_schema(self):
        """Sample database schema for testing"""
        return {
            'tables': {
                'users': {
                    'columns': {
                        'id': 'INTEGER',
                        'name': 'TEXT',
                        'email': 'TEXT',
                        'signup_date': 'DATE'
                    },
                    'row_count': 100
                },
                'orders': {
                    'columns': {
                        'id': 'INTEGER',
                        'user_id': 'INTEGER',
                        'total_amount': 'DECIMAL',
                        'created_at': 'TIMESTAMP'
                    },
                    'row_count': 250
                }
            }
        }

    @pytest.fixture
    def single_table_schema(self):
        """Single table schema for testing"""
        return {
            'tables': {
                'products': {
                    'columns': {
                        'id': 'INTEGER',
                        'name': 'TEXT',
                        'price': 'DECIMAL',
                        'inventory': 'INTEGER'
                    },
                    'row_count': 500
                }
            }
        }

    @pytest.fixture
    def empty_schema(self):
        """Empty schema with no tables"""
        return {'tables': {}}

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('core.gemini_processor.genai')
    def test_generate_with_gemini_success(self, mock_genai):
        """Test successful Gemini API call"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.text = "Show me all users who signed up last week"

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        result = generate_with_gemini("Test prompt")

        assert result == "Show me all users who signed up last week"
        mock_genai.configure.assert_called_once_with(api_key='test-key')
        mock_genai.GenerativeModel.assert_called_once_with('gemini-2.5-flash')

    @patch.dict(os.environ, {}, clear=True)
    def test_generate_with_gemini_missing_api_key(self):
        """Test Gemini API generation fails without API key"""
        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable not set"):
            generate_with_gemini("Test prompt")

    @patch('core.gemini_processor.genai', None)
    def test_generate_with_gemini_sdk_not_installed(self):
        """Test Gemini generation fails without SDK"""
        with pytest.raises(ValueError, match="google-generativeai is not installed"):
            generate_with_gemini("Test prompt")

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('core.gemini_processor.genai')
    def test_generate_with_gemini_markdown_cleanup(self, mock_genai):
        """Test Gemini response cleanup removes markdown"""
        # Mock response with markdown code blocks
        mock_response = MagicMock()
        mock_response.text = """```
Show me users from last week
```"""

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        result = generate_with_gemini("Test prompt")

        # Should have markdown removed
        assert result == "Show me users from last week"
        assert not result.startswith("```")
        assert not result.endswith("```")

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('core.llm_processor.generate_with_gemini')
    def test_generate_random_sql_description_success(self, mock_generate, sample_schema):
        """Test successful random SQL description generation"""
        mock_generate.return_value = "Show me all users who signed up in the last 30 days"

        result = generate_random_sql_description(sample_schema)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "users" in result.lower() or "Show me" in result
        mock_generate.assert_called_once()

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('core.llm_processor.generate_with_gemini')
    def test_generate_random_sql_description_not_empty(self, mock_generate, sample_schema):
        """Test that generated descriptions are not empty"""
        mock_generate.return_value = "Sample description"

        result = generate_random_sql_description(sample_schema)

        assert len(result.strip()) > 0
        assert result != ""

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('core.llm_processor.generate_with_gemini')
    def test_generate_random_sql_description_reasonable_length(self, mock_generate, sample_schema):
        """Test that generated descriptions have reasonable length"""
        mock_description = "Show me users signed up in the last week and their total orders."
        mock_generate.return_value = mock_description

        result = generate_random_sql_description(sample_schema)

        # Description should be 1-3 sentences (reasonable length)
        sentence_count = result.count('.') + result.count('?')
        assert 1 <= sentence_count <= 3
        assert len(result) < 500  # Reasonable max length

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('core.llm_processor.generate_with_gemini')
    def test_generate_random_sql_with_single_table(self, mock_generate, single_table_schema):
        """Test generation with single table"""
        mock_generate.return_value = "Show me the top 10 most expensive products"

        result = generate_random_sql_description(single_table_schema)

        assert isinstance(result, str)
        assert len(result) > 0
        mock_generate.assert_called_once()

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('core.llm_processor.generate_with_gemini')
    def test_generate_random_sql_description_api_error(self, mock_generate, sample_schema):
        """Test error handling when Gemini API fails"""
        mock_generate.side_effect = Exception("API connection failed")

        with pytest.raises(Exception, match="Error generating random SQL description"):
            generate_random_sql_description(sample_schema)

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('core.llm_processor.generate_with_gemini')
    def test_generate_random_sql_description_empty_response(self, mock_generate, sample_schema):
        """Test handling of empty responses from LLM"""
        mock_generate.return_value = "   "  # Only whitespace

        with pytest.raises(Exception, match="Generated description is empty"):
            generate_random_sql_description(sample_schema)

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('core.llm_processor.generate_with_gemini')
    def test_generate_random_sql_uses_temperature_08(self, mock_generate, sample_schema):
        """Test that generation uses temperature 0.8 for randomness"""
        mock_generate.return_value = "Show me random data"

        result = generate_random_sql_description(sample_schema)

        # Check that generate_with_gemini was called with temperature=0.8
        call_kwargs = mock_generate.call_args.kwargs
        assert call_kwargs['temperature'] == 0.8

    def test_random_sql_response_model(self):
        """Test RandomSQLResponse model"""
        response = RandomSQLResponse(
            description="Show me all users",
            tables_analyzed=['users', 'orders']
        )

        assert response.description == "Show me all users"
        assert response.tables_analyzed == ['users', 'orders']
        assert response.error is None

    def test_random_sql_response_model_with_error(self):
        """Test RandomSQLResponse model with error"""
        response = RandomSQLResponse(
            description="",
            tables_analyzed=[],
            error="No tables found"
        )

        assert response.description == ""
        assert response.tables_analyzed == []
        assert response.error == "No tables found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
