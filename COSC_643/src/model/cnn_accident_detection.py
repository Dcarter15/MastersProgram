import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
import numpy as np
from src.utils.logging import setup_logging

logger = setup_logging()
processor = DetrImageProcessor.from_pretrained("hilmantm/detr-traffic-accident-detection")
model = DetrForObjectDetection.from_pretrained("hilmantm/detr-traffic-accident-detection")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
logger.info(f"Using device: {device}")

def detect_accident(frame):
    try:
        inputs = processor(images=frame, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        outputs = model(**inputs)
        target_sizes = torch.tensor([frame.shape[:2]], device=device)
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.7)[0]
        
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            if model.config.id2label[label.item()] == "accident":
                logger.info(f"Accident detected with confidence {score.item()}")
                return True, box.cpu().tolist()
        return False, None
    except Exception as e:
        logger.error(f"Detection error: {e}")
        return False, None

if __name__ == "__main__":
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    is_accident, box = detect_accident(dummy_frame)
    print(f"Accident: {is_accident}, Box: {box}")