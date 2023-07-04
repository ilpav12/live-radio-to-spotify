# Automatically add song playing live on an online radio to a Spotify playlist

## Requirements:
- Python 3.10+
- Spotify account

## Installation:
1. Clone this repository
2. Install the requirements with `pip install -r requirements.txt`
3. Create a Spotify application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
4. Create a .env file copying the .env.example file and fill in the required fields
5. Run the script with `python main.py`

## env variables:
- `URL`: The URL of the online radio playing song details e.g. `https://titoli.fluidstream.it/klasseuno/onair_piter.json`
- `PLAYLIST_ID`: The ID of the Spotify playlist where the songs will be added e.g. `5CD1EBQw2qUNNeslfn8UdO`
- `SPOTIPY_CLIENT_ID`: The Client ID of the Spotify application
- `SPOTIPY_CLIENT_SECRET`: The Client Secret of the Spotify application
- `SPOTIPY_REDIRECT_URI`: The Redirect URI of the Spotify application e.g. `http://localhost:8080`
- `MARKET`: The market where the song is available e.g. `IT`
- `DAY_DIFF`: The number of days to filter the songs e.g. `182` (6 months)
