#!/bin/bash
# MCP Playwright Connection Test Script

echo "========================================"
echo "MCP Playwright Connection Test"
echo "========================================"
echo

echo "Step 1: Testing Playwright MCP installation..."
if npx -y -- @playwright/mcp --version; then
    echo "✓ Playwright MCP is installed"
else
    echo "✗ Installation failed"
    exit 1
fi
echo

echo "Step 2: Testing MCP server startup..."
echo "Starting server in background for 5 seconds..."
timeout 5 npx -y -- @playwright/mcp --isolated --headless --viewport-size 1920,1080 &
SERVER_PID=$!
sleep 2

if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo "✓ Server started successfully (PID: $SERVER_PID)"
    kill $SERVER_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null
else
    echo "✗ Server failed to start"
    exit 1
fi
echo

echo "Step 3: Checking configuration..."
if [ -f ".mcp.json" ]; then
    echo "✓ .mcp.json exists:"
    cat .mcp.json | python -m json.tool 2>/dev/null || cat .mcp.json
else
    echo "✗ .mcp.json not found!"
    exit 1
fi
echo

echo "========================================"
echo "All tests passed!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Restart Claude Code"
echo "2. Run: /mcp"
echo "3. Playwright should be connected"
echo
