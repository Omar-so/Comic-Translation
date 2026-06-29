# app/dependencies.py
from utils.cache import ImageCache
from strategies.cdn.strategy import get_cdn_strategy
from config import settings

def get_cache() -> ImageCache:
    return ImageCache()  

def get_cacheget_cdn():
    return get_cdn_strategy(settings.cdn_strategy)