# MCP Playwright Server - Fixed Configuration

## What Was Fixed

1. **Incorrect package name**: Changed `@playwright/mcp-server` (doesn't exist) to `@playwright/mcp` (correct)
2. **Added `-y` flag**: Auto-install without prompts
3. **Removed conflicting config**: Cleared duplicate config from `.claude.json`

## Current Configuration

The MCP Playwright server is now configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "--",
        "@playwright/mcp",
        "--isolated",
        "--headless",
        "--viewport-size",
        "1920,1080"
      ]
    }
  }
}
```

**Key changes:**
- Added `--` separator after `-y` for proper npx argument parsing
- Removed `@latest` tag to use stable version
- Package name: `@playwright/mcp` (not `@playwright/mcp-server`)

## Features

- **Version**: 0.0.47
- **Isolated mode**: Each test runs in isolation
- **Headless**: Runs without visible browser window
- **Viewport**: 1920x1080 resolution
- **Auto-install**: No manual package installation needed

## How to Use

### 1. Restart Claude Code

Close and reopen Claude Code to load the new MCP configuration:

```bash
# Exit current session and start a new one
claude
```

### 2. Verify MCP Server Status

In Claude Code, run:

```
/mcp
```

You should see the Playwright MCP server listed and running.

### 3. Using with Playwright Tests

The MCP server provides tools for:
- Browser automation
- Page navigation
- Element interaction
- Screenshot capture
- Network monitoring

You can use these through Claude Code when working with web automation tasks.

## Troubleshooting

### Quick Fix (Recommended)

Run the automated fix script:

**Windows:**
```cmd
fix_mcp_playwright.bat
```

**Linux/Mac:**
```bash
bash test_mcp_connection.sh
```

### Manual Troubleshooting

If MCP still fails to connect:

1. **Check logs**:
   ```bash
   claude --debug
   ```

   Or view log files:
   ```
   C:\Users\amogh\AppData\Local\claude-cli-nodejs\Cache\C--Users-amogh-Downloads-tac5-tac-5\mcp-logs-playwright
   ```

2. **Manual test**:
   ```bash
   npx -y -- @playwright/mcp --isolated --headless --version
   ```

3. **Clear cache**:
   ```bash
   npm cache clean --force
   rm -rf C:\Users\amogh\AppData\Local\claude-cli-nodejs\Cache\C--Users-amogh-Downloads-tac5-tac-5\mcp-logs-playwright
   ```

4. **Test configuration**:
   ```bash
   cd C:\Users\amogh\Downloads\tac5\tac-5
   npx -y -- @playwright/mcp --version
   ```
   Should output: `Version 0.0.47`

### Common Issues

- **Port conflicts**: Make sure no other Playwright instances are running
- **Node.js version**: Requires Node.js 18+ (you have this installed)
- **Permissions**: Run with appropriate user permissions

## Alternative: Use Connection Helpers Instead

If you prefer direct Playwright control without MCP, use the connection helpers I created:

- `playwright_connection_helper.py` - Python helper
- `playwright_connection_helper.js` - JavaScript helper
- `test_with_connection_helper.py` - Example test
- `test_with_connection_helper.js` - Example test

These provide brute-force connection retry logic without needing MCP.

## Next Steps

1. Restart Claude Code
2. Run `/mcp` to verify the server is connected
3. Start using Playwright automation features through Claude

---

**Status**: ✅ Configuration Fixed
**Package**: @playwright/mcp@0.0.47
**Mode**: Isolated, Headless, 1920x1080
