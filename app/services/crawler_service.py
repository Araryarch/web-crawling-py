from typing import Dict, Any
from app.domain.entities import CrawlResult
from app.domain.exceptions import InvalidUrlError, DomainException
from app.use_cases.crawl_website import CrawlWebsiteUseCase


class CrawlerService:
    def __init__(self, crawl_use_case: CrawlWebsiteUseCase):
        self.crawl_use_case = crawl_use_case
    
    def crawl_website(self, url: str) -> Dict[str, Any]:
        result: CrawlResult = self.crawl_use_case.execute(url)
        return result.to_dict()
    
    def validate_url(self, url: str) -> bool:
        try:
            self.crawl_use_case._validate_url(url)
            return True
        except InvalidUrlError:
            return False
