import requests
import logging
from typing import Optional
from app.domain.interfaces import IHttpClient

logger = logging.getLogger(__name__)

class RequestsHttpClient(IHttpClient):
    def get(self, url: str, timeout: int, headers: dict) -> Optional[str]:
        try:
            response = requests.get(url, timeout=timeout, headers=headers)
            
            if response.status_code != 200:
                logger.warning(f"Status code {response.status_code} saat mengakses: {url}")
                return None
            
            content_type = response.headers.get('Content-Type', '').lower()
            if 'text/html' not in content_type:
                logger.info(f"Skipping non-HTML content type {content_type} for: {url}")
                return None
            
            return response.text
        
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout saat mengakses: {url}")
            return None
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error saat mengakses: {url}")
            return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error untuk {url}: {e}")
            return None
        
        except Exception as e:
            logger.exception(f"Unexpected error untuk {url}: {e}")
            return None
