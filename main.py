import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import psycopg2
import kaggle
from sqlalchemy import create_engine

# API access credentials
os.environ['SPOTIPY_CLIENT_ID'] = '7c6d0e7c43904c28a29047f947d55951'
os.environ['SPOTIPY_CLIENT_SECRET'] = '277304c85fa442059e887b5222581aba'

# Authentication
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

# Import genre list from mental health CSV
kaggle.api.authenticate()
kaggle.api.dataset_download_files("catherinerasgaitis/mxmh-survey-results", path="C:/Users/Clinton/Desktop/Python/Spotify/", unzip=True)
#mmhcsv = pd.read_csv("C:/Users/Clinton/Desktop/Python/Spotify/mxmh-survey-results.csv", sep=";")
mmhcsv = pd.read_csv("C:/Users/Clinton/Desktop/Python/Spotify/mxmh_survey_results.csv")
csvdf = pd.DataFrame(mmhcsv)
genre_list = csvdf['Fav genre'].unique()

for i in range(len(genre_list)):
    genre_list[i] = genre_list[i].lower()
    if " " in genre_list[i]:
        genre_list[i] = genre_list[i].replace(" ", "-")

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

recs = sp.recommendations(seed_genres=[genre_list[0]], country='SG')

# Spotify recommendations by genre, taking 3 tracks per genre
genre_rec = []

for i in range(len(genre_list)):
    recs = sp.recommendations(seed_genres=[genre_list[i]], country='SG')
    for k in range(10):
        track_data = {
            "track_name": recs['tracks'][k]["name"],
            "artist": ", ".join(artist["name"] for artist in recs['tracks'][k]["artists"]),
            "album": recs['tracks'][k]["album"]["name"],
            "genre": genre_list[i],
            "image": recs['tracks'][k]["album"]["images"][0]["url"],
            "preview_url": recs['tracks'][k]["preview_url"],
            "url": recs['tracks'][k]['album']['external_urls']['spotify']
        }
        genre_rec.append(track_data)

        # Search for individual track by ID to get "popularity".
        track_search = sp.track(recs['tracks'][k]['id'])
        track_data["popularity"] = track_search["popularity"]

        # Search for audio features of track by ID
        audio_features = sp.audio_features(recs['tracks'][k]['id'])[0]
        for key, value in audio_features.items():
            track_data[key] = value

# Create a DataFrame from the track data
df = pd.DataFrame(genre_rec)

# Return recommendations by genre
df = df.sort_values("popularity", ascending=False).groupby("genre")
df = df.head(3).sort_values("genre").reset_index()

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

# Drop existing table
cur.execute("""
    DROP TABLE IF EXISTS recommended_tracks
""")

# Create a table
cur.execute("""
    CREATE TABLE recommended_tracks (
        track_name VARCHAR,
        artist VARCHAR,
        album VARCHAR,
        genre VARCHAR,
        image VARCHAR,
        preview_url VARCHAR,
        url VARCHAR,
        popularity SMALLINT,
        danceability FLOAT,
        energy FLOAT,
        key SMALLINT,
        loudness FLOAT,
        mode SMALLINT,
        speechiness FLOAT,
        acousticness FLOAT,
        liveness FLOAT, 
        valence FLOAT,
        tempo FLOAT,
        type VARCHAR,
        id VARCHAR,
        uri VARCHAR,
        track_href VARCHAR,
        analysis_url VARCHAR,
        duration_ms INT,
        time_signature SMALLINT
    )
""")
conn.commit()

# Insert data into the table
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO recommended_tracks (track_name, artist, album, genre, image, preview_url, url, popularity, danceability, energy, key, loudness, mode, speechiness, acousticness, liveness, valence, tempo, type, id, uri, track_href, analysis_url, duration_ms, time_signature)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row["track_name"], row["artist"], row["album"], row["genre"], row["image"], row["preview_url"], row["url"], row["popularity"], row["danceability"], row["energy"], row["key"], row["loudness"], row["mode"], row["speechiness"], row["acousticness"], row["liveness"], row["valence"], row["tempo"], row["type"], row["id"], row["uri"], row["track_href"], row["analysis_url"], row["duration_ms"], row["time_signature"]))

conn.commit()

# Drop columns of no value
cur.execute("""
    ALTER TABLE recommended_tracks
    DROP COLUMN type,
    DROP COLUMN uri,
    DROP COLUMN track_href,
    DROP COLUMN analysis_url;
""")
conn.commit()

# Close connection to PostgreSQL
conn.close()


