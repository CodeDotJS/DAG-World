import os
import json

os.makedirs('database', exist_ok=True)

def merge_json_files(directory):
    merged_data = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    merged_data.append(data)
    print("Done!")
    return merged_data


def write_merged_json(data, output_file):
    with open(output_file, 'w') as file:
        for item in data:
            file.write(json.dumps(item, indent=4))
            file.write('\n')

if __name__ == "__main__":
    input_directory = 'Artists'
    output_file = 'database/art.json'

    merged_data = merge_json_files(input_directory)
    write_merged_json(merged_data, output_file)
