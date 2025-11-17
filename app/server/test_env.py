import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Check API keys
gemini_key = os.environ.get("GEMINI_API_KEY")
openai_key = os.environ.get("OPENAI_API_KEY")
anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

print(f"GEMINI_API_KEY: {gemini_key[:20] if gemini_key else 'NOT SET'}...")
print(f"OPENAI_API_KEY: {'SET' if openai_key else 'NOT SET'}")
print(f"ANTHROPIC_API_KEY: {'SET' if anthropic_key else 'NOT SET'}")

# Test the routing logic
if gemini_key:
    print("\nRouting: Would use Gemini (priority 1)")
elif openai_key:
    print("\nRouting: Would use OpenAI (priority 2)")
elif anthropic_key:
    print("\nRouting: Would use Anthropic (priority 3)")
else:
    print("\nRouting: NO API KEYS SET!")
