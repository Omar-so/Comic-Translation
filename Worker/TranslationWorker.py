# worker.py — only imported by Celery worker process
from celery_app import celery
from celery.signals import worker_process_init
import torch
import os

from strategies.translation.Hunyuan import HunyuanTranslation
from strategies.detection.Textsegmenter import TextSegmenter
from strategies.ocr.paddle import PaddleOCR
from utils.Lame import Inpainting
from utils.cache import ImageCache
from strategies.detection.factory import get_detection_stratgy
from strategies.ocr.strategy import get_ocr_strategy
from strategies.translation.strategy import get_translation_stratgy
from strategies.cdn.strategy import get_cdn_strategy
from config import settings

# globals
lama_model = None
yolo_model = None
ocr_model = None
translation_pipe = None
device = None
detector = None
ocr_strategy = None
cdn_strategy = None
translation_strategy = None

if not torch.cuda.is_available():
    device = "cpu"
    lama_model, _ = Inpainting.load_lama_model("cpu")
    lama_model.share_memory()
    yolo_model = TextSegmenter.load_text_segmentation_model()
    yolo_model.model.share_memory()
    ocr_model = PaddleOCR.load_model(use_gpu=False)
    translation_pipe = HunyuanTranslation.build_pipeline(-1)
else:
    Inpainting.load_lama_model("cuda")
    TextSegmenter.load_text_segmentation_model()
    PaddleOCR.load_model(use_gpu=True)
    HunyuanTranslation.build_pipeline(0)

@worker_process_init.connect
def load_models(**kwargs):
    global lama_model, yolo_model, ocr_model, translation_pipe, device
    global detector, ocr_strategy, cdn_strategy, translation_strategy

    if torch.cuda.is_available():
        device = "cuda"
        lama_model, _ = Inpainting.load_lama_model("cuda")
        yolo_model = TextSegmenter.load_text_segmentation_model()
        ocr_model = PaddleOCR.load_model(use_gpu=True)
        translation_pipe = HunyuanTranslation.build_pipeline(0)

    ImageCache.connectsync()

    detector = get_detection_stratgy(settings.detection_strategy)
    ocr_strategy = get_ocr_strategy(settings.ocr_strategy)
    cdn_strategy = get_cdn_strategy(settings.cdn_strategy)
    translation_strategy = get_translation_stratgy(settings.translation_strategy)