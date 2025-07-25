import json
from src.utils.logging import setup_logging

logger = setup_logging()

def parse_x_posts(file_path):
    try:
        with open(file_path, "r") as f:
            posts = json.load(f)
        logger.info(f"Parsed {len(posts)} X posts")
        return posts
    except Exception as e:
        logger.error(f"Error parsing X posts: {e}")
        return []