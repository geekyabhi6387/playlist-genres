from flask import Flask, request, jsonify
from flask_cors import CORS
import spotipy
import os
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from collections import Counter
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)  


CLIENT_ID = os.environ["spotify_client_id"]
CLIENT_SECRET = os.environ["spotify_client_secret"]
LASTFM_KEY = os.environ["lastfm_key"]

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def get_genre(track_name, artist_name):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getTopTags",
        "api_key": LASTFM_KEY,
        "artist": artist_name,
        "track": track_name,
        "format": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "toptags" in data and "tag" in data["toptags"] and len(data["toptags"]["tag"]) > 0:
        return data["toptags"]["tag"][0]["name"].lower()  
    
    return "unknown" 

@app.route('/get_playlist_tracks', methods=['GET'])
def get_playlist_tracks():
    playlist_url = request.args.get("playlist_url")
    if not playlist_url:
        return jsonify({"error": "No playlist URL provided"}), 400

   
    try:
        playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
    except IndexError:
        return jsonify({"error": "Invalid playlist URL"}), 400

    results = sp.playlist_tracks(playlist_id)
    tracks = []
    genre_count = Counter()
    
    for item in results["items"]:
        track = item["track"]
        genre = get_genre(track["name"],track["artists"][0]["name"])
        genre_count[genre] += 1

        tracks.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "preview_url": track["preview_url"],
            "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
            "genre": genre
        })

    return jsonify({
        "tracks": tracks,
        "genre_count" : dict(genre_count)            
                    })

if __name__ == '__main__':
    app.run(debug=True)
