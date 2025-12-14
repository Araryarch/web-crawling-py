from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class TreeNode:
    """Representasi node dalam tree crawl"""
    url: str
    route: str
    depth: int
    is_valid: bool
    children: List['TreeNode'] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            'url': self.url,
            'route': self.route,
            'depth': self.depth,
            'is_valid': self.is_valid,
            'children': [child.to_dict() for child in self.children]
        }
    
    def to_tree_string(self, prefix: str = "", is_last: bool = True) -> str:
        """Menghasilkan representasi string tree yang visual"""
        connector = "└── " if is_last else "├── "
        status = "✓" if self.is_valid else "✗"
        result = f"{prefix}{connector}[{status}] {self.route} (depth: {self.depth})\n"
        
        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(self.children):
            is_last_child = (i == len(self.children) - 1)
            result += child.to_tree_string(child_prefix, is_last_child)
        
        return result


@dataclass
class CrawlResult:
    start_url: str
    found_routes: List[str] = field(default_factory=list)
    invalid_routes: List[str] = field(default_factory=list)
    pages_crawled: int = 0
    max_depth_reached: int = 0
    tree: Optional[TreeNode] = None
    route_depths: Dict[str, int] = field(default_factory=dict)  # route -> depth mapping
    
    def validate_page_count(self) -> bool:
        """Validasi bahwa valid + invalid = pages_crawled"""
        total = len(self.found_routes) + len(self.invalid_routes)
        return total == self.pages_crawled
    
    def to_dict(self) -> dict:
        result = {
            'start_url': self.start_url,
            'found_routes': sorted(self.found_routes),
            'invalid_routes': sorted(self.invalid_routes),
            'pages_crawled': self.pages_crawled,
            'max_depth_reached': self.max_depth_reached,
            'route_depths': self.route_depths,
            'validation': {
                'valid_count': len(self.found_routes),
                'invalid_count': len(self.invalid_routes),
                'total_count': len(self.found_routes) + len(self.invalid_routes),
                'pages_crawled': self.pages_crawled,
                'is_valid': self.validate_page_count()
            }
        }
        
        if self.tree:
            result['tree'] = self.tree.to_dict()
            result['tree_visual'] = self.get_tree_visual()
        
        return result
    
    def get_tree_visual(self) -> str:
        """Menghasilkan representasi visual tree"""
        if not self.tree:
            return ""
        
        status = "✓" if self.tree.is_valid else "✗"
        result = f"[{status}] {self.tree.route} (depth: {self.tree.depth})\n"
        
        for i, child in enumerate(self.tree.children):
            is_last = (i == len(self.tree.children) - 1)
            result += child.to_tree_string("", is_last)
        
        return result


@dataclass
class CrawlConfig:
    timeout: int = 10
    max_pages: int = 100
    max_depth: int = 10  # Batas kedalaman DFS
    delay: float = 0.1
    user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # Opsi untuk bypass
    verify_ssl: bool = True  # Set False untuk bypass SSL verification
    retry_count: int = 3  # Jumlah retry jika gagal
    retry_delay: float = 1.0  # Delay antara retry
    follow_redirects: bool = True
    
    # Rotasi User-Agent untuk menghindari blocking
    rotate_user_agent: bool = True
    user_agents: List[str] = field(default_factory=lambda: [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36',
    ])
