import os
import sys
import pandas as pd
import numpy as np
import pandas as pd
from datetime import datetime
import calendar
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from bs4 import BeautifulSoup

def process_markup_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        clean_text = soup.get_text()
        labels = []

        for tag in soup.find_all():
            tag_text = tag.get_text()
            start = clean_text.find(tag_text)
            end = start + len(tag_text)
            labels.append([start, end, tag.name.upper()])

        return {"text": clean_text, "label": labels}

def process_markup_folder(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.txt'):
            input_file = os.path.join(input_dir, file_name)
            try:
                converted_record = process_markup_file(input_file)

                output_file_name = f'{os.path.splitext(file_name)[0]}.jsonl'
                output_file = os.path.join(output_dir, output_file_name)

                with open(output_file, 'w', encoding='utf-8') as out_f:
                    json_record = json.dumps(converted_record, ensure_ascii=False)
                    out_f.write(json_record + '\n')

                print(f"Processed and saved: {output_file}")
            except FileNotFoundError:
                print(f"File {input_file} not found, skipping.")
            except Exception as e:
                print(f"An error occurred while processing file {input_file}: {e}")




def process_file(file_path):
    ################################################# LOADING DATA #################################
    # Add your file processing code here
    
    print(f"Processing {file_path} with Script 1")
    print(file_path)

    # Creating Input folder
    input_dir = file_path

    # Creating Output Folder
    output_dir = "./jsonl_output"
    os.makedirs(output_dir, exist_ok=True)

    process_markup_folder(input_dir, output_dir)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("No file provided")
