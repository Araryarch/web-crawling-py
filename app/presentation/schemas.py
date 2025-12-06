from dataclasses import dataclass
from typing import Optional


@dataclass
class CrawlRequest:
    url: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CrawlRequest':
        if not data:
            raise ValueError("Request body tidak boleh kosong")
        
        url = data.get('url')
        if not url:
            raise ValueError("Field 'url' wajib ada")
        
        if not isinstance(url, str):
            raise ValueError("Field 'url' harus berupa string")
        
        return cls(url=url.strip())


@dataclass
class ErrorResponse:
    error: str
    details: Optional[str] = None
    
    def to_dict(self) -> dict:
        result = {'error': self.error}
        if self.details:
            result['details'] = self.details
        return result
