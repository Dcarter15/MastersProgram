from src.utils.config import ALERT_API_URL
from src.utils.logging import setup_logging

logger = setup_logging()

def send_alert(alert):
    if not alert:
        return False
    logger.info(f"Mock sending alert to {ALERT_API_URL}: {alert}")
    return True