#!/bin/bash
# Navigate to project root
cd "$(dirname "$0")/.."

# Convert path to Windows format if running in Git Bash
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    PROJECT_ROOT=$(pwd -W)
else
    PROJECT_ROOT=$(pwd)
fi

# Create virtual environment
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    py -3.8 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment!"
        exit 1
    fi
else
    echo "Virtual environment already exists in $VENV_DIR."
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source "$VENV_DIR/Scripts/activate"
else
    source "$VENV_DIR/bin/activate"
fi

# Install Python dependencies
if [ -f "docs/requirements.txt" ]; then
    pip install -r docs/requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Python dependencies!"
        exit 1
    fi
else
    echo "Error: docs/requirements.txt not found at $PROJECT_ROOT/docs/requirements.txt!"
    exit 1
fi

# Download the DETR model
python -c "from transformers import DetrImageProcessor, DetrForObjectDetection; \
           DetrImageProcessor.from_pretrained('hilmantm/detr-traffic-accident-detection'); \
           DetrForObjectDetection.from_pretrained('hilmantm/detr-traffic-accident-detection')"
if [ $? -ne 0 ]; then
    echo "Error: Failed to download DETR model!"
    exit 1
fi

echo "Setup completed successfully. Virtual environment is active."