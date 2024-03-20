# JDE03 Interim Project [Insight Igniters]

*****************

### 1. Introduction 
(Overview, Problem Statement)

Can music improve an individual's mood and overall mental health? If so, what music can someone listen to in order to counter certain mental conditions?

We seek to analyse the results from a survey of respondents regarding listening habits and mental health conditions, and based on the results, suggest tracks for the user based on her condition.

### 2. Data Sources
(Data Chosen, Data Dictionary)

Data from Kaggle, Spotify
.
.
.

### 3. Methodology/Approach 
(tech stack/tools, ETL (incl data preparation), architecture diagram, database schema/ERD diagram, table structure, data validation)

### 4. Challenges
(Solutions/Workarounds)/Limitations

- Spotify genre data questionable
- lack of time/knowledge

### 5. Findings/Analysis

### 6. Next Steps/Conclusion
- more visualisation
- better genre/track recommendations

******************

# Project Start
Get survey data on mental health and music
Download .csv from:
https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results/data

#### In Python:


```python
# Example python code:

# Step 1: import libraries
import pandas as pd
from sqlalchemy import create_engine

# Step 2: Read the CSV file
df = pd.read_csv('your_file.csv')

# Step 3: Drop unnecessary columns
df = df.drop(columns=['Timestamp', 'BPM', 'Permission'])

# Step 4: Rename the columns
df = df.rename(columns={'old_name1': 'new_name1', 'old_name2': 'new_name2'})

# Step 5: data cleaning (null, duplicates)
.
.
.

# Step 6: create new column (age_group) 

# Step 7: Create a connection to the PostgreSQL database
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# Step 8: Create new tables in PostgreSQL
commands = (# TABLE 1: results
            '''Create TABLE IF NOT EXISTS weather(id SERIAL PRIMARY KEY,
                                                age INT,
                                                streaming_service VARCHAR,
                                                hours INT,
                                                .
                                                .
                                                .
                                                .
                                                .);''')

# Step 9: Copy the data to the PostgreSQL table
df.to_sql('table_name', engine, if_exists='replace', index=False)
```

### Option A:

1. Extract 3 song recommendations from Spotify for each genre
2. Copy data into a table

### Create some visualisations:

1. most used streaming service
2. listen to music while working
3. fav genre by age group that improves mental health conditions, per mental health condition

### User Interaction:

1. Request input 'Are you affected by any of the following? 1.Anxiety 2.Depression 3.Insomnia 4.OCD 5. I'm feeling fine'
2. Based on answer, 
    if Option A (above) was chosen:
        search in tables for 3 song recommendations for the particular condition
    else 
        make an api call to spotify to get 3 song recommendations for the particular condition

** END **
