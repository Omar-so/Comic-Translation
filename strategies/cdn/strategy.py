from strategies.cdn.local import LocalCDNStrategy
from strategies.cdn.cloudinary import CloudinaryCDNStrategy
from  strategies.cdn.base import CDNStrategy
from functools import lru_cache

@lru_cache(maxsize=None)
def get_cdn_strategy(name: str) -> CDNStrategy:
    if name == "local":
        return LocalCDNStrategy()
    elif name == "cloudinary":
        return CloudinaryCDNStrategy()
    else:
        raise ValueError(f"Unknown CDN strategy: {name}")