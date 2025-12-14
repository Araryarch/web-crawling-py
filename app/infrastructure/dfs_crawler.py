import time
import json
import logging
from typing import Set, Dict, List, Tuple, Generator, Any
from app.domain.interfaces import ICrawler, IHttpClient, IUrlParser, ILinkExtractor
from app.domain.entities import CrawlResult, CrawlConfig, TreeNode

logger = logging.getLogger(__name__)


class DFSWebCrawler(ICrawler):
    def __init__(self, http_client: IHttpClient, url_parser: IUrlParser, link_extractor: ILinkExtractor, config: CrawlConfig):
        self.http_client = http_client
        self.url_parser = url_parser
        self.link_extractor = link_extractor
        self.config = config
    
    def crawl(self, start_url: str) -> CrawlResult:
        """Non-streaming crawl - returns final result"""
        result = None
        for event in self.crawl_stream(start_url):
            if event['type'] == 'complete':
                result = event['result']
        return result
    
    def crawl_stream(self, start_url: str) -> Generator[Dict[str, Any], None, None]:
        """
        Streaming crawl - yields progress events.
        
        Event types:
        - 'start': Crawl dimulai
        - 'page': Setiap page yang di-crawl
        - 'complete': Crawl selesai dengan result lengkap
        """
        # Emit start event
        yield {
            'type': 'start',
            'url': start_url,
            'max_pages': self.config.max_pages,
            'max_depth': self.config.max_depth
        }
        
        result = CrawlResult(start_url=start_url)
        domain = self.url_parser.get_domain(start_url)
        
        visited_urls: Set[str] = set()
        processed_routes: Set[str] = set()
        valid_routes_set: Set[str] = set()
        invalid_routes_set: Set[str] = set()
        
        stack: List[Tuple[str, int, str | None]] = [(start_url, 0, None)]
        pages_crawled = 0
        max_depth_reached = 0
        
        node_map: Dict[str, TreeNode] = {}
        root_node: TreeNode | None = None
        
        while stack and pages_crawled < self.config.max_pages:
            current_url, current_depth, parent_url = stack.pop()
            
            if current_url in visited_urls:
                continue
            
            if current_depth > self.config.max_depth:
                continue
            
            visited_urls.add(current_url)
            
            route = self.url_parser.extract_path(current_url)
            
            if route in processed_routes:
                continue
            
            processed_routes.add(route)
            pages_crawled += 1
            
            if current_depth > max_depth_reached:
                max_depth_reached = current_depth
            
            html = self.http_client.get(
                url=current_url,
                timeout=self.config.timeout,
                headers={'User-Agent': self._get_user_agent()},
                verify_ssl=self.config.verify_ssl,
                retry_count=self.config.retry_count,
                retry_delay=self.config.retry_delay,
                follow_redirects=self.config.follow_redirects
            )
            
            is_valid = html is not None
            
            # Add new links to stack first (before emitting event)
            new_links_added = 0
            if is_valid:
                links = self.link_extractor.extract_links(html, current_url)
                
                for link in links:
                    normalized_link = self.url_parser.normalize_url(link)
                    
                    if not self.url_parser.is_valid_url(normalized_link, domain):
                        continue
                    
                    if normalized_link in visited_urls:
                        continue
                    
                    stack.append((normalized_link, current_depth + 1, current_url))
                    new_links_added += 1
            
            # Calculate actual remaining queue (filter already visited/processed)
            remaining_queue = sum(
                1 for url, depth, _ in stack 
                if url not in visited_urls and depth <= self.config.max_depth
            )
            
            # Emit page event with accurate queue size
            yield {
                'type': 'page',
                'route': route,
                'url': current_url,
                'depth': current_depth,
                'is_valid': is_valid,
                'pages_crawled': pages_crawled,
                'queue_size': remaining_queue,
                'progress': min(100, int((pages_crawled / self.config.max_pages) * 100))
            }
            
            node = TreeNode(
                url=current_url,
                route=route,
                depth=current_depth,
                is_valid=is_valid
            )
            node_map[current_url] = node
            
            if parent_url is None:
                root_node = node
            elif parent_url in node_map:
                node_map[parent_url].children.append(node)
            
            result.route_depths[route] = current_depth
            
            if is_valid:
                valid_routes_set.add(route)
            else:
                invalid_routes_set.add(route)
            
            time.sleep(self.config.delay)
        
        # Build final result
        result.found_routes = sorted(list(valid_routes_set))
        result.invalid_routes = sorted(list(invalid_routes_set))
        result.pages_crawled = pages_crawled
        result.max_depth_reached = max_depth_reached
        result.tree = root_node
        
        if not result.validate_page_count():
            logger.warning(
                f"Page count validation failed! "
                f"valid={len(result.found_routes)}, "
                f"invalid={len(result.invalid_routes)}, "
                f"total={len(result.found_routes) + len(result.invalid_routes)}, "
                f"pages_crawled={pages_crawled}"
            )
        
        # Determine stop reason
        if pages_crawled >= self.config.max_pages:
            stop_reason = 'max_pages_reached'
        elif not stack:
            stop_reason = 'queue_empty'
        else:
            stop_reason = 'unknown'
        
        result.stop_reason = stop_reason
        
        # Emit complete event
        yield {
            'type': 'complete',
            'result': result,
            'stop_reason': stop_reason
        }
    
    def _get_user_agent(self) -> str:
        """Mendapatkan User-Agent, dengan rotasi jika diaktifkan"""
        if self.config.rotate_user_agent and self.config.user_agents:
            import random
            return random.choice(self.config.user_agents)
        return self.config.user_agent
