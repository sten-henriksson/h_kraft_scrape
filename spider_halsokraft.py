import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque
from scrape_price import scrape_price

RESULTS_FILE = 'crawl_results.json'

class HalsokraftSpider:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited = set()
        self.queue = deque()
        self.queue.append(base_url)
        
    def extract_links(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = set()
            
            for a_tag in soup.find_all('a', href=True):
                link = urljoin(self.base_url, a_tag['href'])
                if link.startswith(self.base_url):
                    links.add(link)
            
            return links
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return set()
    
    def crawl(self, max_pages=100):
        results = []
        crawl_data = {
            'timestamp': datetime.now().isoformat(),
            'pages_crawled': 0,
            'results': []
        }
        
        while self.queue and len(results) < max_pages:
            current_url = self.queue.popleft()
            
            if current_url in self.visited:
                continue
                
            self.visited.add(current_url)
            print(f"Crawling: {current_url}")
            
            new_links = self.extract_links(current_url)
            # Scrape price with error handling
            try:
                price_data = json.loads(scrape_price(current_url))
                
                # Only store price details if it's a product page
                result = {
                    'url': current_url,
                    'links': list(new_links)
                }
                
                if price_data.get('is_product_page', False):
                    result.update({
                        'price': price_data.get('price', 'N/A'),
                        'error': price_data.get('error')
                    })
            except Exception as e:
                print(f"Error scraping price from {current_url}: {e}")
                result = {
                    'url': current_url,
                    'links': list(new_links),
                    'error': str(e)
                }
            
            results.append(result)
            
            for link in new_links:
                if link not in self.visited:
                    self.queue.append(link)
        
        crawl_data['pages_crawled'] = len(results)
        crawl_data['results'] = results
        
        # Load existing data or create new list
        if os.path.exists(RESULTS_FILE):
            try:
                with open(RESULTS_FILE, 'r') as f:
                    all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = []
        else:
            all_data = []
        
        # Append new crawl data
        all_data.append(crawl_data)
        
        # Save updated data
        with open(RESULTS_FILE, 'w') as f:
            json.dump(all_data, f, indent=4)
        
        return results

if __name__ == "__main__":
    spider = HalsokraftSpider("https://halsokraft.se")
    results = spider.crawl(max_pages=10)  # Limit to 10 pages for demo
    
    print("\nCrawl Results:")
    for result in results:
        print(f"\nURL: {result['url']}")
        if result.get('error'):
            print(f"Error: {result['error']}")
        else:
            print(f"Price: {result['price']}")
        print(f"Links found: {len(result['links'])}")
    
    print(f"\nTotal pages crawled: {len(results)}")
    print(f"Results saved to {RESULTS_FILE}")
