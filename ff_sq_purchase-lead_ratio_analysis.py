# file name:ff_sq_purchase-lead_ratio_analysis.py
# version: V000-000-001
# Note:
#

import pandas as pd

def load_data(file_path):
    """Load data from a CSV file."""
    return pd.read_csv(file_path)

def categorize_ratios(df):
    """Categorize search terms based on ff_purchase_to_lead_ratio."""
    # Define categories for the ratio
    categories = {
        "No Value or Zero": df['ff_purchase_to_lead_ratio'].isna() | (df['ff_purchase_to_lead_ratio'] == 0),
        "0 < Ratio <= 0.1": (df['ff_purchase_to_lead_ratio'] > 0) & (df['ff_purchase_to_lead_ratio'] <= 0.1),
        "0.1 < Ratio <= 0.2": (df['ff_purchase_to_lead_ratio'] > 0.1) & (df['ff_purchase_to_lead_ratio'] <= 0.2),
        "0.2 < Ratio <= 0.5": (df['ff_purchase_to_lead_ratio'] > 0.2) & (df['ff_purchase_to_lead_ratio'] <= 0.5),
        "0.5 < Ratio <= 1.0": (df['ff_purchase_to_lead_ratio'] > 0.5) & (df['ff_purchase_to_lead_ratio'] <= 1.0),
        "Ratio > 1.0": df['ff_purchase_to_lead_ratio'] > 1.0
    }
    
    # Create a new column for the category
    df['ratio_category'] = 'Other'
    for category, condition in categories.items():
        df.loc[condition, 'ratio_category'] = category
    
    return df

def group_and_analyze(df):
    """Group the data by ratio categories and perform analysis."""
    grouped = df.groupby('ratio_category').agg({
        'ff_purchases': 'sum',
        'ff_leads': 'sum',
        'ff_BRSubmit': 'sum',
        'ff_DMSubmit': 'sum',
        'ff_PhoneGet': 'sum',
        'Clicks': 'sum',
        'Impr.': 'sum',
        'Cost': 'sum',
        'ff_purchase_to_lead_ratio': 'mean'
    }).reset_index()
    
    return grouped

def save_results(df, output_file):
    """Save the results to a CSV file."""
    df.to_csv(output_file, index=False)

def save_search_terms_by_group(df, output_file, categories):
    """Save search terms grouped by specified ratio categories to a CSV file."""
    # Filter the DataFrame for the specified categories
    filtered_df = df[df['ratio_category'].isin(categories)]
    
    # Save the filtered DataFrame
    filtered_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Load the data
    input_file = "output/FINAL_merged_output.csv"
    df = load_data(input_file)

    # Categorize the ratios
    df = categorize_ratios(df)

    # Group and analyze the data
    grouped_df = group_and_analyze(df)

    # Save the results to a new CSV file
    output_file = "output/ratio_analysis_output.csv"
    save_results(grouped_df, output_file)

    # Save search terms by specified ratio categories to another CSV file
    search_term_categories = [
        "0 < Ratio <= 0.1",
        "0.1 < Ratio <= 0.2",
        "0.2 < Ratio <= 0.5",
        "0.5 < Ratio <= 1.0"
    ]
    output_search_terms_file = "output/search_terms_by_group.csv"
    save_search_terms_by_group(df, output_search_terms_file, search_term_categories)

    # Save search terms for the "No Value or Zero" category to another CSV file
    no_value_or_zero_category = ["No Value or Zero"]
    output_no_value_or_zero_file = "output/search_terms_no_value_or_zero.csv"
    save_search_terms_by_group(df, output_no_value_or_zero_file, no_value_or_zero_category)

    print(f"Ratio analysis results have been saved to {output_file}")
    print(f"Search terms grouped by specified ratio categories have been saved to {output_search_terms_file}")
    print(f"Search terms for 'No Value or Zero' category have been saved to {output_no_value_or_zero_file}")
