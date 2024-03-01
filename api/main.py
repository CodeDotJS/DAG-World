import os
from dotenv import load_dotenv
import asyncio
from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

load_dotenv()
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri)

db = client["art"]
artists_collection = db['artists']

artists_collection.create_index([('name', 'text')])
artist_cache = {}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

async def get_artists_from_db():
    try:
        return list(artists_collection.find({}, {'_id': 0}))
    except PyMongoError as e:
        print(f"Error fetching artists: {e}")
        return []

@app.route('/artists', methods=['GET'])
async def get_artists():
    artists = await get_artists_from_db()  # Bypass cache and fetch directly from DB
    return jsonify(artists)

@app.route('/artists/random', methods=['GET'])
async def get_random_artist():
    artists = await get_artists_from_db()  # Bypass cache and fetch directly from DB
    random_artist = random.choice(artists)
    return jsonify(random_artist)

@app.route('/artists/random/<int:number>', methods=['GET'])
async def get_multiple_random_artists(number):
    artists = await get_artists_from_db()  # Bypass cache and fetch directly from DB
    random_artists = random.sample(artists, min(number, len(artists)))
    return jsonify(random_artists)

# The following endpoints are modified to bypass the cache
@app.route('/artist/<string:artist_name>/artworks', methods=['GET'])
async def get_artist_artworks(artist_name):
    artist = await get_artist_from_db(artist_name)
    if artist:
        return jsonify(artist.get('artworks', []))
    else:
        return jsonify({'message': 'Artist not found'}), 404

@app.route('/artist/<string:artist_name>/intro', methods=['GET'])
async def get_artist_intro(artist_name):
    artist = await get_artist_from_db(artist_name)
    if artist:
        return jsonify({'intro': artist.get('intro', '')})
    else:
        return jsonify({'message': 'Artist not found'}), 404

@app.route('/artist/<string:artist_name>/bio', methods=['GET'])
async def get_artist_bio(artist_name):
    artist = await get_artist_from_db(artist_name)
    if artist:
        return jsonify({'bio': artist.get('bio', '')})
    else:
        return jsonify({'message': 'Artist not found'}), 404

@app.route('/artist/<string:artist_name>/year', methods=['GET'])
async def get_artist_year(artist_name):
    artist = await get_artist_from_db(artist_name)
    if artist:
        return jsonify({'year': artist.get('year', '')})
    else:
        return jsonify({'message': 'Artist not found'}), 404

async def get_artist_from_db(artist_name):
    try:
        return artists_collection.find_one({'name': artist_name}, {'_id': 0})
    except PyMongoError as e:
        print(f"Error fetching artist '{artist_name}': {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
