import cv2
import numpy as np
from config import settings
from utils.cache import ImageCache
from strategies.cdn.strategy  import get_cdn_strategy
from utils.renderer import render_translated_image

from celery import Celery

import json

from celery.celery import detector ,ocr_strategy ,cdn_strategy ,translation_strategy 

# [{
#  "MangaID": "string",
#  "CanvasURL": "string",
#  "target_language": "str",
#  "Chapters_data": {
#     "ChapterID": "string",
#     "Pages": [
#        {
#          "PageID": "string",
#          "x1": 0,
#          "y1": 0,
#          "w": 0,
#          "h": 0
#        }
#     ]
#  }
# }]
    
@celery.task(
        bind=True,
        max_retries=3    )
def process(self, job: dict) -> dict:
        user_id = job["user_id"]
        image_url = job["CanvasURL"]
        comic_id  = job["MangaID"]
        chapter_id = job["Chapters_data"]["ChapterID"]

            
 
        # 3. Run pipeline
        #    a. Detection
        boxes , future =  self.detector.detect(job)



        if not boxes:
            raise ValueError("No text regions detected")

       
        ocr_result =  ocr_strategy.extract(boxes)
           

        after_translation = translation_strategy.translate_blocks(ocr_result)
        

        # image_cleared = parentconnection.recv()
        # process.join()  # Ensure detection process has completed
        # #    e. Render final image (inpainting + Pango text overlay)
       
        image_cleared =  future.result() # Ensure detection process has completed


        final_images = render_translated_image(image_cleared, after_translation)
        

        
        height = 0
        width = 0
        #glue images 
        for image in final_images: 
           h, w=  np.array(image).shape[:2]
           height=max(h,height)
           width+=w
        pages_meta = []
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        intail = 0
        for page_id, image in zip(page_ids, final_images):
            h, w = np.array(image).shape[:2]
            canvas[0:h, intail:intail + w] = image
            pages_meta.append({
                "PageID": page_id,
                "x1": intail,
                "y1": 0,
                "w": w,
                "h": h,
                "order": len(pages_meta)
            })
            intail += w


        # 4. Upload to CDN
        _, img_encoded = cv2.imencode('.png', canvas)
        img_bytes = img_encoded.tobytes()   
        cdn_url = cdn_strategy.upload(img_bytes, f"{has_been_translated}.png")    

         

      
        cache = ImageCache()
        
        cache.redis.xadd(f"notifications:{user_id}", {
            "user_id": user_id,
            "status": "success",
            "pages_meta": json.dumps(pages_meta),  # xadd values must be strings
            "image_url": cdn_url,
            "comic_id":comic_id,
            "chapter_id":chapter_id,
            "cached": "false"
        })

        