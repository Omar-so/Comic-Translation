from strategies.translation.naive import NaiveTranslation
from strategies.translation.base import TranslationStrategy
from functools import lru_cache
from .Hunyuan import HunyuanTranslation
@lru_cache(maxsize=None)
def get_translation_stratgy(name: str) -> TranslationStrategy:
    if name == "Naive":
        return NaiveTranslation()  
    if name =="hunyusn":
        return HunyuanTranslation()
    else:
        raise ValueError(f"Unknown CDN strategy: {name}")                    