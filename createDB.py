import os
import sqlite3
import json

os.makedirs('database', exist_ok=True)
conn = sqlite3.connect('database/art.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Artist (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   year TEXT,
                   intro TEXT,
                   bio TEXT,
                   CurrentProductId TEXT,
                   LastArtProId TEXT,
                   profile TEXT,
                   image TEXT
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Artwork (
                   id INTEGER PRIMARY KEY,
                   artist_id INTEGER,
                   painting TEXT,
                   title TEXT,
                   year INTEGER,
                   medium TEXT,
                   FOREIGN KEY (artist_id) REFERENCES Artist(id)
               )''')

def insert_data(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path) as f:
                    data = json.load(f)
                    artist_data = (data['name'], data['year'], data['intro'], data['bio'], data['CurrentProductId'], data['LastArtProId'], data['profile'], data['image'])
                    cursor.execute("INSERT INTO Artist (name, year, intro, bio, CurrentProductId, LastArtProId, profile, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", artist_data)
                    artist_id = cursor.lastrowid
                    artworks_data = [(artist_id, artwork['painting'], artwork['title'], artwork['year'], artwork['medium']) for artwork in data['artworks']]
                    cursor.executemany("INSERT INTO Artwork (artist_id, painting, title, year, medium) VALUES (?, ?, ?, ?, ?)", artworks_data)

for folder in range(ord('A'), ord('Z')+1):
    folder_path = os.path.join('Artists', chr(folder))
    if os.path.exists(folder_path):
        insert_data(folder_path)

print('DONE!')

conn.commit()
conn.close()
