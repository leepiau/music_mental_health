import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# API access credentials
os.environ['SPOTIPY_CLIENT_ID'] = '7c6d0e7c43904c28a29047f947d55951'
os.environ['SPOTIPY_CLIENT_SECRET'] = '277304c85fa442059e887b5222581aba'
#export SPOTIPY_CLIENT_ID='7c6d0e7c43904c28a29047f947d55951'
#export SPOTIPY_CLIENT_SECRET='277304c85fa442059e887b5222581aba'

# Authentication
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

auth_url = 'https://accounts.spotify.com/api/token'
data = {
    'grant_type': 'client_credentials',
    'client_id': os.environ['SPOTIPY_CLIENT_ID'],
    'client_secret': os.environ['SPOTIPY_CLIENT_SECRET'],
}
"""
auth_response = requests.post(auth_url, data=data)
access_token = auth_response.json().get('access_token')
headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}
"""

# List of genres
genre_list = sp.recommendation_genre_seeds()

# Featured playlists of Singapore
sg_feat_playlists = sp.featured_playlists(locale=None, country='SG', timestamp=None, limit=20, offset=0)
print(sg_feat_playlists)

### Categories in Singapore
# Popular categories in Singapore
categories = sp.categories('Singapore')
sg_categories = {}
for i in range(len(categories['categories'])):
    sg_categories[categories['categories']['items'][i]['name']] = (categories['categories']['items'][i]['id'])

# Playlists for above categories.
seed_genres
for cat, cat_id in sg_categories.items():
    if cat in genre_list:

    category_playlists = sp.category_playlists(cat_id, country='SG')
    print(category_playlists)

# Must select more than one genre.
country_songs = sp.recommendations(seed_genres=["country", "acoustic"])
print(country_songs)


"""
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
"""