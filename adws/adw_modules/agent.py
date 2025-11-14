"""Gemini AI agent module for executing prompts programmatically."""

import sys
import os
import json
import re
from typing import Optional, List, Dict, Any, Tuple
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai not installed. Install with: pip install google-generativeai")
    sys.exit(1)

from .data_types import (
    AgentPromptRequest,
    AgentPromptResponse,
    AgentTemplateRequest,
    ClaudeCodeResultMessage,
)

# Load environment variables
load_dotenv()

# Get Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set")
    sys.exit(1)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


def check_gemini_available() -> Optional[str]:
    """Check if Gemini API is configured. Return error message if not."""
    try:
        if not GEMINI_API_KEY:
            return "Error: GEMINI_API_KEY environment variable not set"
        # Try to list models to verify API key works
        models = genai.list_models()
        return None
    except Exception as e:
        return f"Error: Failed to connect to Gemini API: {str(e)}"


def parse_jsonl_output(
    output_file: str,
) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Parse JSONL output file and return all messages and the result message.

    Returns:
        Tuple of (all_messages, result_message) where result_message is None if not found
    """
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            # Read all lines and parse each as JSON
            messages = [json.loads(line) for line in f if line.strip()]

            # Find the result message (should be the last one)
            result_message = None
            for message in reversed(messages):
                if message.get("type") == "result":
                    result_message = message
                    break

            return messages, result_message
    except Exception as e:
        print(f"Error parsing JSONL file: {e}", file=sys.stderr)
        return [], None


def convert_jsonl_to_json(jsonl_file: str) -> str:
    """Convert JSONL file to JSON array file.

    Creates a .json file with the same name as the .jsonl file,
    containing all messages as a JSON array.

    Returns:
        Path to the created JSON file
    """
    # Create JSON filename by replacing .jsonl with .json
    json_file = jsonl_file.replace(".jsonl", ".json")

    # Parse the JSONL file
    messages, _ = parse_jsonl_output(jsonl_file)

    # Write as JSON array with UTF-8 encoding
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    print(f"Created JSON file: {json_file}")
    return json_file




def save_prompt(prompt: str, adw_id: str, agent_name: str = "ops") -> None:
    """Save a prompt to the appropriate logging directory."""
    # Extract slash command from prompt
    match = re.match(r"^(/\w+)", prompt)
    if not match:
        return

    slash_command = match.group(1)
    # Remove leading slash for filename
    command_name = slash_command[1:]

    # Create directory structure at project root (parent of adws)
    # __file__ is in adws/adw_modules/, so we need to go up 3 levels to get to project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    prompt_dir = os.path.join(project_root, "agents", adw_id, agent_name, "prompts")
    os.makedirs(prompt_dir, exist_ok=True)

    # Save prompt to file
    prompt_file = os.path.join(prompt_dir, f"{command_name}.txt")
    with open(prompt_file, "w") as f:
        f.write(prompt)

    print(f"Saved prompt to: {prompt_file}")


def prompt_gemini(request: AgentPromptRequest) -> AgentPromptResponse:
    """Execute Gemini API with the given prompt configuration."""

    # Check if Gemini API is configured
    error_msg = check_gemini_available()
    if error_msg:
        return AgentPromptResponse(output=error_msg, success=False, session_id=None)

    # Save prompt before execution
    save_prompt(request.prompt, request.adw_id, request.agent_name)

    # Create output directory if needed
    output_dir = os.path.dirname(request.output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        # Initialize Gemini model
        model = genai.GenerativeModel(request.model)

        # Call Gemini API
        response = model.generate_content(
            request.prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=4096,
            )
        )

        # Extract response text
        response_text = response.text if response else ""

        # Create response object
        result = {
            "type": "result",
            "output": response_text,
            "model": request.model,
            "success": True
        }

        # Write output in JSONL format for consistency
        with open(request.output_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(result) + "\n")

        print(f"Output saved to: {request.output_file}")

        return AgentPromptResponse(
            output=response_text,
            success=True,
            session_id=None
        )

    except Exception as e:
        error_msg = f"Error executing Gemini API: {str(e)}"
        print(error_msg, file=sys.stderr)

        # Write error to output file
        error_result = {
            "type": "result",
            "output": error_msg,
            "model": request.model,
            "success": False
        }

        with open(request.output_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(error_result) + "\n")

        return AgentPromptResponse(output=error_msg, success=False, session_id=None)


def execute_template(request: AgentTemplateRequest) -> AgentPromptResponse:
    """Execute a Gemini template with slash command and arguments."""
    # Construct prompt from slash command and args
    prompt = f"{request.slash_command} {' '.join(request.args)}"

    # Create output directory with adw_id at project root
    # __file__ is in adws/adw_modules/, so we need to go up 3 levels to get to project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(
        project_root, "agents", request.adw_id, request.agent_name
    )
    os.makedirs(output_dir, exist_ok=True)

    # Build output file path
    output_file = os.path.join(output_dir, "raw_output.jsonl")

    # Create prompt request with specific parameters
    prompt_request = AgentPromptRequest(
        prompt=prompt,
        adw_id=request.adw_id,
        agent_name=request.agent_name,
        model=request.model,
        dangerously_skip_permissions=True,
        output_file=output_file,
    )

    # Execute and return response (prompt_gemini now handles all parsing)
    return prompt_gemini(prompt_request)
