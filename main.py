import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

# export as ENV vars
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''

# Spotify auth manager
auth_manager = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
                            scope="playlist-modify-private", redirect_uri="http://example.com")
spotify = spotipy.Spotify(auth_manager=auth_manager)

BASE_URL = 'https://www.billboard.com/charts/hot-100/'
date = input("Which year do you want to travel to (YYYY-MM-DD)?\n")

response = requests.get(BASE_URL + date)

soup = BeautifulSoup(response.text, 'html.parser')

items = soup.select('.o-chart-results-list-row')
titles = [item.find('h3').get_text().strip('\n\t') for item in items]

user_id = spotify.current_user()['id']


def get_song_id(track):
    year = 2004
    try:
        song = spotify.search(q=f"track:{track} year:{year}")
        return song['tracks']['items'][0]['id']
    except IndexError:
        return False


song_ids = []
for title in titles:
    result = get_song_id(title)
    if result:
        song_ids.append(result)

# playlist_create_result = spotify.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# pprint(playlist_create_result)
playlist_id = ''

tracks_to_add = [f"spotify:track:{id}" for id in song_ids]
spotify.playlist_add_items(playlist_id=playlist_id, items=tracks_to_add)
