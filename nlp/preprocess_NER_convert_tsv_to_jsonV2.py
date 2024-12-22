# 

import json
import logging

def tsv_to_json_format(input_path, output_path, unknown_label):
    try:
        with open(input_path, 'r') as f, open(output_path, 'w', encoding='utf-8') as fp:
            fp.write('[')  # Write the beginning of the JSON array
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
                word_start = start_idx
                word_end = start_idx + len(word) #- 1
                # Append the word to the current sentence with correct start and end indices
                sentence.append({'text': word, 'entity': entity, 'identifier': identifier, 'start': word_start, 'end': word_end})
                # Update the start index for the next word
                start_idx = word_end + 1
            # Handle the last sentence
            if sentence:
                sentences.append(sentence)
              
            # Iterate over each sentence and construct the JSON data
            for i, sent in enumerate(sentences):
                content = ' '.join([word['text'] for word in sent])
                content_start_idx = sent[0]['start']
                content_end_idx = sent[-1]['end']
                data_dict = {
                    "content": content,
                    "annotation": [
                        {
                            "label": [word['entity']],
                            "points": [{
                                "start": word['start'] - content_start_idx,
                                "end": word['end'] - content_start_idx,
                                "text": word['text']
                            }]
                        } for word in sent
                    ]
                }
                # Write the JSON data to the output file
                json.dump(data_dict, fp)
                # Add comma after each JSON data dictionary except for the last one
                if i < len(sentences) - 1:
                    fp.write(',\n')
            fp.write(']')  # Write the end of the JSON array
    except Exception as e:
        logging.exception("Unable to process file" + "\n" + "error = " + str(e))

# Example usage:
tsv_to_json_format("data/preprocess_NER_tsv_combined_data.tsv", 'data/preprocess_NER_json_combined_data.json', 'O')
