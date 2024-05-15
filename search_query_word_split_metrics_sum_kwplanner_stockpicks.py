# search_query_word_split_metrics_sum_kwplanner_stockpicks.py
# version: V000-000-000
# plan to delete this file - not needed


import csv

def sum_total_impressions(input_file, output_file):
    # Read data from input CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['Sum Impressions']  # Add new field for sum of impressions
        
        # Create a list to store rows
        rows = []
        
        # Iterate through each row and calculate sum of impressions
        for row in reader:
            impressions = [int(x.strip()) for x in row['Total Impressions'].split(',')]
            sum_impressions = sum(impressions)
            row['Sum Impressions'] = sum_impressions
            rows.append(row)
            
        # Sort rows based on sum of impressions
        sorted_rows = sorted(rows, key=lambda x: x['Sum Impressions'], reverse=True)
        
        # Write sorted data to output CSV file
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()  # Write header row
            
            for row in sorted_rows:
                writer.writerow(row)

# Example usage: Sum total impressions and write to new CSV file
sum_total_impressions('data/search_query_word_split_metrics_kwplanner_stockpicks.csv', 'data/search_query_total_sum_word_split_kwplanner_stockpicks.csv')
