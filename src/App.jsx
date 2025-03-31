import { useState } from "react";
import axios from "axios";

function App() {
  const [playlistUrl, setPlaylistUrl] = useState("");
  const [tracks, setTracks] = useState([]);
  const [genreCounts, setGenreCounts] = useState({});

  const fetchTracks = async () => {
    if (!playlistUrl) return;

    try {
      const response = await axios.get("http://127.0.0.1:5000/get_playlist_tracks", {
        params: { playlist_url: playlistUrl }
      });
      setTracks(response.data.tracks);
      setGenreCounts(response.data.genre_count);
    } catch (error) {
      console.error("Error fetching tracks:", error);
    }
  };

  return (
    <div className="App">
      <div className="InputContainer">
      <h1>Playlist Genres</h1>
      <input
        type="text"
        placeholder="Enter Spotify Playlist URL"
        value={playlistUrl}
        onChange={(e) => setPlaylistUrl(e.target.value)}
      />
      <button onClick={fetchTracks}>Fetch Tracks</button>
      </div>
      
      <ul>
        {tracks.map((track, index) => (
          <li key={index}>
            <img src={track.image} alt={track.name} width="50" />
            <strong>{track.name}</strong> - {track.artist} ({track.genre})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
