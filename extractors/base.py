# extractors/base.py
from abc import ABC, abstractmethod

class BaseExtractor(ABC):

    @abstractmethod
    def extract(self, pdf_path: str) -> dict:
        """
        Returns:
        {
          "text": str,
          "json_path": str
        }
        """
        pass
