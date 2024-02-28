import os
import json
import pandas as pd

base_directory = "Artists"
subdirectories = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

all_artworks_data = []

os.makedirs('database', exist_ok=True)

for subdirectory in subdirectories:
    directory = os.path.join(base_directory, subdirectory)
    if not os.path.isdir(directory):
        continue

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                json_data = json.load(file)

            artist_name = json_data.get('name')

            artworks_data = []
            for artwork in json_data.get('artworks', []):
                artwork_info = {
                    'artist_name': artist_name,
                    'painting': artwork['painting'],
                    'title': artwork['title'],
                    'year': artwork['year'],
                    'medium': artwork['medium']
                }
                artworks_data.append(artwork_info)
            all_artworks_data.extend(artworks_data)

artworks_df = pd.DataFrame(all_artworks_data)
artworks_df.to_csv('database/art.csv', index=False)
print("CSV file has been created successfully.")
