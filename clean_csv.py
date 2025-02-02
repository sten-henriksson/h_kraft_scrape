import json
import csv

def json_to_csv(input_file, output_file):
    """Convert JSON to CSV with title and price columns"""
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Extract all results
    results = data[0]['results']
    
    # Write to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'price'])  # Write header
        
        for item in results:
            writer.writerow([item['title'], item['price']])

if __name__ == '__main__':
    json_to_csv('crawled_clean.json', 'output.csv')
