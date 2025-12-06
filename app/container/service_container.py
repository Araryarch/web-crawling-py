from typing import Optional
from app.domain.entities import CrawlConfig
from app.domain.interfaces import ICrawler, IHttpClient, IUrlParser, ILinkExtractor
from app.infrastructure.http_client import RequestsHttpClient
from app.infrastructure.url_parser import UrlParser
from app.infrastructure.link_extractor import BeautifulSoupLinkExtractor
from app.infrastructure.dfs_crawler import DFSWebCrawler
from app.use_cases.crawl_website import CrawlWebsiteUseCase
from app.services.crawler_service import CrawlerService


class ServiceContainer:
    def __init__(self, config: CrawlConfig):
        self.config = config
        self._http_client: Optional[IHttpClient] = None
        self._url_parser: Optional[IUrlParser] = None
        self._link_extractor: Optional[ILinkExtractor] = None
        self._crawler: Optional[ICrawler] = None
        self._crawl_use_case: Optional[CrawlWebsiteUseCase] = None
        self._crawler_service: Optional[CrawlerService] = None
    
    def get_http_client(self) -> IHttpClient:
        if self._http_client is None:
            self._http_client = RequestsHttpClient()
        return self._http_client
    
    def get_url_parser(self) -> IUrlParser:
        if self._url_parser is None:
            self._url_parser = UrlParser()
        return self._url_parser
    
    def get_link_extractor(self) -> ILinkExtractor:
        if self._link_extractor is None:
            self._link_extractor = BeautifulSoupLinkExtractor()
        return self._link_extractor
    
    def get_crawler(self) -> ICrawler:
        if self._crawler is None:
            self._crawler = DFSWebCrawler(
                http_client=self.get_http_client(),
                url_parser=self.get_url_parser(),
                link_extractor=self.get_link_extractor(),
                config=self.config
            )
        return self._crawler
    
    def get_crawl_use_case(self) -> CrawlWebsiteUseCase:
        if self._crawl_use_case is None:
            self._crawl_use_case = CrawlWebsiteUseCase(
                crawler=self.get_crawler(),
                url_parser=self.get_url_parser()
            )
        return self._crawl_use_case
    
    def get_crawler_service(self) -> CrawlerService:
        if self._crawler_service is None:
            self._crawler_service = CrawlerService(crawl_use_case=self.get_crawl_use_case())
        return self._crawler_service
    
    def reset(self):
        self._http_client = None
        self._url_parser = None
        self._link_extractor = None
        self._crawler = None
        self._crawl_use_case = None
        self._crawler_service = None


_container: Optional[ServiceContainer] = None


def init_container(config: CrawlConfig) -> ServiceContainer:
    global _container
    _container = ServiceContainer(config)
    return _container


def get_container() -> ServiceContainer:
    if _container is None:
        raise RuntimeError("Service container not initialized. Call init_container() first.")
    return _container
