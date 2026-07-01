# app/dependencies.py
from app.utils.cache import ImageCache
from app.strategies.cdn.strategy import get_cdn_strategy
from app.config import settings

def get_cache() -> ImageCache:
    return ImageCache()  

def get_cdn():
    return get_cdn_strategy(settings.cdn_strategy)