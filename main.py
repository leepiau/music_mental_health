import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import psycopg2

# API access credentials
os.environ['SPOTIPY_CLIENT_ID'] = '7c6d0e7c43904c28a29047f947d55951'
os.environ['SPOTIPY_CLIENT_SECRET'] = '277304c85fa442059e887b5222581aba'

# Authentication
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

auth_url = 'https://accounts.spotify.com/api/token'
data = {
    'grant_type': 'client_credentials',
    'client_id': os.environ['SPOTIPY_CLIENT_ID'],
    'client_secret': os.environ['SPOTIPY_CLIENT_SECRET'],
}

# Import genre list from mental health CSV
mmhcsv = pd.read_csv("C:/Users/Clinton/Desktop/Python/Spotify/MUSIC_MENTAL_HEALTH.csv", sep=";")
csvdf = pd.DataFrame(mmhcsv)
#print(csvdf['Fav genre'])
genre_list = csvdf['Fav genre'].unique()

for i in range(len(genre_list)):
    genre_list[i] = genre_list[i].lower()
    if " " in genre_list[i]:
        genre_list[i] = genre_list[i].replace(" ", "-")
#print(genre_list)
"""
# List of genres in Spotify API
genre_list_spo = sp.recommendation_genre_seeds()['genres']
#print(genre_list_spo)


# Check if genre list from CSV is in API. If not, either fix, or find a close match
for i in genre_list:
    if i not in genre_list_spo:
        print(i)
"""

# Replace with suitable matches.
genre_list = list(map(lambda x: x.replace('r&b', 'r-n-b'), genre_list))
genre_list = list(map(lambda x: x.replace('video-game-music', 'anime'), genre_list))
genre_list = list(map(lambda x: x.replace('lofi', 'ambient'), genre_list))
# genre_list = list(map(lambda x: x.replace('rap', 'hip-hop'), genre_list)) #Rap is closest to hip-hop,
# which is already in the list.

genre_list.remove('rap')
#print(genre_list)

recs = sp.recommendations(seed_genres=[genre_list[0]], country='SG')
print(recs)

# Spotify recommendations by genre
genre_rec = []

for i in range(len(genre_list)):
    recs = sp.recommendations(seed_genres=[genre_list[i]], country='SG')
    j = 0
    while j<3:
        for k in range(len(recs['tracks'])):
            if recs['tracks'][k]['album']['album_type'].upper() == 'SINGLE':
                track_data = {
                    "track_name": recs['tracks'][k]["name"],
                    "artist": ", ".join(artist["name"] for artist in track["artists"]),
                    "album": recs['tracks'][k]["album"]["name"],
                    "genre": genre_list[i],
                    "preview_url": recs['tracks'][k]["preview_url"]
                }
                genre_rec.append(track_data)
                j+=1
        j = 3
print(genre_rec[0])
# Create a DataFrame from the track data
df = pd.DataFrame(genre_rec)

# Print the DataFrame
print(df)

# # Connect to PostgreSQL database
db_params = {
    "host": "localhost",
    "dbname": "Music_project",  # Replace with your desired database name
    "user": "postgres",  # Replace with your PostgreSQL username
    "password": "password",  # Replace with your PostgreSQL password
    "port": "5432" # Replace with your PostgreSQL port
}

conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Create a table (if not exists)
cur.execute("""
    CREATE TABLE IF NOT EXISTS recommended_tracks (
        track_name VARCHAR,
        artist VARCHAR,
        album VARCHAR,
        genre VARCHAR,
        preview_url VARCHAR
    )
""")
conn.commit()

# # Insert data into the table
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO recommended_tracks (track_name, artist, album, genre, preview_url)
        VALUES (%s, %s, %s, %s, %s)
    """, (row["track_name"], row["artist"], row["album"], row["genre"], row["preview_url"]))

conn.commit()
conn.close()



"""
recs = []
# Search for top 3 singles for each genre in list
for i in genre_list:
    j = 0
    print(i)
    search = sp.search(q = "genre:" + i, limit = 1, market = "SG")
    print(search)
    while j<3:
        for k in range(len(search['tracks']['items'])):
            if search['tracks']['items'][k]['album']['album_type']=='single':
                recs.append(search['tracks']['items'])
                j+=1
        j = 3
print(recs[0])
df = pd.DataFrame.from_dict(recs)
print(df.head())
"""

"""
auth_response = requests.post(auth_url, data=data)
access_token = auth_response.json().get('access_token')
headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}
"""

"""
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
"""

"""
# Featured playlists of Singapore
sg_feat_playlists = sp.featured_playlists(locale=None, country='SG', timestamp=None, limit=20, offset=0)
print(sg_feat_playlists)
"""

"""
### Categories in Singapore
# Popular categories in Singapore
categories = sp.categories('Singapore')
category_ids = {}
for i in range(len(categories['categories'])):
    category_ids[categories['categories']['items'][i]['name']] = (categories['categories']['items'][i]['id'])

# Playlists for above categories.
seed_genres = []
for cat, cat_id in category_ids.items():
    if cat.lower() in genre_list['genres']:
        seed_genres.append(cat)
    category_playlists = sp.category_playlists(cat_id, country='SG')
"""
# Must select more than one genre, otherwise it doesn't work
"""
if len(seed_genres) > 1:
    recs = sp.recommendations(seed_genres=seed_genres)
    print(recs)
"""
