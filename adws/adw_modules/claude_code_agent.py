"""Claude Code CLI agent module for executing prompts and slash commands.

This module integrates with the Claude Code CLI to execute slash commands
and parse JSONL output. Used for ADW planning, implementation, and other
workflow operations instead of Gemini API.
"""

import sys
import os
import json
import subprocess
from typing import Optional, List, Dict, Any, Tuple
from dotenv import load_dotenv

from .data_types import (
    AgentPromptRequest,
    AgentPromptResponse,
    AgentTemplateRequest,
)

# Load environment variables
load_dotenv()


def parse_json_output(
    output_file: str,
) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Parse JSON output file and return all messages and the result message.

    Returns:
        Tuple of (all_messages, result_message) where result_message is None if not found
    """
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return [], None

            # Try to parse as JSON (could be array or single object)
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                # If not valid JSON, try to parse as JSONL (legacy format)
                messages = [json.loads(line) for line in content.split('\n') if line.strip()]
                result_message = None
                for message in reversed(messages):
                    if message.get("type") == "result":
                        result_message = message
                        break
                return messages, result_message

            # If we got a list, treat as array of messages
            if isinstance(data, list):
                messages = data
            else:
                # Single object response
                messages = [data]

            # Find the result message (should be the last one)
            result_message = None
            for message in reversed(messages):
                if message.get("type") == "result":
                    result_message = message
                    break

            return messages, result_message
    except Exception as e:
        print(f"Error parsing JSON output file: {e}", file=sys.stderr)
        return [], None


def save_prompt(prompt: str, adw_id: str, agent_name: str = "ops") -> None:
    """Save a prompt to the appropriate logging directory."""
    import re

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
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"Saved prompt to: {prompt_file}")


def execute_claude_code_command(
    slash_command: str,
    args: List[str],
    adw_id: str,
    agent_name: str,
    output_file: str,
) -> AgentPromptResponse:
    """Execute a Claude Code slash command and capture JSON output.

    Args:
        slash_command: The slash command to execute (e.g., "/classify_issue")
        args: List of arguments for the command
        adw_id: Unique ID for this ADW workflow
        agent_name: Name of the agent executing the command
        output_file: Path where JSON output should be saved

    Returns:
        AgentPromptResponse with the command output and success status
    """

    # Create output directory if needed
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Build Claude Code command
    # Format: claude code "{slash_command} arg1 arg2 ..." --output-format json
    command_args = [slash_command] + args
    command_str = " ".join(command_args)

    try:
        # Execute Claude Code CLI
        # Note: Claude Code slash commands work with plain text output; we'll capture and parse it
        # Pass the command via stdin to avoid quoting issues with JSON arguments
        result = subprocess.run(
            ["claude", "code"],
            input=command_str,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=600  # 10 minute timeout
        )

        # Save the raw output to file
        if result.stdout:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result.stdout)

        # Parse the output - Claude Code returns plain text, we'll wrap it in JSON
        if result.stdout:
            # Wrap the output in a JSON result object for consistency
            messages = []
            result_message = {
                "type": "result",
                "output": result.stdout,
                "success": True
            }
            messages.append(result_message)
        else:
            messages = []
            result_message = None

        if result.returncode != 0:
            error_msg = result.stderr or "Claude Code command failed"
            print(f"Claude Code error: {error_msg}", file=sys.stderr)

            # Save error to output file
            error_result = {
                "type": "result",
                "output": error_msg,
                "success": False
            }
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(json.dumps(error_result) + "\n")

            return AgentPromptResponse(
                output=error_msg,
                success=False,
                session_id=None
            )

        # Extract output from result message
        output_text = ""
        if result_message:
            output_text = result_message.get("output", "")
        elif messages:
            # If no result message, use the last message content
            output_text = messages[-1].get("content", "")

        print(f"Output saved to: {output_file}")

        return AgentPromptResponse(
            output=output_text,
            success=True,
            session_id=None
        )

    except subprocess.TimeoutExpired:
        error_msg = "Claude Code command timed out (exceeded 10 minutes)"
        print(error_msg, file=sys.stderr)

        error_result = {
            "type": "result",
            "output": error_msg,
            "success": False
        }
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(error_result) + "\n")

        return AgentPromptResponse(
            output=error_msg,
            success=False,
            session_id=None
        )

    except Exception as e:
        error_msg = f"Error executing Claude Code command: {str(e)}"
        print(error_msg, file=sys.stderr)

        error_result = {
            "type": "result",
            "output": error_msg,
            "success": False
        }
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(error_result) + "\n")

        return AgentPromptResponse(output=error_msg, success=False, session_id=None)


def execute_template(request: AgentTemplateRequest) -> AgentPromptResponse:
    """Execute a Claude Code slash command template.

    Args:
        request: AgentTemplateRequest with slash command, args, and metadata

    Returns:
        AgentPromptResponse with output and success status
    """
    # Create output directory with adw_id at project root
    # __file__ is in adws/adw_modules/, so we need to go up 3 levels to get to project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(
        project_root, "agents", request.adw_id, request.agent_name
    )
    os.makedirs(output_dir, exist_ok=True)

    # Build output file path
    output_file = os.path.join(output_dir, "raw_output.json")

    # Save the prompt for debugging
    prompt = f"{request.slash_command} {' '.join(request.args)}"
    save_prompt(prompt, request.adw_id, request.agent_name)

    # Execute Claude Code command
    return execute_claude_code_command(
        slash_command=request.slash_command,
        args=request.args,
        adw_id=request.adw_id,
        agent_name=request.agent_name,
        output_file=output_file
    )
