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
        
        # Find the price element
        price_element = soup.find('div', class_='wfsqmst').find('div', class_='price n77d0ua')
        price = price_element.text.strip() if price_element else "Price not found"
        
        # Create and return JSON data
        return json.dumps({
            "url": url,
            "price": price
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
