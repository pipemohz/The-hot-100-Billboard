from spotipy.oauth2 import SpotifyOAuth
import spotipy
from bs4 import BeautifulSoup
import requests
import os

#You need to declare env variables with your spotify developer account credentials. Create one in https://developer.spotify.com/

SPOTIPY_CLIENT_ID =  os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")


#Get this data in your spotify user account. https://www.spotify.com/us/account/overview/
USER_ID = os.getenv("SPOTIFY_USER_ID")

URL = "https://www.billboard.com/charts/hot-100/"
date = input(
    'Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')
url_query = f"{URL}{date}"


soup = BeautifulSoup(requests.get(url=url_query).text, "html.parser")

span_title = soup.find_all(
    name="span", class_="chart-element__information__song text--truncate color--primary")

span_artist = soup.find_all(
    name="span", class_="chart-element__information__artist text--truncate color--secondary")

songs = {span_title[i].getText(): span_artist[i].getText()
         for i in range(len(span_title))}

scope = "playlist-modify-private"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                     client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, cache_path="token.txt", scope=scope))


track_list = []

for title in songs:
    try:
        sp.search(title, limit=5)['tracks']['items'][0]
    except IndexError:
        pass
    else:
        results = sp.search(title, limit=5)['tracks']['items']
        for item in results:
            if songs[title].lower() in item['artists'][0]['name'].lower() and title.lower() in item['name'].lower():
                track_list.append(item['uri'])
                break

playlist_id = sp.user_playlist_create(
    USER_ID, f"{date} Top Billboard 100", public=False)['id']

sp.user_playlist_add_tracks(USER_ID, playlist_id, track_list)
