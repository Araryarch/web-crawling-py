"""
Test script untuk DFS Web Crawler
"""
import sys
sys.path.insert(0, '.')

from app import create_app
from app.container.service_container import get_container

def test_crawl():
    """Test basic crawl functionality"""
    app = create_app()
    
    with app.app_context():
        container = get_container()
        crawler_service = container.get_crawler_service()
        
        # Test dengan path (bukan hanya base domain)
        # Bisa juga: "https://example.com/test/apa/"
        test_url = "https://httpbin.org/html"
        print(f"Testing crawl untuk: {test_url}")
        print("(Membuktikan crawler bisa start dari path apapun)\n")
        
        result = crawler_service.crawl_website(test_url)
        
        # Print result
        print("=" * 60)
        print("HASIL CRAWL:")
        print("=" * 60)
        print(f"Start URL: {result['start_url']}")
        print(f"Pages Crawled: {result['pages_crawled']}")
        print(f"Max Depth: {result['max_depth_reached']}")
        
        print(f"\n📗 Valid Routes ({len(result['found_routes'])}):")
        for route in result['found_routes']:
            depth = result['route_depths'].get(route, '?')
            print(f"   ✓ {route} (depth: {depth})")
        
        print(f"\n📕 Invalid Routes ({len(result['invalid_routes'])}):")
        for route in result['invalid_routes']:
            depth = result['route_depths'].get(route, '?')
            print(f"   ✗ {route} (depth: {depth})")
        
        # Validasi: tidak ada duplikat
        valid_set = set(result['found_routes'])
        invalid_set = set(result['invalid_routes'])
        duplicate = valid_set.intersection(invalid_set)
        
        print(f"\n{'=' * 60}")
        print("VALIDASI:")
        print("=" * 60)
        
        if duplicate:
            print(f"❌ GAGAL: Route duplikat ditemukan: {duplicate}")
        else:
            print("✓ PASS: Tidak ada route duplikat")
        
        # Validasi page count
        validation = result['validation']
        print(f"\nValid count: {validation['valid_count']}")
        print(f"Invalid count: {validation['invalid_count']}")
        print(f"Total count: {validation['total_count']}")
        print(f"Pages crawled: {validation['pages_crawled']}")
        
        if validation['is_valid']:
            print("✓ PASS: Page count validation passed")
        else:
            print("❌ GAGAL: Page count validation failed")
        
        # Print tree visual jika ada
        if 'tree_visual' in result:
            print(f"\n{'=' * 60}")
            print("TREE VISUAL:")
            print("=" * 60)
            print(result['tree_visual'])

if __name__ == '__main__':
    test_crawl()
