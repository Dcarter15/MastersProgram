#!/bin/bash
# Navigate to project root
cd "$(dirname "$0")/.."

# Step 1: Find and kill processes matching the virtual environment path using kill
echo "Searching for Python processes in the virtual environment..."
# Escape spaces in the path for grep
VENV_PATH="/c/Users/Daniel Carter/Desktop/Masters Program/COSC_643/Final_Project/venv/Scripts/python"
# Use ps aux, grep for the path, and extract PIDs
PYTHON_PIDS=$(ps aux | grep "$VENV_PATH" | grep -v grep | awk '{print $1}')

if [ -n "$PYTHON_PIDS" ]; then
    echo "Found Python processes with PIDs: $PYTHON_PIDS"
    for PID in $PYTHON_PIDS; do
        echo "Terminating PID $PID with kill..."
        kill -9 "$PID" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "Successfully terminated PID $PID."
        else
            echo "Failed to terminate PID $PID with kill."
        fi
    done
else
    echo "No Python processes found matching the virtual environment path: $VENV_PATH"
fi

# Step 2: Fallback - Check if port 8081 is in use and free it using taskkill
echo "Checking for processes using port 8081..."
if command -v netstat >/dev/null 2>&1; then
    PORT_PID=$(netstat -aon | grep 8081 | grep LISTENING | awk '{print $5}')
    if [ -n "$PORT_PID" ]; then
        echo "Port 8081 in use by PID $PORT_PID, terminating with taskkill as fallback..."
        taskkill /PID "$PORT_PID" /F 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "Successfully terminated PID $PORT_PID."
        else
            echo "Failed to terminate PID $PORT_PID with taskkill."
        fi
    else
        echo "Port 8081 is not in use."
    fi
else
    echo "Error: netstat not found. Cannot check port 8081."
fi

# Step 3: Verify no processes remain
echo "Verifying no Python processes remain..."
PYTHON_PIDS=$(ps aux | grep "$VENV_PATH" | grep -v grep | awk '{print $2}')
if [ -n "$PYTHON_PIDS" ]; then
    echo "Warning: Python processes still running with PIDs: $PYTHON_PIDS"
else
    echo "No Python processes found matching the virtual environment path."
fi

# Step 4: Verify port 8081 is free
echo "Verifying port 8081 is free..."
if command -v netstat >/dev/null 2>&1; then
    PORT_PID=$(netstat -aon | grep 8081 | grep LISTENING | awk '{print $5}')
    if [ -n "$PORT_PID" ]; then
        echo "Port 8081 is still in use by PID $PORT_PID. Manual intervention may be required."
    else
        echo "Port 8081 is now free."
    fi
else
    echo "Warning: netstat not found. Cannot verify port 8081."
fi

echo "Server and background processes termination attempt completed."