#!/bin/bash
# Navigate to project root
cd "$(dirname "$0")/.."

# Activate virtual environment
VENV_DIR="venv"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source "$VENV_DIR/Scripts/activate"
else
    source "$VENV_DIR/bin/activate"
fi

# Kill any existing server using taskkill (Windows-compatible)
if command -v taskkill >/dev/null 2>&1; then
    # Terminate python server.py processes
    taskkill /IM python.exe /F 2>/dev/null | findstr /V "ERROR: The process \"python.exe\" not found." || echo "No existing python.exe processes found."
    taskkill /IM python3.exe /F 2>/dev/null | findstr /V "ERROR: The process \"python3.exe\" not found." || echo "No existing python3.exe processes found."
else
    echo "Warning: taskkill not found. If port 8081 is in use, server may fail to start."
fi

# Check if port 8081 is in use and free it (Windows-compatible netstat)
if command -v netstat >/dev/null 2>&1; then
    # Find PID using port 8081
    PORT_PID=$(netstat -aon | findstr ":8081" | findstr "LISTENING" | awk '{print $5}')
    if [ -n "$PORT_PID" ]; then
        echo "Port 8081 in use by PID $PORT_PID, terminating..."
        taskkill /PID $PORT_PID /F 2>/dev/null
    fi
else
    echo "Warning: netstat not found. If port 8081 is in use, server may fail to start."
fi

# Run the Python server
python server.py > server.log 2>&1 &
echo "Access UI at http://localhost:8081"
sleep 2