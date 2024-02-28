import os
import json

def find_empty_fields(folder_path):
    empty_fields = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if isinstance(value, str) and not value.strip():
                            empty_fields.append(file_path)
                            break

    return empty_fields

def main():
    folder_path = "Artists"
    empty_fields = find_empty_fields(folder_path)
    empty_fields_file_path = "files/empty_fields.json"

    if empty_fields:
        with open(empty_fields_file_path, 'w') as f:
            json.dump(empty_fields, f, indent=4)
        print("Files with empty fields saved to empty_fields.json")
    else:
        if os.path.exists(empty_fields_file_path) and os.path.getsize(empty_fields_file_path) > 0:
            with open(empty_fields_file_path, 'w') as f:
                f.write("")
            print("Empty fields file cleared.")
        else:
            print("No files with empty fields found.")

if __name__ == "__main__":
    main()
