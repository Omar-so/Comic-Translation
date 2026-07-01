import torch
from celery.signals import worker_process_init

from app.celery.celery import celery
from app.strategies.translation.Hunyuan import HunyuanTranslation
from app.strategies.detection.Textsegmenter import TextSegmenter
from app.strategies.ocr.paddle import PaddleOCR
from app.utils.Lame import Inpainting
from app.utils.cache import ImageCache
from app.Worker.model_registry import set_model
from app.config import settings


def _load_models(use_gpu: bool):
    device = "cuda" if use_gpu else "cpu"

    lama_model, _ = Inpainting.load_lama_model(device)
    yolo_model = TextSegmenter.load_text_segmentation_model()
    ocr_model = PaddleOCR.load_model(use_gpu=use_gpu)

    if not use_gpu:
        lama_model.share_memory()
        yolo_model.model.share_memory()

    Transltion_Pipline = HunyuanTranslation.build_pipeline(0 if use_gpu else -1)

    set_model("inpaint", lama_model)
    set_model("translation", Transltion_Pipline )
    set_model("detection", yolo_model)
    set_model("extraction", ocr_model)
    set_model("device", device)


if not torch.cuda.is_available():
    _load_models(use_gpu=False)


@worker_process_init.connect
def load_models(**kwargs):
    if torch.cuda.is_available():
        _load_models(use_gpu=True)
    ImageCache.connectsync()