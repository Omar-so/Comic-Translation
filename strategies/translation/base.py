from abc import ABC, abstractmethod
from typing import List, Optional


class TranslationStrategy(ABC):
    @abstractmethod
    def translate_blocks(
        self,
        text_blocks: List[dict],
        target_lang: Optional[str] = None
    ) -> List[dict]:
        pass
