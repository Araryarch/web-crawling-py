import time
from typing import Set
from app.domain.interfaces import ICrawler, IHttpClient, IUrlParser, ILinkExtractor
from app.domain.entities import CrawlResult, CrawlConfig


class DFSWebCrawler(ICrawler):
    def __init__(self, http_client: IHttpClient, url_parser: IUrlParser, link_extractor: ILinkExtractor, config: CrawlConfig):
        self.http_client = http_client
        self.url_parser = url_parser
        self.link_extractor = link_extractor
        self.config = config
    
    def crawl(self, start_url: str) -> CrawlResult:
        result = CrawlResult(start_url=start_url)
        domain = self.url_parser.get_domain(start_url)
        visited: Set[str] = set()
        stack = [start_url]
        pages_crawled = 0
        
        while stack and pages_crawled < self.config.max_pages:
            current_url = stack.pop()
            
            if current_url in visited:
                continue
            
            visited.add(current_url)

            pages_crawled += 1
            
            html = self.http_client.get(
                url=current_url,
                timeout=self.config.timeout,
                headers={'User-Agent': self.config.user_agent}
            )
            
            if html is None:
                route = self.url_parser.extract_path(current_url)
                if route not in result.invalid_routes:
                    result.invalid_routes.append(route)
                continue

            route = self.url_parser.extract_path(current_url)
            if route not in result.found_routes:
                result.found_routes.append(route)
            
            links = self.link_extractor.extract_links(html, current_url)
            
            for link in links:
                normalized_link = self.url_parser.normalize_url(link)
                
                if not self.url_parser.is_valid_url(normalized_link, domain):
                    continue
                
                if normalized_link in visited:
                    continue
                
                stack.append(normalized_link)
            
            time.sleep(self.config.delay)
        
        result.pages_crawled = pages_crawled
        
        return result
