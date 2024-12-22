# file name: sq_keyword_frequency_counter.py
# version: V000-000-001
# Output file: data/search_query_word_frequency.csv
# Below is a Python script that reads a search query CSV file, counts the frequency of each word, and then writes the word-frequency pairs to an output CSV file:
# file name: sq_keyword_frequency_counter.py output/FINAL_merged_output_normalized_with_similarity.csv

import csv
from collections import Counter
import pandas as pd

def count_word_frequency(df):
    """Count the frequency of each word and the total metrics in the search query DataFrame."""
    word_frequency = Counter()
    impressions_total = Counter()
    clicks_total = Counter()
    ff_purchases_total = Counter()
    cost_total = Counter()
    ff_leads_total = Counter()
    ff_BRSubmit_total = Counter()
    ff_DMSubmit_total = Counter()
    ff_PhoneGet_total = Counter()

    for index, row in df.iterrows():
        query = row['search_term_final'].strip()  # Use search_term_final column
        impressions = int(float(row['Impr.']))  # Assuming impressions are in the "Impr." column
        clicks = int(float(row['Clicks']))
        ff_purchases = float(row['ff_purchases'])  # Convert to float instead of int
        ff_leads = float(row['ff_leads'])  # Convert to float instead of int
        ff_BRSubmit = float(row['ff_BRSubmit'])  # Convert to float instead of int
        ff_DMSubmit = float(row['ff_DMSubmit'])  # Convert to float instead of int
        ff_PhoneGet = float(row['ff_PhoneGet'])  # Convert to float instead of int
        cost = float(row['Cost'])  # Convert to float
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
    # Load the processed data
    df = pd.read_csv("output/FINAL_merged_output_normalized_with_similarity.csv")
    
    # Process the full data
    output_file_all = "output/search_query_word_frequency.csv"
    word_frequency, impressions_total, clicks_total, ff_purchases_total, cost_total, ff_leads_total, ff_BRSubmit_total, ff_DMSubmit_total, ff_PhoneGet_total = count_word_frequency(df)
    write_word_frequency(word_frequency, impressions_total, clicks_total, ff_purchases_total, cost_total, ff_leads_total, ff_BRSubmit_total, ff_DMSubmit_total, ff_PhoneGet_total, output_file_all)
    
    # Filter out rows where contains_city is True and process the data
    df_no_city = df[df['contains_city'] == False]
    output_file_no_city = "output/search_query_word_frequency_no_city.csv"
    word_frequency_no_city, impressions_total_no_city, clicks_total_no_city, ff_purchases_total_no_city, cost_total_no_city, ff_leads_total_no_city, ff_BRSubmit_total_no_city, ff_DMSubmit_total_no_city, ff_PhoneGet_total_no_city = count_word_frequency(df_no_city)
    write_word_frequency(word_frequency_no_city, impressions_total_no_city, clicks_total_no_city, ff_purchases_total_no_city, cost_total_no_city, ff_leads_total_no_city, ff_BRSubmit_total_no_city, ff_DMSubmit_total_no_city, ff_PhoneGet_total_no_city, output_file_no_city)
