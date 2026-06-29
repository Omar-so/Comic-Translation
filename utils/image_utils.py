import requests
import cv2
import numpy as np

def download_image(url: str) -> np.ndarray:
    req = requests.get(url)
    
    req.raise_for_status()  

    arr = np.frombuffer(req.content, dtype=np.uint8)  #  raw bytes → 1D uint8 array
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)         #  decodes jpeg/png/etc → (H,W,3)

    if img is None:
        raise ValueError(f"cv2 could not decode image from {url}")  #  raise not throw

    return img