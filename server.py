import http.server
import socketserver
import json
import threading
import time
import os
import cv2
from src.data_collection.camera_feed_parser import parse_images
from src.data_collection.x_post_scraper import parse_x_posts
from src.model.cnn_accident_detection import detect_accident
from src.model.nlp_keyword_analysis import analyze_text
from src.notification.alert_generator import generate_alert
from src.utils.logging import setup_logging

logger = setup_logging()
PORT = 8081

# In-memory store for alerts
alerts = []

# Ensure frames directory exists
FRAMES_DIR = "frames"
if not os.path.exists(FRAMES_DIR):
    os.makedirs(FRAMES_DIR)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="ui", **kwargs)

    def do_GET(self):
        if self.path == "/alerts":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(alerts).encode())
        elif self.path.startswith("/frames/"):
            # Serve frame images
            try:
                with open("." + self.path, "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/alerts":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            alert = json.loads(post_data.decode())
            global alerts
            alerts.append(alert)
            logger.info(f"Alert received: {alert}")
            self.send_response(201)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"Alert added")
        else:
            self.send_response(404)
            self.end_headers()

def process_data():
    logger.info("Starting accident detection system")
    
    try:
        images = parse_images("data/images/test")
        for i, image in enumerate(images):
            is_accident, box = detect_accident(image)
            alert = generate_alert(is_accident, box, location=f"Image {i}")
            if alert:
                # Save the frame as an image
                frame_filename = f"image_{i}.jpg"
                frame_path = os.path.join(FRAMES_DIR, frame_filename)
                cv2.imwrite(frame_path, image)
                logger.info(f"Saved frame to {frame_path}")
                # Add frame URL to alert
                alert["frame_url"] = f"/frames/{frame_filename}"
                alerts.append(alert)
            time.sleep(0.1)
    except Exception as e:
        logger.error(f"Image processing failed: {e}")
    
    posts = parse_x_posts("data/raw/mock_x_posts.json")
    for post in posts:
        is_accident = analyze_text(post["text"])
        if is_accident:
            alert = generate_alert(True, None, location="Social Media")
            if alert:
                # Social media alerts won't have frames
                alert["frame_url"] = None
                alerts.append(alert)
    
    logger.info("Processing complete")

def run_server():
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        logger.info(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Start video processing in a separate thread
    processing_thread = threading.Thread(target=process_data)
    processing_thread.start()
    
    # Start the HTTP server
    run_server()