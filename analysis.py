import psycopg2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as pyplot

# Connect to DB
db_params = {
    "host": "rain.db.elephantsql.com",
    "dbname": "auspovuc",  # Replace with your desired database name
    "user": "auspovuc",  # Replace with your PostgreSQL username
    "password": "bmJdG19Daw9rkEsJ3VnkefRGCBF_oy7F",  # Replace with your PostgreSQL password
}

conn = psycopg2.connect(**db_params)
cur = conn.cursor()

with conn.cursor() as cursor:
    # Read data from database
    sql = "SELECT * FROM `users`"
    cursor.execute(sql)

    # Fetch all rows
    rows = cursor.fetchall()

    # Print results
    for row in rows:
        print(row)
