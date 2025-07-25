import datetime
from src.utils.logging import setup_logging

logger = setup_logging()

def generate_alert(is_accident, box, location="Unknown"):
    if not is_accident:
        return None
    
    alert = {
        "timestamp": datetime.datetime.now().isoformat(),
        "location": location,
        "severity": "High" if box else "Medium",
        "details": {"bounding_box": box if box else []}
    }
    logger.info(f"Alert generated: {alert}")
    return alert