import requests
from bs4 import BeautifulSoup
import json

def scrape_price(url):
    """Scrape price from given URL and return JSON data"""
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find price in different possible locations
        price = "Price not found"
        
        # Look for price in common locations
        price_element = soup.find('span', class_='price') or \
                       soup.find('div', class_='price') or \
                       soup.find('meta', itemprop='price')
        
        if price_element:
            if price_element.get('content'):
                price = price_element['content']
            else:
                price = price_element.text.strip()
        
        # Create and return JSON data
        return json.dumps({
            "url": url,
            "price": price,
            "is_product_page": price != "Price not found"
        }, indent=4)
        
    except requests.RequestException as e:
        return json.dumps({
            "url": url,
            "error": str(e)
        }, indent=4)

if __name__ == "__main__":
    # Example URL
    url = "https://halsokraft.se/kosttillskott/vitaminer/d-vitamin/d3-vitamin-2000-90-kapslar"
    
    # Scrape and print the result
    result = scrape_price(url)
    print(result)
