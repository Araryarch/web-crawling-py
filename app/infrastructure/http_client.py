import requests
import logging
import time
import urllib3
from typing import Optional
from app.domain.interfaces import IHttpClient

# Disable SSL warnings ketika verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


class RequestsHttpClient(IHttpClient):
    def __init__(self):
        self.session = requests.Session()
        # Set default headers yang lebih lengkap untuk bypass blocking
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get(
        self, 
        url: str, 
        timeout: int, 
        headers: dict,
        verify_ssl: bool = True,
        retry_count: int = 1,
        retry_delay: float = 1.0,
        follow_redirects: bool = True
    ) -> Optional[str]:
        """
        Melakukan HTTP GET request dengan opsi bypass yang lebih lengkap.
        
        Args:
            url: URL target
            timeout: Timeout dalam detik
            headers: Custom headers
            verify_ssl: Apakah verifikasi SSL (False untuk bypass)
            retry_count: Jumlah percobaan ulang
            retry_delay: Delay antara retry
            follow_redirects: Apakah follow redirect
        """
        merged_headers = {**self.session.headers, **headers}
        
        for attempt in range(retry_count):
            try:
                response = self.session.get(
                    url, 
                    timeout=timeout, 
                    headers=merged_headers,
                    verify=verify_ssl,
                    allow_redirects=follow_redirects
                )
                
                # Handle berbagai status code
                if response.status_code == 200:
                    content_type = response.headers.get('Content-Type', '').lower()
                    if 'text/html' not in content_type:
                        logger.info(f"Skipping non-HTML content type {content_type} for: {url}")
                        return None
                    return response.text
                
                elif response.status_code == 403:
                    logger.warning(f"403 Forbidden untuk {url}, mencoba dengan headers berbeda...")
                    # Coba dengan headers yang berbeda
                    if attempt < retry_count - 1:
                        time.sleep(retry_delay)
                        continue
                
                elif response.status_code == 429:
                    # Rate limited, tunggu lebih lama
                    wait_time = retry_delay * (attempt + 2)
                    logger.warning(f"429 Rate Limited untuk {url}, menunggu {wait_time}s...")
                    if attempt < retry_count - 1:
                        time.sleep(wait_time)
                        continue
                
                elif response.status_code in [301, 302, 307, 308]:
                    # Redirect yang tidak di-follow
                    logger.info(f"Redirect {response.status_code} untuk {url}")
                    return None
                
                elif response.status_code >= 500:
                    # Server error, coba lagi
                    logger.warning(f"Server error {response.status_code} untuk {url}")
                    if attempt < retry_count - 1:
                        time.sleep(retry_delay)
                        continue
                
                else:
                    logger.warning(f"Status code {response.status_code} saat mengakses: {url}")
                    return None
            
            except requests.exceptions.SSLError as e:
                logger.warning(f"SSL Error untuk {url}: {e}")
                if verify_ssl and attempt < retry_count - 1:
                    # Coba tanpa SSL verification pada retry berikutnya
                    logger.info(f"Retrying {url} tanpa SSL verification...")
                    verify_ssl = False
                    time.sleep(retry_delay)
                    continue
                return None
            
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout saat mengakses: {url} (attempt {attempt + 1}/{retry_count})")
                if attempt < retry_count - 1:
                    time.sleep(retry_delay)
                    continue
                return None
            
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Connection error saat mengakses: {url}")
                if attempt < retry_count - 1:
                    time.sleep(retry_delay)
                    continue
                return None
            
            except requests.exceptions.TooManyRedirects:
                logger.warning(f"Too many redirects untuk: {url}")
                return None
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error untuk {url}: {e}")
                if attempt < retry_count - 1:
                    time.sleep(retry_delay)
                    continue
                return None
            
            except Exception as e:
                logger.exception(f"Unexpected error untuk {url}: {e}")
                return None
        
        return None
