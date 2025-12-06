from dataclasses import dataclass, field
from typing import List


@dataclass
class CrawlResult:
    start_url: str
    found_routes: List[str] = field(default_factory=list)
    invalid_routes: List[str] = field(default_factory=list)
    pages_crawled: int = 0
    
    def to_dict(self) -> dict:
        return {
            'start_url': self.start_url,
            'found_routes': sorted(self.found_routes),
            'invalid_routes': sorted(self.invalid_routes),
            'pages_crawled': self.pages_crawled
        }


@dataclass
class CrawlConfig:
    timeout: int = 10
    max_pages: int = 100
    delay: float = 0.1
    user_agent: str = 'Mozilla/5.0 (DFS Web Crawler)'
