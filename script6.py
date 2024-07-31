import os
import re
import sys

def add_number_to_jsonl_files(input_dir, output_dir):
    # Regular expression to extract number from filename
    number_pattern = re.compile(r'\d+')

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all files in the given directory
    for filename in os.listdir(input_dir):
        # Process only .jsonl files
        if filename.endswith(".jsonl"):
            # Extract number from the filename
            match = number_pattern.search(filename)
            if match:
                number = match.group()
                
                input_file_path = os.path.join(input_dir, filename)
                output_file_path = os.path.join(output_dir, filename)
                
                # Read the original content of the file
                with open(input_file_path, 'r', encoding="utf-8") as file:
                    lines = file.readlines()
                
                # Write the new content with the number after the "text" key
                with open(output_file_path, 'w', encoding="utf-8") as file:
                    for line in lines:
                        # Assuming each line starts with {"text": "
                        if line.startswith('{"text": "'):
                            # Add number after {"text": "
                            modified_line = line.replace('{"text": "', f'{{"text": "No: {number} ', 1)
                            file.write(modified_line)
                        else:
                            file.write(line)
                print(f"Processed file: {filename} with number: {number}")
            else:
                print(f"No number found in filename: {filename}")

def process_file(file_path):
    ################################################# LOADING DATA #################################
    # Add your file processing code here
    
    print(f"Processing {file_path} with Script 1")
    print(file_path)

    # Creating Input folder
    input_dir = file_path

    # Creating Output Folder
    output_dir = "./numbered_jsonl_output"

    add_number_to_jsonl_files(input_dir, output_dir)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("No directory provided")