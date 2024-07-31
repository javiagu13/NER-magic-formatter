import sys

def process_file(file_path):
    # Add your file processing code here
    print(f"Processing {file_path} with Script 1")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("No file provided")
