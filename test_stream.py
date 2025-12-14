"""
Test script untuk streaming DFS Web Crawler
"""
import sys
sys.path.insert(0, '.')

from app import create_app
from app.container.service_container import get_container

def test_stream():
    """Test streaming crawl functionality"""
    app = create_app()
    
    with app.app_context():
        container = get_container()
        crawler = container.get_crawler()
        
        test_url = "https://example.com"
        print(f"Testing STREAMING crawl untuk: {test_url}\n")
        print("=" * 60)
        
        for event in crawler.crawl_stream(test_url):
            event_type = event['type']
            
            if event_type == 'start':
                print(f"🚀 START: Crawling {event['url']}")
                print(f"   Max Pages: {event['max_pages']}, Max Depth: {event['max_depth']}")
            
            elif event_type == 'page':
                status = "✓" if event['is_valid'] else "✗"
                print(f"📄 PAGE: [{status}] {event['route']} (depth: {event['depth']})")
                print(f"   Progress: {event['progress']}% | Queue: {event['queue_size']} | Crawled: {event['pages_crawled']}")
            
            elif event_type == 'complete':
                result = event['result']
                print("\n" + "=" * 60)
                print("✅ COMPLETE!")
                print(f"   Total Pages: {result.pages_crawled}")
                print(f"   Valid: {len(result.found_routes)}")
                print(f"   Invalid: {len(result.invalid_routes)}")
                print(f"   Max Depth: {result.max_depth_reached}")
                print("\n🌳 Tree:")
                print(result.get_tree_visual())

if __name__ == '__main__':
    test_stream()
