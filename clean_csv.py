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
        data = json.load(f)
    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['title', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in data['results']:
            writer.writerow({
                'title': result['title'],
                'price': result['price']
            })

if __name__ == "__main__":

    clean_to_csv('crawled_clean.json', 'cleaned_results.csv')
