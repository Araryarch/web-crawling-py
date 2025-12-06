from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import CrawlResult


class IHttpClient(ABC):
    @abstractmethod
    def get(self, url: str, timeout: int, headers: dict) -> Optional[str]:
        pass


class ICrawler(ABC):
    @abstractmethod
    def crawl(self, start_url: str) -> CrawlResult:
        pass


class IUrlParser(ABC):
    @abstractmethod
    def is_valid_url(self, url: str, domain: str) -> bool:
        pass
    
    @abstractmethod
    def normalize_url(self, url: str) -> str:
        pass
    
    @abstractmethod
    def extract_path(self, url: str) -> str:
        pass
    
    @abstractmethod
    def get_domain(self, url: str) -> str:
        pass

    @abstractmethod
    def is_safe_url(self, url: str) -> bool:
        """Check if URL is safe to crawl (SSRF protection)"""
        pass


class ILinkExtractor(ABC):
    @abstractmethod
    def extract_links(self, html: str, current_url: str) -> List[str]:
        pass
