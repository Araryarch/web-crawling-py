from app.domain.interfaces import ICrawler, IUrlParser
from app.domain.entities import CrawlResult
from app.domain.exceptions import InvalidUrlError
from urllib.parse import urlparse


class CrawlWebsiteUseCase:
    def __init__(self, crawler: ICrawler, url_parser: IUrlParser):
        self.crawler = crawler
        self.url_parser = url_parser
    
    def execute(self, url: str) -> CrawlResult:
        self._validate_url(url)
        result = self.crawler.crawl(url)
        return result
    
    def _validate_url(self, url: str) -> None:
        try:
            parsed = urlparse(url)
            
            if not parsed.scheme:
                raise InvalidUrlError(url, "URL harus memiliki scheme (http/https)")
            
            if not parsed.netloc:
                raise InvalidUrlError(url, "URL harus memiliki domain/netloc")
            
            if parsed.scheme not in ['http', 'https']:
                raise InvalidUrlError(url, "URL harus menggunakan HTTP atau HTTPS")
            
            if not self.url_parser.is_safe_url(url):
                raise InvalidUrlError(url, "URL tidak aman (potensi SSRF atau hostname tidak valid)")
        
        except ValueError as e:
            raise InvalidUrlError(url, str(e))
