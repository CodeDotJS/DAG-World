import random
import os
from dotenv import load_dotenv
import asyncio
from flask import Flask, jsonify
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
    return jsonify({'message': 'Unofficial API for Delhi Art Gallery - DAG!'})

async def get_artists_from_db():
    try:
        return list(artists_collection.find({}, {'_id': 0}))
    except PyMongoError as e:
        print(f"Error fetching artists: {e}")
        return []

@app.route('/artists', methods=['GET'])
async def get_artists():
    if 'artists' not in artist_cache:
        artists = await get_artists_from_db()
        artist_cache['artists'] = artists
    return jsonify(artist_cache['artists'])

@app.route('/artists/random', methods=['GET'])
async def get_random_artist():
    if 'artists' not in artist_cache:
        artists = await get_artists_from_db()
        artist_cache['artists'] = artists
    random_artist = random.choice(artist_cache['artists'])
    return jsonify(random_artist)

@app.route('/artists/random/<int:number>', methods=['GET'])
async def get_multiple_random_artists(number):
    if 'artists' not in artist_cache:
        artists = await get_artists_from_db()
        artist_cache['artists'] = artists
    random_artists = random.sample(artist_cache['artists'], min(number, len(artist_cache['artists'])))
    return jsonify(random_artists)

async def get_artist_from_db(artist_name):
    try:
        return artists_collection.find_one({'name': artist_name}, {'_id': 0})
    except PyMongoError as e:
        print(f"Error fetching artist '{artist_name}': {e}")
        return None

@app.route('/artist/<string:artist_name>', methods=['GET'])
async def get_artist(artist_name):
    if artist_name not in artist_cache:
        artist = await get_artist_from_db(artist_name)
        artist_cache[artist_name] = artist
    if artist_cache[artist_name]:
        return jsonify(artist_cache[artist_name])
    else:
        return jsonify({'message': 'Artist not found'}), 404

@app.route('/artist/<string:artist_name>/image', methods=['GET'])
async def get_artist_image(artist_name):
    if artist_name not in artist_cache:
        artist = await get_artist_from_db(artist_name)
        artist_cache[artist_name] = artist
    if artist_cache[artist_name]:
        return jsonify({'image': artist_cache[artist_name].get('image', '')})
    else:
        return jsonify({'message': 'Artist not found'}), 404

@app.route('/artist/<string:artist_name>/artworks', methods=['GET'])
async def get_artist_artworks(artist_name):
    if artist_name not in artist_cache:
        artist = await get_artist_from_db(artist_name)
        artist_cache[artist_name] = artist
    if artist_cache[artist_name]:
        return jsonify(artist_cache[artist_name].get('artworks', []))
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

@app.route('/artists/search/<string:query>', methods=['GET'])
async def search_artists(query):
    query = query.lower()
    try:
        artists = list(artists_collection.find({'$text': {'$search': query}}, {'_id': 0}))
        return jsonify(artists)
    except PyMongoError as e:
        print(f"Error searching for artists with query '{query}': {e}")
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
