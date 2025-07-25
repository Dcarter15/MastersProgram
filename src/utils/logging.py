import logging

def setup_logging(log_level="INFO"):
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename = "accident_detection_log",
        filemode="a"
    )

    return logging.getLogger() 