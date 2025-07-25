import cv2
import numpy as np
import os
from src.utils.logging import setup_logging

logger = setup_logging()

def parse_images(images_dir):
    """
    Load images from the specified directory and yield them as frames.
    
    Args:
        images_dir (str): Path to the directory containing images.
    
    Yields:
        numpy.ndarray: Image frame in OpenCV format.
    """
    if not os.path.exists(images_dir):
        logger.error(f"Images directory {images_dir} does not exist")
        raise FileNotFoundError(f"Images directory {images_dir} not found")
    
    # Supported image extensions
    supported_extensions = (".jpg", ".jpeg", ".png")
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(supported_extensions)]
    
    if not image_files:
        logger.warning(f"No images found in {images_dir}")
        return
    
    logger.info(f"Found {len(image_files)} images in {images_dir}")
    for image_file in image_files:
        image_path = os.path.join(images_dir, image_file)
        logger.info(f"Loading image: {image_path}")
        frame = cv2.imread(image_path)
        if frame is None:
            logger.error(f"Failed to load image: {image_path}")
            continue
        yield frame