# python preprocess_NER_convert_json_to_spacyV2.py -i data/preprocess_NER_json_combined_data.json -o preprocess_NER_output.pickle

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
        
        with open(input_file, 'r') as f:
            data = json.load(f)
            
            for item in data:
                text = item['content']
                entities = []
                for annotation in item['annotation']:
                    point = annotation['points'][0]
                    labels = annotation['label']
                    if not isinstance(labels, list):
                        labels = [labels]

                    for label in labels:
                        entities.append((point['start'], point['end'] + 1, label))

                training_data.append((text, {"entities": entities}))
                
            print(type(training_data))

        with open(output_file, 'wb') as fp:
            pickle.dump(training_data, fp)

    except Exception as e:
        logging.exception("Unable to process " + input_file + "\n" + "error = " + str(e))
        return None

if __name__ == '__main__':
    plac.call(main)
