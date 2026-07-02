import io
import numpy as np
from PIL import Image

def build_canvas(pages: list[bytes]) -> tuple[bytes, list[dict]]:
    arrays = []
    positions = []
    cursor_y = 0

    for idx, image_bytes in enumerate(pages):
        arr = np.array(
            Image.open(io.BytesIO(image_bytes)).convert("RGBA"),
            dtype=np.uint8,
        )

        h, w = arr.shape[:2]

        positions.append({
            "PageID": idx,
            "x1": 0,
            "y1": cursor_y,
            "w": w,
            "h": h,
        })

        arrays.append(arr)
        cursor_y += h

    canvas_w = max(p["w"] for p in positions)
    canvas_h = cursor_y

    canvas = np.zeros((canvas_h, canvas_w, 4), dtype=np.uint8)

    for arr, pos in zip(arrays, positions):
        canvas[
            pos["y1"]:pos["y1"] + pos["h"],
            pos["x1"]:pos["x1"] + pos["w"],
        ] = arr

    buf = io.BytesIO()
    Image.fromarray(canvas, "RGBA").save(buf, format="PNG")
    return buf.getvalue(), positions