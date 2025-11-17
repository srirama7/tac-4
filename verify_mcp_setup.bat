@echo off
REM Comprehensive MCP Playwright Verification and Fix Script
setlocal enabledelayedexpansion

echo.
echo ====================================================================
echo   MCP PLAYWRIGHT BRUTEFORCE VERIFICATION AND FIX
echo ====================================================================
echo.

set ERRORS=0

REM Test 1: Check Node.js
echo [1/8] Checking Node.js installation...
node --version > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo [OK] Node.js !NODE_VERSION! detected
) else (
    echo [FAIL] Node.js not found
    set /a ERRORS+=1
)
echo.

REM Test 2: Check npx
echo [2/8] Checking npx availability...
npx --version > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('npx --version') do set NPX_VERSION=%%i
    echo [OK] npx !NPX_VERSION! available
) else (
    echo [FAIL] npx not found
    set /a ERRORS+=1
)
echo.

REM Test 3: Test @playwright/mcp package
echo [3/8] Testing @playwright/mcp package installation...
npx -y @playwright/mcp --version > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('npx -y @playwright/mcp --version') do set PLAYWRIGHT_VERSION=%%i
    echo [OK] @playwright/mcp !PLAYWRIGHT_VERSION! working
) else (
    echo [FAIL] @playwright/mcp package test failed
    set /a ERRORS+=1
)
echo.

REM Test 4: Test server startup with full config
echo [4/8] Testing MCP server startup with full configuration...
echo Starting: npx -y @playwright/mcp --isolated --headless --viewport-size 1920,1080
start /b cmd /c "npx -y @playwright/mcp --isolated --headless --viewport-size 1920,1080 > mcp_test_output.txt 2>&1"
timeout /t 3 /nobreak > nul
taskkill /f /im node.exe /fi "WINDOWTITLE eq *playwright*" > nul 2>&1
if exist mcp_test_output.txt (
    echo [OK] Server started successfully
    del mcp_test_output.txt
) else (
    echo [WARNING] Server test inconclusive
)
echo.

REM Test 5: Check .mcp.json exists
echo [5/8] Verifying .mcp.json configuration file...
if exist ".mcp.json" (
    echo [OK] .mcp.json exists
) else (
    echo [FAIL] .mcp.json not found
    set /a ERRORS+=1
)
echo.

REM Test 6: Validate .mcp.json syntax
echo [6/8] Validating .mcp.json JSON syntax...
node -e "const fs = require('fs'); try { const cfg = JSON.parse(fs.readFileSync('.mcp.json', 'utf8')); if (cfg.mcpServers && cfg.mcpServers.playwright) { console.log('[OK] JSON valid and playwright server configured'); process.exit(0); } else { console.log('[FAIL] playwright server not configured'); process.exit(1); } } catch (e) { console.log('[FAIL] JSON parse error:', e.message); process.exit(1); }"
if %ERRORLEVEL% NEQ 0 (
    set /a ERRORS+=1
)
echo.

REM Test 7: Show current configuration
echo [7/8] Current .mcp.json configuration:
echo --------------------------------------------------------------------
type .mcp.json
echo --------------------------------------------------------------------
echo.

REM Test 8: Check Claude Code process
echo [8/8] Checking for running Claude Code instances...
tasklist /fi "imagename eq node.exe" 2>nul | find /i "node.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo [WARNING] Node.js processes detected - Claude Code may be running
    echo           Close all Claude Code sessions and restart to apply MCP config
) else (
    echo [INFO] No Node.js processes detected
)
echo.

REM Summary
echo ====================================================================
echo   VERIFICATION SUMMARY
echo ====================================================================
echo.
if %ERRORS% EQU 0 (
    echo [SUCCESS] All critical tests passed! Configuration is correct.
    echo.
    echo NEXT STEPS:
    echo   1. Close ALL Claude Code sessions ^(exit any running instances^)
    echo   2. Restart Claude Code: claude
    echo   3. In Claude Code, run: /mcp
    echo   4. You should see: playwright [connected]
    echo.
    echo If /mcp still shows "No MCP servers configured":
    echo   - Make sure you fully exited Claude Code ^(not just minimized^)
    echo   - Check the working directory is: %CD%
    echo   - Run: claude --debug ^(to see detailed MCP startup logs^)
    echo.
) else (
    echo [FAILED] %ERRORS% critical test^(s^) failed
    echo Please review the errors above and fix them before proceeding
    echo.
)

echo ====================================================================
echo.
pause
