from flask import Flask, request, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)  


CLIENT_ID = "7dadeb50c07a4356bb40958f1824260c"
CLIENT_SECRET = "5375a66b6abb4887944011cf1a61d006"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

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
    
    for item in results["items"]:
        track = item["track"]
        tracks.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "preview_url": track["preview_url"],
            "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None
        })

    return jsonify({"tracks": tracks})

if __name__ == '__main__':
    app.run(debug=True)
