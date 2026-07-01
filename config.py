from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # common
    redis_url: str
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    # fastapi
    db_url: str
    session_expire_seconds: int = 10000

    # celery
    celery_app_name: str = "manga_translation"  # keep only this one
    celery_result_backend: Optional[str] = None
    celery_broker_url: str
    celery_worker_running: bool = True

    # strategies
    cdn_strategy: str = "cloudinary"
    detection_strategy: str = "textsegment"
    ocr_strategy: str = "paddle"
    translation_strategy: str = "hunyuan"

    # optional cdn extras (not currently in .env)
    cdn_bucket: Optional[str] = None
    cdn_region: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()