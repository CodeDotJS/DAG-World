import os
import requests
from bs4 import BeautifulSoup
import json
import string

base_url = "https://dagworld.com//artist/index/view"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    "Connection": "keep-alive",
    'Referer': 'https://dagworld.com/artists.html',
}

main_folder = "Artists"
os.makedirs(main_folder, exist_ok=True)

for char in string.ascii_uppercase:
    payload = {'category[]': ord(char)}

    response = requests.post(base_url, data=payload, headers=headers)

    if response.ok:
        json_data = response.json()
        html_content = json_data['output']

        soup = BeautifulSoup(html_content, 'html.parser')
        artist_links = soup.find_all('a', class_='artistLink')

        char_folder = os.path.join(main_folder, char)
        os.makedirs(char_folder, exist_ok=True)

        for link in artist_links:
            href = link['href']
            data_img = link['data-img']
            data_artist = link['data-artist']

            artist_json = {
                "profile": href,
                "image": data_img
            }

            file_name = f"{data_artist.replace(' ', '_')}_Artist.json"
            file_path = os.path.join(char_folder, file_name)

            with open(file_path, 'w') as f:
                json.dump(artist_json, f, indent=4)

        print(f"Saved data for character '{char}' in folder '{char_folder}'")
    else:
        print(f"Failed to retrieve data for character '{char}'. Status code:", response.status_code)
