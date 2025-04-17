import sqlite3
from update import update_watched
from update import update_watchlist

class Movie:
    def __init__(self, title, year, watched=False, rating=None):
        self.title = title
        self.year = year
        self.watched = watched
        self.rating = rating

class MovieLibrary:
    def __init__(self, db_name="movies.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER,
                watched BOOLEAN,
                rating REAL
            )
        ''')
        self.conn.commit()

    def add_movie(self, movie: Movie):
        self.cursor.execute('''
            INSERT INTO movies (title, year, watched, rating)
            VALUES (?, ?, ?, ?, ?)
        ''', (movie.title, movie.year, movie.watched, movie.rating))
        self.conn.commit()

    def list_movies(self):
        self.cursor.execute('SELECT id, title, year, watched, rating FROM movies')
        rows = self.cursor.fetchall()
        print("\nAll Movies:")
        for row in rows:
            id_, title, year, watched, rating = row
            status = "Watched" if watched else "To-Watch"
            print(f"[{id_}] {title} ({year}) - {status} - Rating: {rating if rating else 'N/A'}")

    def watchlist(self):
        self.cursor.execute('SELECT id, title, year FROM movies WHERE watched = 0')
        rows = self.cursor.fetchall()
        print("\nWatchlist:")
        if(not rows):
            print("  (Empty)")
        else:
            for row in rows:
                id_, title, year = row
                print(f"[{id_}] {title} ({year})")

    def mark_watched(self, id):
        self.cursor.execute(
            '''
            UPDATE movies
            SET watched = 1
            WHERE id = ?
        ''', (id,))
        self.conn.commit()

    def update_rating(self, rating, id):
        self.cursor.execute(
        '''
        UPDATE movies
        SET rating = ?           
        WHERE id = ?
        ''', (rating, id))

    def close(self):
        self.conn.close()


def main():
    lib = MovieLibrary()

    while True:
        print("")
        print("=== Movie Library Menu ===")
        print("1. Add a movie")
        print("2. Show all movies")
        print("3. Show Watchlist")
        print("4. Mark a movie as watched")
        print("5. Update existing rating")
        print("6. Update movies from Letterboxd")
        print("7. Exit")

        choice = input("Choose an option: ")

        if(choice == "1"):
            title = input("Title: ")
            year = int(input("Year: "))
            watched = input("Already watched? (y/n): ").lower() == "y"
            rating = None
            if(watched):
                rating = float(input("Rating (1–10): "))
            movie = Movie(title, year, watched, rating)
            lib.add_movie(movie)
            print("Movie added!")
        elif(choice == "2"):
            lib.list_movies()
        elif(choice == "3"):
            lib.watchlist()
        elif(choice == "4"):
            lib.watchlist()
            try:
                id = int(input("Enter the ID of the movie to mark as watched: "))
                lib.mark_watched(id)
                rating = float(input("Rating (1–10): "))
                lib.update_rating(rating, id)
                print("Marked as watched!")
            except ValueError:
                print("Invalid ID.") 
        elif(choice == "5"):
            lib.list_movies()
            try:
                id = input("ID of the movie you want to update: ")
                rating = input("New rating (1-10): ")
                lib.update_rating(rating, id)
            except ValueError:
                print("Invalid ID.") 
        elif(choice == "6"):
            importChoice = input("Do you want to update your watched list or your watchlist: \n" \
            "1. Watched\n2. Watchlist \n3. Help\nChoose an option: ")
            if(importChoice == "1"):
                update_watched()
                print("Movies updated")
            elif(importChoice == "2"):
                update_watchlist()
                print("Watchlist updated")
            elif(importChoice == "3"):
                print("To import movies from Letterboxd export your Letterboxd data and paste \n" \
                "the files 'ratings.csv' and 'watchlist.csv' to the folder in which your 'movies.py' is.")
        elif(choice == "7" or choice == "q"):
            lib.close()
            break
        else:
            print("Nope.")

if(__name__ == "__main__"):
    main()