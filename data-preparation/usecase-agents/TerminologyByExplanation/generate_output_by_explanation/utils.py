import os
import json

def save_output_as_json(data, file_name):
    # Prepare the output directory
    output_dir = "../output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the output file path
    output_file_path = os.path.join(output_dir, file_name)

    # Save the word_tree to a file
    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent=2)

    print(f"Word tree saved to {output_file_path}")