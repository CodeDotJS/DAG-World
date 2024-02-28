import os
import json

def reorder_keys(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    json_data = json.load(f)

                json_data = {
                    "name": json_data.get("name"),
                    "year": json_data.get("year"),
                    "intro": json_data.get("intro"),
                    "bio": json_data.get("bio"),
                    "CurrentProductId": json_data.get("CurrentProductId"),
                    "LastArtProId": json_data.get("LastArtProId"),
                    "profile": json_data.get("profile"),
                    "image": json_data.get("image"),
                    "artworks": json_data.get("artworks")
                }

                with open(file_path, 'w') as f:
                    json.dump(json_data, f, indent=4)

def main():
    folder = "Artists/"
    reorder_keys(folder)

if __name__ == "__main__":
    main()
