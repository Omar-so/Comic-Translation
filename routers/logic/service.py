import asyncio
from sqlalchemy.orm import Session

from models.chapter import Chapter
from config import settings
from .utils import build_canvas
from schema import TranslateComicRequest
from fastapi import FastAPI, Response , Request

from tasks.pipeline import process

from strategies.cdn.base import CDNStrategy
from utils.cache import ImageCache
import json


async def create_chapters(
    payload: TranslateComicRequest,
    contents: list[bytes],
    user,
    db: Session,
    cdn: CDNStrategy
) -> list[int]:
    chapter_ids = []
    cursor = 0

    chapter_id = payload.ChapterID  
 

        # build canvas + derive positions from actual image shapes
    canvas_bytes, positions =  build_canvas( contents )
    

    canvas_url = await cdn.upload(canvas_bytes, f"{chapter_id}.png")

    chapter = Chapter(
            comic_name=payload.MangaID,
            chapter_id=chapter_id,
            canvas_url_before=canvas_url,
            canvas_url_after="",
            user_id=user.id,
        )
    db.add(chapter)
    db.flush()

    celery_payload = {
            "user_id":user.user_id,
            "MangaID": payload.MangaID,
            "CanvasURL": canvas_url,
            "target_language": payload.target_language,
            "Chapters_data": {
                "ChapterID": chapter_id,
                "Pages": positions,   
            },
        }
    process.delay(celery_payload)
    db.commit()
    return chapter_ids

# timeout path
#client ←──── FIN ────── nginx    (idle too long, nginx closes)

# max requests path  
#client ←──── FIN ────── nginx    (100 requests done, nginx closes)

async def event_stream(user_id: str, request: Request, cache: ImageCache, last_id: str = "$"):
    stream_key = f"notifications:{user_id}"
    while True:
        if await request.is_disconnected():   # client send fin
            break
        result = await cache.xread({stream_key: last_id}, block=15000, count=10)
        if not result:
            yield ": keepalive\n\n"
            continue
        for _, messages in result:
            for msg_id, fields in messages:
                last_id = msg_id
                await cache.setAsync(
                    f"{fields['comic_id']}:{fields['chapter_id']}",
                    fields,
                    86400
                )
                data = json.dumps(fields)
                yield f"id: {msg_id}\ndata: {data}\n\n"