import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

def process_file(file_path):
    # Add your file processing code here
    
    print(f"Processing {file_path} with Script 1")
    print(file_path)

    # Creating Input folder
    input_dir = file_path

    # Creating Output Folder
    output_dir = "./markup_output"
    os.makedirs(output_dir, exist_ok=True)

    process_jsonl_folder(input_dir, output_dir)


def adjust_offsets(labels):
    adjusted_labels = []
    for start, end, label_type in labels:
        adjusted_labels.append([start, end, label_type])
    return adjusted_labels

def apply_markup(text, labels):
    labeled_text = []
    last_index = 0
    
    for start, end, label_type in sorted(labels, key=lambda x: x[0]):
        labeled_text.append(text[last_index:start])
        labeled_text.append(f'<{label_type}>')
        labeled_text.append(text[start:end])
        labeled_text.append(f'</{label_type}>')
        last_index = end
    
    labeled_text.append(text[last_index:])
    return ''.join(labeled_text)

def transform_record(record):
    text = record['text']
    labels = adjust_offsets(record['label'])
    
    marked_up_text = apply_markup(text, labels)
    
    transformed_record = {
        "input": text,
        "marked_up_text": marked_up_text,
        "output": labels
    }
    
    return transformed_record

def process_jsonl_file(input_file, output_dir):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        record = json.loads(line.strip())
        
        # Debug: Print record before processing
        print(f"Processing record: {record}")
        
        # Remove the "Comments" key if it exists
        if "Comments" in record:
            del record["Comments"]

        transformed_record = transform_record(record)

        # Use the input file name to create an output file name
        input_file_name = os.path.basename(input_file)
        output_file = os.path.join(output_dir, f'{input_file_name}.txt')
        
        # Debug: Print output file path
        print(f"Writing to output file: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as out_f:
            out_f.write(transformed_record['marked_up_text'] + '\n')

def process_jsonl_folder(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.jsonl'):
            input_file = os.path.join(input_dir, file_name)
            process_jsonl_file(input_file, output_dir)




if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("No file provided")
