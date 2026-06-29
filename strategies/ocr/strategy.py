from app.strategies.ocr.paddleocr import PaddleOCRAPIStrategy
from app.strategies.ocr.base import OCRStrategy
from functools import lru_cache
from .paddle import PaddleOCRStrategy

@lru_cache(maxsize=None)
def get_ocr_strategy(name: str) -> OCRStrategy:
    if name == "PaddleOCR":
        return PaddleOCRAPIStrategy()
    if name =="paddle":
        return PaddleOCRStrategy()
    else:
        raise ValueError(f"Unknown OCR strategy: {name}")