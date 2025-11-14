# Gemini API Setup - Complete Guide

## Overview

Your ADW project has been updated to use **Google's Gemini API** instead of Anthropic's Claude or OpenAI. This gives you access to Google's latest AI models with a free API tier.

## What Changed?

### Before (Claude Code)
```
Claude Code CLI → Anthropic API → ANTHROPIC_API_KEY required
```

### After (Gemini)
```
google-generativeai SDK → Google Gemini API → GEMINI_API_KEY required
```

## Key Benefits

✅ **Free Tier Available** - 60 requests/minute at no cost
✅ **Latest Models** - Access to Gemini 2.0 Flash, 1.5 Pro, and 1.5 Flash
✅ **No CLI Needed** - Direct Python API integration
✅ **Simple Setup** - Just need API key and one Python package

## Setup Steps

### 1. Get Gemini API Key (Free)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Select or create a Google Cloud project
4. Copy your API key

### 2. Install Dependencies

```bash
# Using uv (recommended)
pip install google-generativeai
# or with uv:
uv pip install google-generativeai
```

### 3. Set Environment Variable

**Option A: Inline (for testing)**
```bash
export GEMINI_API_KEY="your-api-key-here"
cd adws
uv run adw_plan_build.py 13
```

**Option B: .env file (recommended)**
```bash
# Copy the sample
cp .env.sample .env

# Edit .env
nano .env
# or edit in your editor

# Add your key:
GEMINI_API_KEY=your-api-key-here
```

**Option C: System environment**
```bash
# macOS/Linux
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# Windows PowerShell
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY","your-api-key-here","User")
```

### 4. Verify Setup

```bash
cd adws
python -c "import google.generativeai as genai; print('✓ Gemini SDK installed')"
echo "Using model: gemini-2.5-flash (latest)"
```

## Usage

### Run ADW Workflow

```bash
cd adws

# Plan and build (full workflow)
uv run adw_plan_build.py 13

# Plan only
uv run adw_plan.py 13

# Build only
uv run adw_build.py 13
```

## Configuration Options

### Models Available

Edit `.env` file to specify which Gemini model to use:

```env
# Default (latest, fastest, recommended)
GEMINI_MODEL=gemini-2.5-flash

# Previous version (stable)
GEMINI_MODEL=gemini-2.0-flash

# Pro model (more capable but slower)
GEMINI_MODEL=gemini-1.5-pro

# Flash model (fast, balanced, older)
GEMINI_MODEL=gemini-1.5-flash
```

### GitHub Token (Optional)

If you want to use a different GitHub account:

```env
GITHUB_PAT=ghp_your_github_token_here
```

## Files Modified

### Core Changes
- **adws/adw_modules/agent.py** - Switched from Claude Code CLI to Gemini API
- **adws/adw_modules/data_types.py** - Updated model types to support Gemini
- **adws/adw_plan.py** - Updated to require GEMINI_API_KEY
- **adws/adw_build.py** - Updated to require GEMINI_API_KEY

### Configuration
- **.env.sample** - Added GEMINI_API_KEY and GEMINI_MODEL
- **adws/README.md** - Updated with Gemini setup instructions
- **adws/adw_plan_build.py** - Updated dependencies

### Scripts Updated
- adw_plan_build.py
- adw_plan.py
- adw_build.py

All scripts now include `google-generativeai` in their dependencies.

## Troubleshooting

### Error: "GEMINI_API_KEY environment variable not set"
**Solution**: Make sure you've set the environment variable
```bash
export GEMINI_API_KEY="your-key"
```

### Error: "google-generativeai not installed"
**Solution**: Install the package
```bash
pip install google-generativeai
```

### Error: "Failed to connect to Gemini API"
**Possible causes**:
- Invalid API key (check it's copied correctly)
- API not enabled in Google Cloud project
- Rate limit exceeded (free tier: 60 req/min)

### Slow responses
- Free tier is rate-limited - consider upgrading to paid tier
- Use faster model: `gemini-2.0-flash`

## API Rate Limits

### Free Tier
- 60 requests per minute
- 1,500 requests per day
- No cost

### Paid Tier
- Higher limits available
- Per-request pricing
- Set up billing in Google Cloud

## Switching Models

To use a different model, edit `.env`:

```env
# Fastest, latest (recommended)
GEMINI_MODEL=gemini-2.5-flash

# Previous stable version
GEMINI_MODEL=gemini-2.0-flash

# More capable but slower
GEMINI_MODEL=gemini-1.5-pro

# Balance between speed and quality
GEMINI_MODEL=gemini-1.5-flash
```

## How It Works

1. Your ADW script sends a prompt to Google's Gemini API
2. Gemini processes and generates a response
3. Response is saved to output file in JSON format
4. ADW continues with the workflow

```
┌─────────────┐
│ ADW Script  │
└──────┬──────┘
       │
       ├─→ Prepares prompt
       │
       ├─→ Calls Gemini API with google-generativeai SDK
       │
       ├─→ Receives response
       │
       ├─→ Saves to output file
       │
       └─→ Continues workflow
```

## Example Workflow

```bash
# 1. Set up environment
export GEMINI_API_KEY="AIza..."

# 2. Run the workflow
cd adws
uv run adw_plan_build.py 13

# Expected output:
# ✓ GEMINI_API_KEY configured
# ✓ Fetching GitHub issue #13
# ✓ Classifying issue with Gemini
# ✓ Generating plan with Gemini
# ✓ Implementing solution with Gemini
# ✓ Creating pull request
```

## Support

### Google Gemini Documentation
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [google-generativeai Python SDK](https://github.com/google/generative-ai-python)

### Pricing
- Free tier: No credit card required
- Paid tier: [Check Google Cloud pricing](https://ai.google.dev/pricing)

## Migration from Claude Code

If you were previously using Claude Code CLI:

1. ✅ Remove ANTHROPIC_API_KEY from .env
2. ✅ Get free GEMINI_API_KEY from Google AI Studio
3. ✅ Run same commands - everything else works the same!

No code changes needed in your ADW scripts - we've already updated them!

## Next Steps

1. Get your Gemini API key
2. Set GEMINI_API_KEY environment variable
3. Run: `uv run adw_plan_build.py <issue-number>`
4. Watch as Gemini AI plans and implements your features!

---

**Questions?** Check the main README.md or visit https://aistudio.google.com/app/apikey for API key help.
