from spotipy import Spotify
from dotenv import load_dotenv
from os import getenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv() #loads .env file

#load the various tokens
client_ID=getenv("SPOTIPY_CLIENT_ID")
api_key=getenv("SPOTIPY_CLIENT_SECRET")
redirect_link=getenv("SPOTIPY_REDIRECT_URI")


scope="user-top-read"

spotify = Spotify(auth_manager=SpotifyOAuth(scope=scope))




#get_artist_name implants the user top artists' names into the "artist_name" list

def get_artist_name(limit):
    ''' Adds the artist names to the the list 'artist_name'''
    user_top_artists = spotify.current_user_top_artists(limit=30, offset=0, time_range='short_term')

    artist_name = [artist_name["name"] for artist_name in user_top_artists["items"]]
    return artist_name



