import sys
import os
import json
import re


######### AUX FUNCTIONS ############################################################################################

global summary_success
global summary_fail
global summary_missed_labels

summary_success=""
summary_fail=""
summary_missed_labels=""

def load_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")

def extract_text_and_labels(input_text):

    global summary_fail

    text_match = re.search(r"\[INST\].*?medical record:(.*?)(?=\[/INST\])", input_text, re.DOTALL)
    if not text_match:
        raise ValueError("Text could not be extracted correctly.")
    main_text = text_match.group(1).strip()

    labels_string_match = re.search(r"\[/INST\]\s*(.*)", input_text, re.DOTALL)
    if not labels_string_match:
        raise ValueError("Labels could not be extracted correctly.")
    json_labels_string = labels_string_match.group(1).strip()

    # Clean up the JSON string
    json_labels_string = json_labels_string.replace("'", '"').strip()
    json_labels_string = json_labels_string.lstrip('.').strip()  # Remove leading periods and extra spaces

    #print(f"JSON string: {json_labels_string}")  # Log the JSON string for debugging

    try:
        labels = json.loads(json_labels_string)
    except json.JSONDecodeError as e:
        summary_fail+=f"Failed to decode JSON: {e}\n"
        print(f"Failed to decode JSON: {e}")
        return main_text, {}

    return main_text, labels

def find_offsets(text, label, entity_type):
    global summary_missed_labels
    start = text.find(label)
    if start == -1:
        print(f"The label '{label}' was not found, skipping...")
        summary_missed_labels+=f"The label '{label}' was not found, skipping...\n"
        return None
    end = start + len(label)
    return {
        'type': entity_type,
        'start_offset': start,
        'end_offset': end
    }

def process_labels(text, original_labels):
    corrected_labels = {'text': text, 'label': []}
    for entity_type, entities in original_labels.items():
        for entity in entities:
            label_text = entity['type']
            corrected_entity = find_offsets(text, label_text, entity_type)
            if corrected_entity:
                corrected_labels['label'].append(
                    [corrected_entity['start_offset'], corrected_entity['end_offset'], entity_type]
                )
    return corrected_labels


def write_summaries_to_files():
    global summary_success
    global summary_fail
    global summary_missed_labels

    # Create the 'summaries' directory to store the output files
    output_dir = "./ai/summaries"
    os.makedirs(output_dir, exist_ok=True)
    
    # Write summary_success to file
    with open(os.path.join(output_dir, "summary_success.txt"), 'w', encoding='utf-8') as file:
        file.write(summary_success)
    
    # Write summary_fail to file
    with open(os.path.join(output_dir, "summary_fail.txt"), 'w', encoding='utf-8') as file:
        file.write(summary_fail)
    
    # Write summary_missed_labels to file
    with open(os.path.join(output_dir, "summary_missed_labels.txt"), 'w', encoding='utf-8') as file:
        file.write(summary_missed_labels)
    
    print("Summaries have been written to files.")


# Main processing function
def process_files_in_folder(folder_path):
    global summary_success
    global summary_fail
    global summary_missed_labels
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            input_text = load_text_file(file_path)
            print(f"Processing {file_name}...")
            summary_fail+=f"Processing {file_name}...\n"
            summary_missed_labels+=f"Processing {file_name}...\n"
            if input_text:
                try:
                    text, original_labels = extract_text_and_labels(input_text)
                    corrected_labels = process_labels(text, original_labels)

                    output_file_path = file_path + '.jsonl'
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write(json.dumps(corrected_labels, ensure_ascii=False) + '\n')
                    print(f"Processed {file_name} and saved to {output_file_path}")
                    summary_success+=f"Processed {file_name} and saved to {output_file_path}\n"
                except ValueError as ve:
                    print(f"ValueError: {ve} in file {file_name}")
                except Exception as e:
                    print(f"An error occurred while processing {file_name}: {e}")
    write_summaries_to_files()
######### AUX FUNCTIONS ############################################################################################


######## MAIN FUNCTION ############################################################################################


def process_file(file_path):
    # Add your file processing code here
    print(f"Processing {file_path} with Script 1")

    ### TEST TSV TO TXT FILES ####################################
    # Define the path to the test set
    test_set_path = file_path

    # Create the 'ai' directory to store the output files
    output_dir = "./ai"

    os.makedirs(output_dir, exist_ok=True)

    # Read the test_set.tsv file and write each line to a separate file
    with open(test_set_path, 'r', encoding='utf-8') as file:
        for idx, line in enumerate(file, start=1):
            # Find the position of the [INST] tag
            inst_start_index = line.find('[INST]')
            if inst_start_index != -1:
                # Find the position of the [/INST] tag
                inst_end_index = line.find('[/INST]', inst_start_index)
                if inst_end_index != -1:
                    # Extract everything between [INST] and [/INST] including [/INST]
                    prefix = line[inst_start_index + len('[INST]'):inst_end_index + len('[/INST]')]
                    # Find the first occurrence of '{' after [/INST]
                    json_start_index = line.find('{', inst_end_index + len('[/INST]'))
                    if json_start_index != -1:
                        # Extract the JSON data starting from the first '{'
                        json_data = line[json_start_index:]
                        # Remove anything after }]} if it exists
                        json_data = json_data.split("}]}")[0] + "}]} \n"  # Split at }]}, keep first part and add newline
                        # Combine the prefix and JSON data with a space in between
                        final_output = "[INST] "+prefix.strip() + ' ' + json_data.strip()
                        output_file_path = os.path.join(output_dir, f"ai_{idx}.txt")
                        with open(output_file_path, 'w', encoding='utf-8') as output_file:
                            output_file.write(final_output)
                    else:
                        # Handle cases where '{' is not found after [/INST]
                        print(f"No JSON found in line {idx}")
                else:
                    # Handle cases where [/INST] is not found after [INST]
                    print(f"[/INST] not found in line {idx}")
            else:
                # Handle cases where [INST] is not found
                print(f"[INST] not found in line {idx}")

    print(f"Processed {idx} lines. Output files are saved in {output_dir}.")

    process_files_in_folder(output_dir)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("No file provided")
