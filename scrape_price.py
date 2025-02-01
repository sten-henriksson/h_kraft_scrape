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
        price_elements = [
            soup.find('span', class_='price'),
            soup.find('div', class_='price'),
            soup.find('meta', itemprop='price'),
            soup.find('div', {'class': lambda x: x and 'price' in x}),
            soup.find('span', {'class': lambda x: x and 'price' in x})
        ]
        
        # Find first valid price element
        price_element = next((el for el in price_elements if el is not None), None)
        
        if price_element:
            try:
                if price_element.get('content'):
                    price = price_element['content']
                else:
                    price = price_element.text.strip()
            except Exception as e:
                print(f"Error extracting price from {url}: {e}")
        
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
