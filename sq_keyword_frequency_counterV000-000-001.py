# file name: sq_keyword_frequency_counter.py
# version: V000-000-001
# Output file: data/search_query_word_frequency.csv
# Below is a Python script that reads a search query CSV file, counts the frequency of each word, and then writes the word-frequency pairs to an output CSV file:
# file name: sq_keyword_frequency_counter.py

import csv
from collections import Counter

def count_word_frequency(query_file):
    """Count the frequency of each word and the total metrics in the search query file."""
    word_frequency = Counter()
    impressions_total = Counter()
    clicks_total = Counter()
    ff_purchases_total = Counter()
    cost_total = Counter()
    ff_leads_total = Counter()
    ff_BRSubmit_total = Counter()
    ff_DMSubmit_total = Counter()
    ff_PhoneGet_total = Counter()
    with open(query_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header row
        clicks_index = header.index('Clicks') if 'Clicks' in header else None
        ff_purchases_index = header.index('ff_purchases') if 'ff_purchases' in header else None
        cost_index = header.index('Cost') if 'Cost' in header else None
        impr_index = header.index('Impr.') if 'Impr.' in header else None
        ff_leads_index = header.index('ff_leads') if 'ff_leads' in header else None
        ff_BRSubmit_index = header.index('ff_BRSubmit') if 'ff_BRSubmit' in header else None
        ff_DMSubmit_index = header.index('ff_DMSubmit') if 'ff_DMSubmit' in header else None
        ff_PhoneGet_index = header.index('ff_PhoneGet') if 'ff_PhoneGet' in header else None
        if clicks_index is None:
            raise ValueError("Clicks column not found in input CSV file")
        if ff_purchases_index is None:
            raise ValueError("ff_purchases column not found in input CSV file")
        if ff_leads_index is None:
            raise ValueError("ff_leads column not found in input CSV file")
        if ff_BRSubmit_index is None:
            raise ValueError("ff_BRSubmit column not found in input CSV file")
        if ff_DMSubmit_index is None:
            raise ValueError("ff_DMSubmit column not found in input CSV file")
        if ff_PhoneGet_index is None:
            raise ValueError("ff_PhoneGet column not found in input CSV file")
        if cost_index is None:
            raise ValueError("Cost column not found in input CSV file")
        if impr_index is None:
            raise ValueError("Impr. column not found in input CSV file")
        for row in reader:
            query = row[0].strip()  # Assuming search queries are in the first column
            impressions = int(float(row[impr_index]))  # Assuming impressions are in the "Impr." column
            clicks = int(float(row[clicks_index]))
            ff_purchases = float(row[ff_purchases_index])  # Convert to float instead of int
            ff_leads = float(row[ff_leads_index])  # Convert to float instead of int
            ff_BRSubmit = float(row[ff_BRSubmit_index])  # Convert to float instead of int
            ff_DMSubmit = float(row[ff_DMSubmit_index])  # Convert to float instead of int
            ff_PhoneGet = float(row[ff_PhoneGet_index])  # Convert to float instead of int
            cost = float(row[cost_index])  # Convert to float
            words = query.split()
            word_frequency.update(words)
            for word in set(words):
                impressions_total[word] += impressions
                clicks_total[word] += clicks
                ff_purchases_total[word] += ff_purchases
                ff_leads_total[word] += ff_leads
                ff_BRSubmit_total[word] += ff_BRSubmit
                ff_DMSubmit_total[word] += ff_DMSubmit
                ff_PhoneGet_total[word] += ff_PhoneGet
                cost_total[word] += cost
    return word_frequency, impressions_total, clicks_total, ff_purchases_total, cost_total, ff_leads_total, ff_BRSubmit_total, ff_DMSubmit_total, ff_PhoneGet_total

def write_word_frequency(word_frequency, impressions_total, clicks_total, ff_purchases_total, cost_total, ff_leads_total, ff_BRSubmit_total, ff_DMSubmit_total, ff_PhoneGet_total, output_file):
    """Write word-frequency pairs and total metrics to an output CSV file."""
    # Sort by 'Total ff_purchases' instead of 'word frequency'
    sorted_word_frequency = sorted(ff_purchases_total.items(), key=lambda x: x[1], reverse=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Word", "Frequency", "Total Impressions", "Total Clicks", "Total ff_purchases", "Total Cost", "Total ff_leads", "Total ff_BRSubmit", "Total ff_DMSubmit", "Total ff_PhoneGet", "Total Cost Per Click", "Total Cost Per ff_purchases", "Total ff_purchases_lead Rate","Total ff_purchases Rate", "Total ff_leads_BRSubmit_rate", "Total Click Thru Rate"])
        for word, total_ff_purchases in sorted_word_frequency:
            frequency = word_frequency[word]
            total_impressions = impressions_total[word]
            total_clicks = clicks_total[word]
            total_ff_purchases = round(total_ff_purchases, 2)  # Round to 2 decimal places
            total_ff_leads = round(ff_leads_total[word], 2)  # Round to 2 decimal places
            total_ff_BRSubmit = round(ff_BRSubmit_total[word], 2)  # Round to 2 decimal places
            total_ff_DMSubmit = round(ff_DMSubmit_total[word], 2)  # Round to 2 decimal places
            total_ff_PhoneGet = round(ff_PhoneGet_total[word], 2)  # Round to 2 decimal places
            total_cost = cost_total[word]
            total_cost_per_click = round(total_cost / total_clicks, 2) if total_clicks > 0 else 0
            total_cost_per_ff_purchases = round(total_cost / total_ff_purchases, 2) if total_ff_purchases > 0 else 0
            total_ff_purchases_leads_rate = round(total_ff_purchases / total_ff_leads, 2) if total_ff_leads > 0 else 0
            total_ff_purchases_rate = round(total_ff_purchases / total_clicks, 2) if total_clicks > 0 else 0
            total_ff_leads_BRSubmit_rate = round(total_ff_leads / total_ff_BRSubmit, 2) if total_ff_BRSubmit > 0 else 0
            total_click_thru_rate = round(total_clicks / total_impressions, 2) if total_impressions > 0 else 0
            writer.writerow([word, frequency, total_impressions, total_clicks, total_ff_purchases, total_cost, total_ff_leads, total_ff_BRSubmit, total_ff_DMSubmit, total_ff_PhoneGet, total_cost_per_click, total_cost_per_ff_purchases, total_ff_purchases_leads_rate, total_ff_purchases_rate, total_ff_leads_BRSubmit_rate, total_click_thru_rate])

if __name__ == "__main__":
    query_file = "output/FINAL_merged_output.csv"  # Path to the CSV file containing search queries and metrics
    output_file = "output/search_query_word_frequency.csv"  # Output CSV file
    word_frequency, impressions_total, clicks_total, ff_purchases_total, cost_total, ff_leads_total, ff_BRSubmit_total, ff_DMSubmit_total, ff_PhoneGet_total = count_word_frequency(query_file)
    write_word_frequency(word_frequency, impressions_total, clicks_total, ff_purchases_total, cost_total, ff_leads_total, ff_BRSubmit_total, ff_DMSubmit_total, ff_PhoneGet_total, output_file)
