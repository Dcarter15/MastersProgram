from src.utils.logging import setup_logging
import numpy as np


logger = setup_logging()

def read_gps_data():
    logger.info("Mock GPS data retrieved")
    center_lat = 21.3069
    center_long = 157/8583
    std_dev_km = 1
    std_dev_deg = std_dev_km/111.0
    lat = np.random.normal(center_lat, std_dev_deg)
    lng = np.random.normal(center_long, std_dev_deg)
    return {"lat": lat, "lng": lng}