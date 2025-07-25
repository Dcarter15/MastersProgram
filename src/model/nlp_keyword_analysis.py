from src.utils.logging import setup_logging

logger = setup_logging()

def analyze_text(text):
    keywords = ["crash", "accident", "collision", "emergency"]
    is_accident = any(keyword in text.lower() for keyword in keywords)
    if is_accident:
        logger.info(f"Accident detected in text: {text}")
    return is_accident