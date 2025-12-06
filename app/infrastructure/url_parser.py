import socket
import ipaddress
import logging
from urllib.parse import urlparse, urldefrag
from app.domain.interfaces import IUrlParser

logger = logging.getLogger(__name__)

class UrlParser(IUrlParser):
    def is_safe_url(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
            if not hostname:
                return False
                
            # Allow localhost only in debug/dev mode? No, safe by default means NO localhost.
            # Convert hostname to IP(s)
            try:
                # getaddrinfo returns list of (family, type, proto, canonname, sockaddr)
                # sockaddr is (address, port) for IPv4/v6
                addr_info = socket.getaddrinfo(hostname, None)
                for res in addr_info:
                    ip_str = res[4][0]
                    ip = ipaddress.ip_address(ip_str)
                    
                    if ip.is_private or ip.is_loopback or ip.is_link_local:
                        logger.warning(f"Blocked unsafe IP {ip_str} for hostname {hostname}")
                        return False
                        
            except socket.gaierror:
                logger.warning(f"Could not resolve hostname: {hostname}")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error checking url safety: {e}")
            return False

    def is_valid_url(self, url: str, domain: str) -> bool:
        try:
            parsed = urlparse(url)
            
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Allow subdomains
            # Remove 'www.' for comparison
            url_domain = parsed.netloc.replace('www.', '')
            base_domain = domain.replace('www.', '')
            
            if url_domain != base_domain and not url_domain.endswith('.' + base_domain):
                return False
            
            if parsed.scheme not in ['http', 'https']:
                return False
            
            return True
        
        except Exception:
            return False
    
    def normalize_url(self, url: str) -> str:
        url, _ = urldefrag(url)
        
        # Parse and reconstruct to strip query params for canonical path-based crawling
        parsed = urlparse(url)
        
        # Ensure scheme and netloc are lowercased
        scheme = parsed.scheme.lower() if parsed.scheme else ''
        netloc = parsed.netloc.lower() if parsed.netloc else ''
        path = parsed.path
        
        # Remove trailing slash from path unless it is root
        if path != '/' and path.endswith('/'):
            path = path.rstrip('/')
            
        # Reconstruct without params, query, or fragment
        # This treats /page?id=1 and /page?id=2 as the same page /page
        url = f"{scheme}://{netloc}{path}"
        
        return url
    
    def extract_path(self, url: str) -> str:
        parsed = urlparse(url)
        return parsed.path if parsed.path else '/'
    
    def get_domain(self, url: str) -> str:
        parsed = urlparse(url)
        return parsed.netloc
