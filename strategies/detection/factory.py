from app.strategies.detection.roboflowdetection import RoboflowDetection
from app.strategies.detection.base import DetectionStrategy
from functools import lru_cache
from .Textsegmenter import TextSegmenter

@lru_cache(maxsize=None)
def get_detection_stratgy(name: str) -> DetectionStrategy:
    if name == "RoboflowDetection":
        return RoboflowDetection()  
    if name == "textsegment": 
        return TextSegmenter();
    else:
        raise ValueError(f"Unknown CDN strategy: {name}")