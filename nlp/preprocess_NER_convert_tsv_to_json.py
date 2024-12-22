# https://towardsdatascience.com/custom-named-entity-recognition-using-spacy-7140ebbb3718

# Convert .tsv file to dataturks json format. 

# import json
# import logging


# def tsv_to_json_format(input_path, output_path, unknown_label):
#     try:
#         with open(input_path, 'r') as f, open(output_path, 'w') as fp:
#             next(f)  # Skip header row
#             data_dict = {}
#             annotations = []
#             label_dict = {}
#             s = ''
#             start = 0
#             for line in f:
#                 parts = line.strip().split('\t')
#                 if len(parts) != 3:
#                     continue  # Skip malformed lines
#                 word, entity, identifier = parts
#                 s += word + " "
#                 entity = entity[:len(entity) - 1]
#                 if entity != unknown_label:
#                     if len(entity) != 1:
#                         d = {'text': word, 'start': start, 'end': start + len(word) - 1, 'entity': entity}
#                         try:
#                             label_dict[identifier].append(d)
#                         except KeyError:
#                             label_dict[identifier] = [d]
#                 start += len(word) + 1
#             data_dict['content'] = s
#             s = ''
#             for ident, entities in label_dict.items():
#                 label_list = []
#                 for ent in entities:
#                     label_list.append({'label': [ent['entity']], 'points': [ent]})
#                 annotations.extend(label_list)
#             data_dict['annotation'] = annotations
#             json.dump(data_dict, fp)
#             fp.write('\n')
#     except Exception as e:
#         logging.exception("Unable to process file" + "\n" + "error = " + str(e))

# tsv_to_json_format("data/preprocess_NER_tsv_combined_data.tsv", 'data/preprocess_NER_json_combined_data.json', 'O')



# second version

# import json
# import logging

# def tsv_to_json_format(input_path, output_path, unknown_label):
#     try:
#         with open(input_path, 'r') as f, open(output_path, 'w') as fp:
#             next(f)  # Skip header row
#             data_dict = {}
#             annotations = []
#             label_dict = {}
#             sentences = []  # List to store individual sentences
#             sentence = []  # List to store words in a sentence
#             for line in f:
#                 parts = line.strip().split('\t')
#                 if len(parts) != 3:
#                     continue  # Skip malformed lines
#                 word, entity, identifier = parts
#                 if word == '.':
#                     if sentence:  # If sentence is not empty
#                         sentences.append(sentence)
#                         sentence = []  # Reset sentence list
#                     continue
#                 sentence.append({'text': word, 'entity': entity, 'identifier': identifier})
#             # Handle the last sentence
#             if sentence:
#                 sentences.append(sentence)
#             for idx, sent in enumerate(sentences):
#                 data_dict['content'] = ' '.join([word['text'] for word in sent])
#                 data_dict['annotation'] = [{'label': [word['entity']], 'points': [word]} for word in sent]
#                 json.dump(data_dict, fp)
#                 fp.write('\n')
#     except Exception as e:
#         logging.exception("Unable to process file" + "\n" + "error = " + str(e))

# tsv_to_json_format("data/preprocess_NER_tsv_combined_data.tsv", 'data/preprocess_NER_json_combined_data.json', 'O')



# 3rd version

# import json
# import logging

# def tsv_to_json_format(input_path, output_path, unknown_label):
#     try:
#         with open(input_path, 'r') as f, open(output_path, 'w') as fp:
#             next(f)  # Skip header row
#             data_dict = {}
#             sentences = []  # List to store individual sentences
#             sentence = []  # List to store words in a sentence
#             start_idx = 0  # Initialize start index for each sentence
#             for line in f:
#                 parts = line.strip().split('\t')
#                 if len(parts) != 3:
#                     continue  # Skip malformed lines
#                 word, entity, identifier = parts
#                 if word == '.':
#                     if sentence:  # If sentence is not empty
#                         end_idx = start_idx + len(sentence) - 1
#                         sentences.append(sentence)
#                         sentence = []  # Reset sentence list
#                         start_idx = end_idx + 2  # Move start index to next sentence
#                     continue
#                 sentence.append({'text': word, 'entity': entity, 'identifier': identifier, 'start': start_idx, 'end': start_idx + len(word) - 1})
#             # Handle the last sentence
#             if sentence:
#                 end_idx = start_idx + len(sentence) - 1
#                 sentences.append(sentence)
#             for sent in sentences:
#                 data_dict = {
#                     "content": ' '.join([word['text'] for word in sent]),
#                     "annotation": [
#                         {
#                             "label": [word['entity']],
#                             "points": [{
#                                 "start": word['start'],
#                                 "end": word['end'],
#                                 "text": word['text']
#                             }]
#                         } for word in sent
#                     ]
#                 }
#                 json.dump(data_dict, fp)
#                 fp.write('\n')
#     except Exception as e:
#         logging.exception("Unable to process file" + "\n" + "error = " + str(e))

# tsv_to_json_format("data/preprocess_NER_tsv_combined_data.tsv", 'data/preprocess_NER_json_combined_data.json', 'O')



# 4th version - the previous version was not start & ending the values correctly. This version corrects that.

# import json
# import logging

# def tsv_to_json_format(input_path, output_path, unknown_label):
#     try:
#         with open(input_path, 'r') as f, open(output_path, 'w') as fp:
#             next(f)  # Skip header row
#             data_dict = {}
#             sentences = []  # List to store individual sentences
#             sentence = []  # List to store words in a sentence
#             start_idx = 0  # Initialize start index for each sentence
#             for line in f:
#                 parts = line.strip().split('\t')
#                 if len(parts) != 3:
#                     continue  # Skip malformed lines
#                 word, entity, identifier = parts
#                 if word == '.':
#                     if sentence:  # If sentence is not empty
#                         # Calculate the end index of the sentence
#                         end_idx = start_idx + len(sentence) -1
#                         # Append the sentence to the list of sentences
#                         sentences.append(sentence)
#                         # Reset the sentence list
#                         sentence = []
#                         # Update the start index for the next sentence
#                         start_idx = end_idx + 2
#                     continue
#                 word_start = start_idx
#                 word_end = start_idx + len(word) - 1
#                 # Append the word to the current sentence with correct start and end indices
#                 sentence.append({'text': word, 'entity': entity, 'identifier': identifier, 'start': word_start, 'end': word_end})
#                 # Update the start index for the next word
#                 start_idx = word_end + 1

#             # Handle the last sentence
#             if sentence:
#                 sentences.append(sentence)
#             # Iterate over each sentence and construct the JSON data
#             for sent in sentences:
#                 content = ' '.join([word['text'] for word in sent])
#                 content_start_idx = 0
#                 content_end_idx = 0
#                 data_dict = {
#                     "content": content, #' '.join([word['text'] for word in sent]),
#                     "annotation": [
#                         {
#                             "label": [word['entity']],
#                             "points": [{
#                                 "start": content_start_idx, # [word['start']], #word['start'] - start_sent,
#                                 "end": content_end_idx + len(word['text']) -1, # word['end'], #end_sent + len(word['text']) -1, #word['end'] - end_sent,
#                                 "text": word['text']
#                             }]
#                         } for word in sent
#                     ]
#                 }
#                 for annotation in data_dict['annotation']:
#                     start_word = annotation['points'][0]['start']
#                     end_word = annotation['points'][0]['end']
#                     annotation['points'][0]['start'] = start_word
#                     annotation['points'][0]['end'] = end_word
#                     content_end_idx = end_word + 2 # Move end index to the next word accounting for spaces
#                 # Write the JSON data to the output file
#                 json.dump(data_dict, fp)
#                 fp.write('\n')
#     except Exception as e:
#         logging.exception("Unable to process file" + "\n" + "error = " + str(e))

# # Example usage:
# tsv_to_json_format("data/preprocess_NER_tsv_combined_data.tsv", 'data/preprocess_NER_json_combined_data.json', 'O')



# 5th version of the code best version with corrected token values

import json
import logging

def tsv_to_json_format(input_path, output_path, unknown_label):
    try:
        with open(input_path, 'r') as f, open(output_path, 'w') as fp:
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
            for sent in sentences:
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
                fp.write('\n')
    except Exception as e:
        logging.exception("Unable to process file" + "\n" + "error = " + str(e))

# Example usage:
tsv_to_json_format("data/preprocess_NER_tsv_combined_data.tsv", 'data/preprocess_NER_json_combined_data.json', 'O')



# 6th version - the previous version had incorrect json format

# import json
# import logging

# def tsv_to_json_format(input_path, output_path, unknown_label):
#     try:
#         with open(input_path, 'r') as f, open(output_path, 'w') as fp:
#             next(f)  # Skip header row
#             sentences = []  # List to store individual sentences
#             sentence = []  # List to store words in a sentence
#             start_idx = 0  # Initialize start index for each sentence
#             for line in f:
#                 parts = line.strip().split('\t')
#                 if len(parts) != 3:
#                     continue  # Skip malformed lines
#                 word, entity, identifier = parts
#                 if word == '.':
#                     if sentence:  # If sentence is not empty
#                         # Calculate the end index of the sentence
#                         end_idx = start_idx + len(sentence) - 1
#                         # Append the sentence to the list of sentences
#                         sentences.append(sentence)
#                         # Reset the sentence list
#                         sentence = []
#                         # Update the start index for the next sentence
#                         start_idx = end_idx + 2
#                     continue
#                 word_start = start_idx
#                 word_end = start_idx + len(word) #- 1
#                 # Append the word to the current sentence with correct start and end indices
#                 sentence.append({'text': word, 'entity': entity, 'identifier': identifier, 'start': word_start, 'end': word_end})
#                 # Update the start index for the next word
#                 start_idx = word_end + 1

#             # Handle the last sentence
#             if sentence:
#                 sentences.append(sentence)
                
#             # Iterate over each sentence and construct the JSON data
#             fp.write('[')  # Start of the JSON array
#             for idx, sent in enumerate(sentences):
#                 content = ' '.join([word['text'] for word in sent])
#                 content_start_idx = sent[0]['start']
#                 content_end_idx = sent[-1]['end']
#                 data_dict = {
#                     "content": content,
#                     "annotation": [
#                         {
#                             "label": [word['entity']],
#                             "points": [{
#                                 "start": word['start'] - content_start_idx,
#                                 "end": word['end'] - content_start_idx,
#                                 "text": word['text']
#                             }]
#                         } for word in sent
#                     ]
#                 }
#                 # Write the JSON data to the output file
#                 if idx > 0:
#                     fp.write(',')  # Separate JSON objects by comma
#                 json.dump(data_dict, fp)
#             fp.write(']')  # End of the JSON array
#     except Exception as e:
#         logging.exception("Unable to process file" + "\n" + "error = " + str(e))

# # Example usage:
# tsv_to_json_format("data/preprocess_NER_tsv_combined_data.tsv", 'data/preprocess_NER_json_combined_data.json', 'O')
