import os
import logging
from typing import Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)


def generate_with_gemini(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1024
) -> str:
    """
    Generate text using Google Gemini API.

    Args:
        prompt: The prompt to send to Gemini
        temperature: Controls randomness (0.0-1.0), higher = more creative
        max_tokens: Maximum tokens in response

    Returns:
        Generated text from Gemini

    Raises:
        ValueError: If GEMINI_API_KEY is not set or Gemini SDK is not installed
        Exception: If API call fails
    """
    if genai is None:
        raise ValueError(
            "google-generativeai is not installed. "
            "Install it with: pip install google-generativeai"
        )

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)

        # Use Gemini 2.5 Flash model (latest and fastest)
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Generate content
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        )

        # Extract text and clean up
        text = response.text.strip()

        # Remove markdown code blocks if present
        if text.startswith("```"):
            # Remove opening markdown block
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            # Remove closing markdown block
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()

        logger.info("Successfully generated content with Gemini")
        return text

    except Exception as e:
        logger.error(f"Error generating content with Gemini: {str(e)}")
        raise Exception(f"Error generating content with Gemini: {str(e)}")
