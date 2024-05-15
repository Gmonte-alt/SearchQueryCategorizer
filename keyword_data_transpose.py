# keyword_data_transpose.copy()
# the goal of the script is to take each search query from the training data & split each keyword into a row for each word. 
# Each new transposed keyword will complete with a tailing "." in order to inform the model in the next few steps to use
# that period as a signal to begin a new keyword. A new column, "bio_tag", is created with default values of "O".
# this next section will be the other manual part to this project. 

import pandas as pd

# Read the CSV file
df = pd.read_csv('data/keyword_data_training-kw_only.csv') # keywords.csv')

# Initialize an empty list to store the rows
rows = []

# Iterate over each keyword
for keyword in df['keyword']:
    # Split the keyword into individual words
    words = keyword.split()
    
    # Iterate over each word and add it as a row
    for word in words:
        # Append the word and 'O' to indicate no special tag
        rows.append([word, 'O'])
    
    # Add a period after each keyword
    rows.append(['.', 'O'])

# Create a DataFrame from the list of rows
result = pd.DataFrame(rows, columns=['word', 'bio_tag'])

# Save the result to a new CSV file
result.to_csv('data/keyword_data_training-kw_only_transposed.csv', index=False) # output_keywords_with_period.csv'

print("Keywords transposed successfully with period added!")
