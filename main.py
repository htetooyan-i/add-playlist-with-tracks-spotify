import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import os

# Get environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

# user inputs
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
playlist_name = input("Enter a name for your new playlist: ")
playlist_description = input("Enter a description for your new playlist: ")

# request header

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
url = "https://www.billboard.com/charts/hot-100/" + date

# request data and format to html
response = requests.get(url=url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")

# get song names from html
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

# Initialize Spotipy with OAuth
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private user-library-read",
        redirect_uri=redirect_uri,  # Use the variable
        client_id=client_id,         # Use the variable
        client_secret=client_secret, # Use the variable
        show_dialog=True,
        cache_path="token.txt",
        username='i',            # Use the variable
    )
)
user_id = sp.current_user()["id"]

# song urls
song_uris = []

# get year for input date
year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Add songs to the newly created playlist
if song_uris:
    new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False,
                                           description=playlist_description)
    sp.user_playlist_add_tracks(user=user_id, playlist_id=new_playlist['id'], tracks=song_uris)
    print(f"Added {len(song_uris)} songs to the playlist.")