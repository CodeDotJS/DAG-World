import os
import json
import requests
from bs4 import BeautifulSoup

def extract_artwork_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    artwork_divs = soup.find_all('div', class_='work-cont')

    artworks = []

    for artwork_div in artwork_divs:
        painting_url = artwork_div.find('img', class_='respImg')['src']
        title = artwork_div.find('p', class_='text1 italic mb-0').get_text().strip()
        medium = artwork_div.find_all('p', class_='text1 mb-0')[1].get_text().strip()

        try:
            year = int(artwork_div.find('p', class_='text1 mb-0').get_text().strip())
        except ValueError:
            year = None

        artwork_data = {
            "painting": painting_url,
            "title": title,
            "year": year,
            "medium": medium
        }

        artworks.append(artwork_data)

    return artworks

def process_artists_data():
    base_folder = "Artists"

    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)

        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)

                if filename.endswith(".json"):
                    with open(file_path, 'r') as file:
                        artist_data = json.load(file)

                    url = "https://dagworld.com/allartworks/index/view/"
                    referer_url = artist_data["profile"]
                    curr_pro_id = artist_data["CurrentProductId"]
                    last_art_pro_id = artist_data["LastArtProId"]

                    headers = {
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "X-Requested-With": "XMLHttpRequest",
                        "Connection": "keep-alive",
                        "Referer": referer_url,
                    }

                    payload = {
                        "currProId": curr_pro_id,
                        "currPage": "1",
                        "lastArtProId": last_art_pro_id
                    }

                    response = requests.post(url, headers=headers, data=payload)
                    html_response = response.json()["output"]

                    artworks = extract_artwork_details(html_response)

                    artist_data["artworks"] = artworks

                    with open(file_path, 'w') as file:
                        json.dump(artist_data, file, indent=4)

                    print(f"Artworks scraped and appended for file: {filename}")

if __name__ == "__main__":
    process_artists_data()
    print("Process completed successfully!")
