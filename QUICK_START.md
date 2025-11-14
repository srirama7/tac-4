# Quick Start: Claude Code ADW + Gemini SQL

## 🎯 Setup in 3 Steps

### Step 1: Install Claude Code CLI
```bash
curl https://claude.com/install.sh | bash
source ~/.bashrc
claude --version  # Verify installation
```

### Step 2: Configure Environment
```bash
# In .env file:
GEMINI_API_KEY=your-gemini-key-here        # For SQL operations only
GITHUB_PAT=your-github-token               # Optional
```

### Step 3: Update Dependencies
```bash
cd adws
uv sync  # No more google-generativeai needed!
```

---

## ✨ What Works Now

### ADW (Planning & Implementation)
```bash
cd adws
uv run adw_plan_build.py 123           # Plan + Build issue #123
uv run adw_plan_build_test.py 123      # Plan + Build + Test
uv run adw_triggers/trigger_cron.py    # Auto-monitor GitHub issues
```

### SQL Operations (Still Uses Gemini)
```bash
curl -X POST http://localhost:8000/api/random-sql
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "list all customers from NY"}'
```

---

## 📊 Architecture Summary

```
┌─────────────────────┐
│   GitHub Issues     │
└──────────┬──────────┘
           │
      ┌────▼────┐
      │   ADW   │────────────► Claude Code CLI ✅ (Local)
      └────┬────┘
           │
      ┌────▼──────────┐
      │   SQL Server  │
      │   Operations  │
      └────┬──────────┘
           │
      ┌────▼──────────┐
      │  Gemini API   │✅ (SQL descriptions)
      └───────────────┘
```

---

## 🔑 Key Changes

| Component | Before | Now |
|-----------|--------|-----|
| ADW Engine | Gemini API ☁️ | Claude Code CLI 💻 |
| Execution | Remote (cloud) | Local |
| SQL Engine | Gemini | Gemini ✅ |
| Dependencies | 3 | 2 |
| Setup Time | 5 min | 2 min |

---

## 🆘 Common Issues

**"claude: command not found"**
→ Install Claude Code CLI: `curl https://claude.com/install.sh | bash`

**"GEMINI_API_KEY not set"**
→ Only needed for SQL ops. ADW doesn't need it!

**"ImportError: No module named 'google.generativeai'"**
→ Run `cd adws && uv sync` - dependency removed from ADW

---

## 📚 Full Documentation

- `CLAUDE_CODE_MIGRATION.md` - Complete migration guide
- `MIGRATION_SUMMARY.md` - All changes documented
- `.claude/commands/` - Available slash commands

---

## 🚀 Next: Deploy Locally

```bash
# Terminal 1: Backend
cd app/server
uv sync
uv run python server.py

# Terminal 2: Frontend
cd app/client
bun install
bun run dev

# Terminal 3: Monitor ADW (optional)
cd adws
uv run adw_triggers/trigger_cron.py
```

**Access:** http://localhost:5173

---

**Ready to go!** Your TAC-5 project now uses Claude Code CLI for ADW and Gemini for SQL. 🎉
