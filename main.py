import os
from time import sleep

import requests
import spotipy
from datetime import datetime
from spotipy.oauth2 import SpotifyOauthError, SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')
playlist_id = os.getenv('PLAYLIST_ID')

while True:
    sleep(60)
    response = requests.get(url)
    data = response.json()

    if not data['trackName'].strip():
        print('There is no song playing at the moment')
        continue

    try:
        spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private"))
    except SpotifyOauthError as e:
        with open("log.txt", "a") as file:
            file.write(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Error authenticating to Spotify: {str(e)}\n')
        raise RuntimeError(f'Error authenticating to Spotify: {e}')

    results = spotify.search(q=f'{data["artistName"]}+{data["trackName"]}', type='track', limit=1,
                             market=os.getenv('MARKET'))

    if not results['tracks']['items']:
        print(f'Song {data["trackName"]} by {data["artistName"]} not found')
        with open("log.txt", "a") as file:
            file.write(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Song {data["trackName"]} '
                       f'by {data["artistName"]} not found\n')
        continue

    match results['tracks']['items'][0]['album']['release_date_precision']:
        case 'day':
            release_date = datetime.strptime(results['tracks']['items'][0]['album']['release_date'], '%Y-%m-%d')
        case 'month':
            release_date = datetime.strptime(results['tracks']['items'][0]['album']['release_date'], '%Y-%m')
        case 'year':
            release_date = datetime.strptime(results['tracks']['items'][0]['album']['release_date'], '%Y')

    if (datetime.now() - release_date).days > int(os.getenv('DAY_DIFF')):
        print(f'Song {data["trackName"]} by {data["artistName"]} is too old')
        continue

    playing_track_id = results['tracks']['items'][0]['id']

    current_playlist_tracks = spotify.playlist(playlist_id)['tracks']['items']
    current_playlist_track_ids = [track['track']['id'] for track in current_playlist_tracks]

    if playing_track_id in current_playlist_track_ids:
        print(f'Song {data["trackName"]} by {data["artistName"]} is already present in the playlist')
        continue

    spotify.playlist_add_items(playlist_id, [playing_track_id])
