[music_mental_health]
GenSG JDE03 interim project

2024-03-21
Uploaded 3 files:
1. tracks_2_db_clean.ipynb 
    - gets 3 tracks for 15 genres (1 is not in Spotify's list and 3 need to be mapped to another genre later)
    - creates table in db and copies data to table
2. csv_2_db_clean.ipynb
    - converts the csv to a dataframe, rename the columns
    - creates table in db and copies data to table
3. sql_query_2_db_clean.ipynb
    - load ipython library
    - send sql queries to db and assign results to a variable
  
Todo: 
- study at Clinton's script
- explore cloud database as suggested by Clarence

2024-03-22

Discoveries:
1. Create a sql view to select the top genre per condition
%%sql
CREATE OR REPLACE VIEW anxiety_music 
AS
	(
	SELECT fav_genre, COUNT(*)
	FROM survey
	WHERE anxiety >= 7
	GROUP BY fav_genre
	ORDER BY COUNT(*) DESC
	LIMIT 1
    )

2. Use the result to print 3 recommendations from Spotify
%%sql result << 
SELECT t.track_name, t.artist, t.album, t.genre, t.preview_url 
FROM recommended_tracks t
JOIN anxiety_music a
ON a.fav_genre = t.genre

2024-03-25

1. Upload 3 latest files:
1_csv_clean_2_db_lee.ipynb
2_tracks_clean_2_db_lee.ipynb
3_sql_query_2_db_psycopg2_lee.ipynb

2. Created ElephantSQL acct and DB. Tested, works as expected. EOL in Jan 2025
3. Explore how to suggest tracks by looking at frequency instead of fav_genre (use sql in python?)

2024-04-01
1. Removed old files
2. Uploaded v2.0 files
