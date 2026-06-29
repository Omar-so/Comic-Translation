from abc import ABC, abstractmethod
from typing import List, Optional

from .base import TranslationStrategy

from transformers import pipeline

from celery.celery import  translation_pipe


class HunyuanTranslation(TranslationStrategy):

    @staticmethod
    def build_pipeline( Gpu : int = 0):
        return pipeline(
            "translation",
            model="tencent/HY-MT1.5-1.8B-GPTQ-Int4",
            device=Gpu  # GPU, or -1 for CPU
        )
    

                    # "page_id": box_meta["page_id"],
                    # "manga_id": box_meta["manga_id"],
                    # "box_index": box_meta["box_index"],
                    # "offset_x": box_meta["offset_x"],
                    # "offset_y": box_meta["offset_y"],
                    # "width": box_meta["weidth"],   
                    # "height": box_meta["height"],
                    # "confidence": box_meta["confidence"],
                    # "ocr_text": ocr_result,  

    def __init__(self, to_lang="en"):
        self.pipe = translation_pipe
        self.to_lang = to_lang

    def translate_blocks(self, pages: List[dict]) -> List[dict]:
        flat_text = []    
        page_lengths = []    

        for page in pages:
            valid_boxes = [box for box in page if box.get("ocr_text") is not None]
            page_lengths.append(len(valid_boxes))
            flat_text.extend(box["ocr_text"] for box in valid_boxes)

        if not flat_text:
            return [[] for _ in pages]

        translated = self.pipe(flat_text, batch_size=len(flat_text))

        all_results = []
        cursor = 0
        for page, length in zip(pages, page_lengths):
            valid_boxes = [box for box in page if box.get("ocr_text") is not None]
            
            page_translation_results = translated[cursor:cursor + length]
            cursor += length

            page_results = []
            for box_meta, text in zip(valid_boxes, page_translation_results):
                page_results.append({
                    "page_id": box_meta["page_id"],
                    "manga_id": box_meta["manga_id"],
                    "box_index": box_meta["box_index"],
                    "offset_x": box_meta["offset_x"],
                    "offset_y": box_meta["offset_y"],
                    "width": box_meta["weidth"],   
                    "height": box_meta["height"],
                    "confidence": box_meta["confidence"],
                    "text": text,      
                })

            all_results.append(page_results)

        return all_results