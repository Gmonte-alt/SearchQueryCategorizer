import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

nlp = spacy.blank("en") # load a new spacy model
db = DocBin() # create a DocBin object

json_file = ('data/preprocess_NER_json_combined_data.json')

# import json
# f = open(json_file)
# TRAIN_DATA = json.load(f)

# print(TRAIN_DATA)

import json

# Open the JSON file and read its contents
with open(json_file, 'r') as f:
    json_data = f.read()

# Parse the JSON data using json.loads()
TRAIN_DATA = json.loads(json_data)
#print(TRAIN_DATA)

# for text, annot in tqdm(TRAIN_DATA['annotations']):
#     doc = nlp.make_doc(text)
#     ents = []
#     for start, end, label in annot["entities"]:
#         span = doc.char_span(start, end, label=label, alignment_mode="contract")
#         if span is None:
#             print("Skipping entity")
#         else:
#             ents_append(span)
#     doc.ents = entsdb.add(doc)
    
# Iterate over each dictionary in TRAIN_DATA
for data in tqdm(TRAIN_DATA):
    # Access the 'annotations' key of each dictionary
    annotations = data.get('annotations')
    if annotations is not None:  # Check if 'annotations' key exists
        # Iterate over each item in the 'annotations' list
        for text, annot in annotations:
            # Process text and annotation here
            doc = nlp.make_doc(text)
            ents = []
            for start, end, label in annot["entities"]:
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
                if span is None:
                    print("Skipping entity")
                else:
                    ents_append(span)
            pass  # Placeholder for actual processing
    else:
        print("'annotations' key not found in data:", data)
    
db.to_disk("./pvr_training_data.spacy") #save the docbin object