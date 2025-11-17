@echo off
REM Fix MCP Playwright Connection Script
REM Run this if MCP is still failing

echo ========================================
echo MCP Playwright Fix Script
echo ========================================
echo.

echo Step 1: Clearing npm cache...
call npm cache clean --force
echo ✓ NPM cache cleared
echo.

echo Step 2: Clearing Claude Code MCP logs...
if exist "%LOCALAPPDATA%\claude-cli-nodejs\Cache\C--Users-amogh-Downloads-tac5-tac-5\mcp-logs-playwright" (
    rmdir /s /q "%LOCALAPPDATA%\claude-cli-nodejs\Cache\C--Users-amogh-Downloads-tac5-tac-5\mcp-logs-playwright"
    echo ✓ MCP logs cleared
) else (
    echo ⚠ No MCP logs found (already clean)
)
echo.

echo Step 3: Testing Playwright MCP installation...
call npx -y -- @playwright/mcp --version
if %ERRORLEVEL% EQU 0 (
    echo ✓ Playwright MCP is installed and working
) else (
    echo ✗ Playwright MCP installation failed
    exit /b 1
)
echo.

echo Step 4: Verifying configuration...
if exist ".mcp.json" (
    echo ✓ .mcp.json exists
    type .mcp.json
) else (
    echo ✗ .mcp.json not found!
    exit /b 1
)
echo.

echo ========================================
echo All checks passed!
echo ========================================
echo.
echo Next steps:
echo 1. Close all Claude Code sessions
echo 2. Restart Claude Code: claude
echo 3. Run: /mcp
echo 4. You should see playwright connected
echo.
echo If still failing, run: claude --debug
echo.
pause
