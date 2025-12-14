from dataclasses import dataclass
from typing import Optional


@dataclass
class CrawlRequest:
    url: str
    max_pages: int = 100
    max_depth: int = 10
    timeout: float = 10.0
    delay: float = 0.1
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CrawlRequest':
        if not data:
            raise ValueError("Request body tidak boleh kosong")
        
        url = data.get('url')
        if not url:
            raise ValueError("Field 'url' wajib ada")
        
        if not isinstance(url, str):
            raise ValueError("Field 'url' harus berupa string")
        
        return cls(
            url=url.strip(),
            max_pages=int(data.get('max_pages', 100)),
            max_depth=int(data.get('max_depth', 10)),
            timeout=float(data.get('timeout', 10.0)),
            delay=float(data.get('delay', 0.1))
        )


@dataclass
class ErrorResponse:
    error: str
    details: Optional[str] = None
    
    def to_dict(self) -> dict:
        result = {'error': self.error}
        if self.details:
            result['details'] = self.details
        return result
