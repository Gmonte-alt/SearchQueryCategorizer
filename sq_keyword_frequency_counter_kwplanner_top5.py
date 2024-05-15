import csv
from collections import defaultdict

def find_associated_words(input_file1, input_file2, output_file):
    """Find associated words from input_file2 based on input_file1 and save the result to output_file."""
    # Read the first input file into a dictionary
    keywords_data = {}
    with open(input_file1, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            keyword = row['Keyword'].strip()
            avg_monthly_searches = int(row['Average Monthly Searches'])
            if keyword not in keywords_data:
                keywords_data[keyword] = {'avg_monthly_searches': avg_monthly_searches, 'associated_words': []}
    
    # Read the second input file and find associated words
    with open(input_file2, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word = row['Word'].strip()
            if word in keywords_data:
                keywords_data[word]['associated_words'].append((row['Word'], int(row['Frequency'])))
    
    # Write the output file with top 5 associated words for each keyword
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Word', 'Frequency', 'Total Impressions']
        for i in range(1, 6):
            fieldnames.extend([f'Word{i}', f'Word{i}Impressions'])
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for keyword, data in keywords_data.items():
            associated_words = sorted(data['associated_words'], key=lambda x: x[1], reverse=True)[:5]
            row_data = {'Word': keyword, 'Frequency': data['avg_monthly_searches'], 'Total Impressions': sum([freq for _, freq in associated_words])}
            for i, (word, freq) in enumerate(associated_words, start=1):
                row_data[f'Word{i}'] = word
                row_data[f'Word{i}Impressions'] = freq
            writer.writerow(row_data)

if __name__ == "__main__":
    input_file1 = "c:/MyPrograms/workstation/GoogleAdsSearchReportsHrly/keywordplanner/output/nvda_kwplanner_tickers.csv"  # Path to the first CSV file
    input_file2 = output_file = "data/search_query_word_frequency_kwplanner_nvda.csv"  # Path to the second CSV file
    output_file = "data/search_query_word_frequency_kwplanner_nvda_top5.csv"  # Output CSV file
    find_associated_words(input_file1, input_file2, output_file)
