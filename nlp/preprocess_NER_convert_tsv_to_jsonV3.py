# preprocess_NER_convert_tsv_to_jsonV3.py

import json
import logging

def tsv_to_json_format(input_path, output_path, unknown_label):
    try:
        with open(input_path, 'r') as f, open(output_path, 'w', encoding='utf-8') as fp:
            to_send_to_json_DATA = []  # List to store data in JSON format
            next(f)  # Skip header row
            sentences = []  # List to store individual sentences
            sentence = []  # List to store words in a sentence
            start_idx = 0  # Initialize start index for each sentence
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) != 3:
                    continue  # Skip malformed lines
                word, entity, identifier = parts
                if word == '.':
                    if sentence:  # If sentence is not empty
                        # Calculate the end index of the sentence
                        end_idx = start_idx + len(sentence) - 1
                        # Append the sentence to the list of sentences
                        sentences.append(sentence)
                        # Reset the sentence list
                        sentence = []
                        # Update the start index for the next sentence
                        start_idx = end_idx + 2
                    continue
                # Append the word to the current sentence with correct start and end indices
                word_start = start_idx
                word_end = start_idx + len(word)
                sentence.append({'text': word, 'entity': entity, 'identifier': identifier, 'start': word_start, 'end': word_end})
                # Update the start index for the next word
                start_idx += len(word) + 1
            # Handle the last sentence
            if sentence:
                sentences.append(sentence)
              
            # Iterate over each sentence and construct the JSON data
            for sent in sentences:
                content = ' '.join([word['text'] for word in sent])
                entities = []
                for word in sent:
                    word_start = word['start'] - sent[0]['start']
                    word_end = word['end'] - sent[0]['start']
                    entities.append((word_start, word_end, word['entity']))
                data_dict = (content, {"entities": entities})
                to_send_to_json_DATA.append(data_dict)
                
            # Write the JSON data to the output file
            json.dump(to_send_to_json_DATA, fp)
            
    except Exception as e:
        logging.exception("Unable to process file" + "\n" + "error = " + str(e))

# Example usage:
tsv_to_json_format("data/preprocess_NER_tsv_combined_data.tsv", 'data/preprocess_NER_json_combined_data.json', 'O')
