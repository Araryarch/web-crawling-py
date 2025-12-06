import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List
from app.domain.interfaces import ILinkExtractor

logger = logging.getLogger(__name__)

class BeautifulSoupLinkExtractor(ILinkExtractor):
    def extract_links(self, html: str, current_url: str) -> List[str]:
        links = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(current_url, href)
                links.append(absolute_url)
        
        except Exception as e:
            logger.error(f"Error saat extract links dari {current_url}: {e}")
        
        return links
