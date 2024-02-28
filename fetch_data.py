import os
import json
import requests
from bs4 import BeautifulSoup
import re

def update_json(file_path):
    with open(file_path, 'r') as file:
        artist_data = json.load(file)

    href = artist_data.get('profile')
    if href:
        response = requests.get(href)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            name_element = soup.find('h4', class_='heading2 text-center text-white mb-0')
            if name_element:
                name = name_element.get_text().strip()
                artist_data['name'] = name

            year_element = soup.find('p', class_='text2 text-center text-white')
            if year_element:
                year = year_element.get_text().strip().replace('\n', '')
                year = ' '.join(year.split())
                artist_data['year'] = year

            intro_element = soup.find('p', class_='text1 text1Heading')
            if intro_element:
                intro = intro_element.get_text().strip()
                artist_data['intro'] = intro

            parent_element = soup.find('div', class_='col-md-6 order-md-1 artistBio customScrollbar1')
            if parent_element:
                bio_elements = parent_element.find_all('p', class_='text1')
                bio = ''
                for element in bio_elements:
                    if element != intro_element:
                        bio += element.get_text().strip() + '\n'
                artist_data['bio'] = bio.strip()

            script_content = response.text
            match_current_product_id = re.search(r'"CurrentProductId"\s*:\s*"(\d+)"', script_content)
            if match_current_product_id:
                artist_data['CurrentProductId'] = match_current_product_id.group(1)

            match_last_art_pro_id = re.search(r'"LastArtProId"\s*:\s*"(\d+)"', script_content)
            if match_last_art_pro_id:
                artist_data['LastArtProId'] = match_last_art_pro_id.group(1)

    with open(file_path, 'w') as file:
        json.dump(artist_data, file, indent=4)

main_directory = 'Artists'

for subdir in os.listdir(main_directory):
    subdirectory = os.path.join(main_directory, subdir)
    if os.path.isdir(subdirectory):
        for filename in os.listdir(subdirectory):
            if filename.endswith('.json'):
                file_path = os.path.join(subdirectory, filename)
                update_json(file_path)
