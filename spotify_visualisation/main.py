import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

load_dotenv()

CLIENT_ID=os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')   
REDIRECT_URL=os.getenv('REDIRECT_URL')

SCOPE = "user-read-recently-played" 

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret= CLIENT_SECRET, redirect_uri=REDIRECT_URL, scope=SCOPE))

results = sp.current_user_recently_played(limit=10)

for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])