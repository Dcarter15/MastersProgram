# Traffic Accident Detection System

Detects accidents from a YouTube video stream and mock X posts, using GPU if available, serving alerts via a Python HTTP server to a web UI. Displays a static map if video fails, shows accident frames on click, and prompts for confirmation with appropriate alerts. Uses `hilmantm/detr-traffic-accident-detection`. Optimized for Python 3.8.

## Prerequisites
- Python 3.8
- Optional: NVIDIA GPU with CUDA 11.7/12.1
- A Creative Commons YouTube video URL (e.g., traffic camera feed)

## Setup
1. Clone repo: `git clone <repo-url>`
2. Install dependencies:
   - On Windows (Command Prompt): `cd scripts && setup.bat`
   - On Unix-like (Git Bash/WSL): `cd scripts && bash setup.sh`
3. Edit `src/utils/config.py` to set `YOUTUBE_URL` to a CC-licensed video
4. Run:
   - On Windows: `cd scripts && run_demo.bat`
   - On Unix-like: `cd scripts && bash run_demo.sh`
5. Open `http://localhost:8081`

## Features
- Displays a Leaflet map with alerts.
- Shows the accident frame when an alert is clicked (for video alerts).
- Prompts user to confirm if it's an accident.
- Alerts "Emergency services are being notified" or "Being sent for review" based on user response.

## Structure
- `/data`: X posts, models
- `/frames`: Saved accident frames
- `/src`: Python pipeline
- `/ui`: Web UI
- `/tests`: Unit tests
- `/docs`: Documentation
- `/scripts`: Setup and run scripts
- `server.py`: Python HTTP server and video processing
- `venv`: Virtual environment