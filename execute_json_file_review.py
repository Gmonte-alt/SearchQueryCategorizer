import json

# Path to the JSON file
json_file_path = 'data/preprocess_NER_json_combined_data.json'

# Load JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = file.read()

# Parse the JSON data using json.loads()
data = json.loads(json_data)

# Now 'data' will contain a list of dictionaries, each representing a JSON object from the file
print(data)
