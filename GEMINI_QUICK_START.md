# Gemini API - Quick Start (2 Minutes)

## Step 1: Get Free API Key (1 minute)

1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Done! 🎉

## Step 2: Set Environment Variable (30 seconds)

```bash
# Option A: Quick test
export GEMINI_API_KEY="paste-your-key-here"

# Option B: Permanent (.env file)
echo 'GEMINI_API_KEY=paste-your-key-here' > .env
```

## Step 3: Install Package (30 seconds)

```bash
pip install google-generativeai
# or with uv:
uv pip install google-generativeai
```

## Step 4: Run Your Workflow! 🚀

```bash
cd adws
uv run adw_plan_build.py 13
```

That's it! No Anthropic key, no OpenAI key, no CLI tools needed.

---

## Configuration

### Choose Model (Optional)

Edit `.env`:
```env
GEMINI_API_KEY=your-key
GEMINI_MODEL=gemini-2.5-flash  # Default (latest, fastest)
# GEMINI_MODEL=gemini-2.0-flash  # Previous version
# GEMINI_MODEL=gemini-1.5-pro  # Pro model (more capable)
```

### GitHub Token (Optional)

```env
GITHUB_PAT=ghp_your_token_here
```

---

## Commands

```bash
# Full workflow (plan + build)
uv run adw_plan_build.py 13

# Plan only
uv run adw_plan.py 13

# Build only
uv run adw_build.py 13

# Individual phases
uv run adw_test.py 13
```

---

## Free Tier

✅ **60 requests per minute**
✅ **No credit card required**
✅ **Perfect for development**

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `GEMINI_API_KEY not set` | `export GEMINI_API_KEY="your-key"` |
| `google-generativeai not installed` | `pip install google-generativeai` |
| `API connection failed` | Check your API key is correct |
| `Rate limited` | Free tier = 60 req/min, wait a minute |

---

## API Key

- **Get free key**: https://aistudio.google.com/app/apikey
- **Docs**: https://ai.google.dev
- **Pricing**: Free tier included, upgrade anytime

---

## More Info

- `GEMINI_API_SETUP.md` - Detailed setup guide
- `GEMINI_MIGRATION_SUMMARY.md` - What changed
- `adws/README.md` - Full project documentation

---

**Ready?** Get your key and run: `uv run adw_plan_build.py 13` 🚀
