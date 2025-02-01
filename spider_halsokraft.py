import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

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
        while self.queue and len(results) < max_pages:
            current_url = self.queue.popleft()
            
            if current_url in self.visited:
                continue
                
            self.visited.add(current_url)
            print(f"Crawling: {current_url}")
            
            new_links = self.extract_links(current_url)
            results.append({
                'url': current_url,
                'links': list(new_links)
            })
            
            for link in new_links:
                if link not in self.visited:
                    self.queue.append(link)
        
        return results

if __name__ == "__main__":
    spider = HalsokraftSpider("https://halsokraft.se")
    results = spider.crawl()
    print(f"Crawled {len(results)} pages")
