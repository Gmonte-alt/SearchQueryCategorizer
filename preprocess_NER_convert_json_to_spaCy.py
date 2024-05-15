# python preprocess_NER_convert_json_to_spaCy.py -i data/preprocess_NER_json_combined_data.json -o preprocess_NER_output.pickle
# python preprocess_NER_convert_json_to_spaCy.py -i data/preprocess_NER_json_combined_data.json -o preprocess_NER_output.pickle


# Convert json file to spaCy format.
import plac
import logging
import argparse
import sys
import os
import json
import pickle

@plac.annotations(input_file=("Input file", "option", "i", str), output_file=("Output file", "option", "o", str))

def main(input_file=None, output_file=None):
    try:
        training_data = []
        lines=[]
        with open(input_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            data = json.loads(line)
            text = data['content']
            entities = []
            for annotation in data['annotation']:
                point = annotation['points'][0]
                labels = annotation['label']
                if not isinstance(labels, list):
                    labels = [labels]

                for label in labels:
                    entities.append((point['start'], point['end'] + 1 ,label))


            training_data.append((text, {"entities": entities}))

        print(training_data)

        with open(output_file, 'wb') as fp:
            pickle.dump(training_data, fp)

    except Exception as e:
        logging.exception("Unable to process " + input_file + "\n" + "error = " + str(e))
        return None
if __name__ == '__main__':
    plac.call(main)
    
    
# 2nd version

# import plac
# import logging
# import argparse
# import sys
# import os
# import json
# import pickle

# @plac.annotations(input_file=("Input file", "option", "i", str), output_file=("Output file", "option", "o", str))

# def main(input_file=None, output_file=None):
#     try:
#         training_data = []
#         with open(input_file, 'r') as f:
#             for idx, line in enumerate(f, start=1):
#                 try:
#                     data = json.loads(line)
#                     if not isinstance(data, dict):
#                         logging.warning(f"Skipping non-dictionary JSON object on line {idx}")
#                         continue

#                     text = data.get('content', '')  # Use .get() to safely access 'content'
#                     entities = []
#                     for annotation in data.get('annotation', []):  # Use .get() to safely access 'annotation'
#                         point = annotation.get('points', [{'start': 0, 'end': 0}])[0]  # Default to empty point if 'points' is missing
#                         labels = annotation.get('label', [])
#                         if not isinstance(labels, list):
#                             labels = [labels]

#                         for label in labels:
#                             entities.append((point['start'], point['end'] + 1 ,label))

#                     training_data.append((text, {"entities" : entities}))
#                 except json.JSONDecodeError as e:
#                     logging.warning(f"Skipping invalid JSON on line {idx}: {line.strip()}")
#                     continue

#         with open(output_file, 'wb') as fp:
#             pickle.dump(training_data, fp)

#     except Exception as e:
#         logging.exception("Unable to process " + input_file + "\n" + "error = " + str(e))
#         return None

# if __name__ == '__main__':
#     plac.call(main)
