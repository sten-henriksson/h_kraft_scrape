import json
import csv

def json_to_csv(input_file, output_file):
    """Convert JSON crawl results to CSV with url, title, price columns"""
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['url', 'title', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in data['results']:
            writer.writerow({
                'url': result['url'],
                'title': result['title'],
                'price': result['price']
            })

def clean_to_csv(input_file, output_file):
    """Convert cleaned JSON to CSV with only title and price columns"""
    with open(input_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return
    
    # Handle both list and dictionary formats
    results = data if isinstance(data, list) else data.get('results', [])
    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['title', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            # Skip if result is not a dictionary or missing required fields
            if not isinstance(result, dict):
                continue
                
            writer.writerow({
                'title': result.get('title', 'Unknown'),
                'price': result.get('price', 'N/A')
            })

if __name__ == "__main__":

    clean_to_csv('crawled_clean.json', 'cleaned_results.csv')
