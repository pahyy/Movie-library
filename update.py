import pandas as pd
import sqlite3

def update_watched(csv_filename="ratings.csv", db_filename="movies.db"):
    df = pd.read_csv(csv_filename)

    df = df.rename(columns={
        'Name': 'title',
        'Year': 'year',
        'Rating': 'rating',
    })

    if 'watched' not in df.columns:
        df['watched'] = True
    if 'rating' in df.columns:
        df['rating'] = df['rating'] * 2

    df = df[['title', 'year', 'watched', 'rating']]

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    for _, x in df.iterrows():
        title = x['title']
        year = int(x['year'])
        rating = x['rating']
        watched = x.get('watched', True)

        cursor.execute('SELECT id FROM movies WHERE title = ? AND year = ?', (title, year))
        result = cursor.fetchone()

        if(not result):
            cursor.execute(
            '''
                INSERT INTO movies (title, year, watched, rating)
                VALUES (?, ?, ?, ?)
            ''', (title, year, watched, rating))    

    conn.commit()
    conn.close()


def update_watchlist(csv_filename="watchlist.csv", db_filename="movies.db"):
    df = pd.read_csv(csv_filename)

    df = df.rename(columns={
        'Name': 'title',
        'Year': 'year',
    })

    if 'watched' not in df.columns:
        df['watched'] = False
    if 'rating' not in df.columns:
        df['rating'] = None

    df = df[['title', 'year', 'watched', 'rating']]

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    for _, x in df.iterrows():
        title = x['title']
        year = None
        rating = x['rating']
        watched = x.get('watched', False)

        cursor.execute('SELECT id FROM movies WHERE title = ? AND year = ?', (title, None))
        result = cursor.fetchone()

        if(not result):
            cursor.execute(
            '''
                INSERT INTO movies (title, year, watched, rating)
                VALUES (?, ?, ?, ?)
            ''', (title, year, watched, rating))    

    conn.commit()
    conn.close()