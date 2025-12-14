from abc import ABC, abstractmethod
from typing import List, Optional, Generator, Dict, Any
from app.domain.entities import CrawlResult


class IHttpClient(ABC):
    @abstractmethod
    def get(
        self, 
        url: str, 
        timeout: int, 
        headers: dict,
        verify_ssl: bool = True,
        retry_count: int = 1,
        retry_delay: float = 1.0,
        follow_redirects: bool = True
    ) -> Optional[str]:
        """
        Melakukan HTTP GET request.
        
        Args:
            url: URL target
            timeout: Timeout dalam detik
            headers: Custom headers
            verify_ssl: Apakah verifikasi SSL (False untuk bypass)
            retry_count: Jumlah percobaan ulang
            retry_delay: Delay antara retry
            follow_redirects: Apakah follow redirect
            
        Returns:
            HTML content atau None jika gagal
        """
        pass


class ICrawler(ABC):
    @abstractmethod
    def crawl(self, start_url: str) -> CrawlResult:
        """Non-streaming crawl - returns final result"""
        pass
    
    @abstractmethod
    def crawl_stream(self, start_url: str) -> Generator[Dict[str, Any], None, None]:
        """
        Streaming crawl - yields progress events.
        
        Event types:
        - 'start': Crawl dimulai
        - 'page': Setiap page yang di-crawl  
        - 'complete': Crawl selesai dengan result lengkap
        """
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
