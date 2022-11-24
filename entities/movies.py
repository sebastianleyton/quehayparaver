import database
from definitions import DB_PATH
from functions.dal.db import DBConnection


class Movie:
    def __init__(self, title, description, duration, genre, address, cinema, image_name, movie_url):
        self.title = title
        self.description = description
        self.duration = duration
        self.genre = genre
        self.address = address
        self.cinema = cinema
        self.image_name = image_name
        self.movie_url = movie_url

    def save(self):
        db = DBConnection(DB_PATH)
        db.insert_movie(self.title, self.description, self.duration, self.genre, self.address, self.cinema,
                        self.image_name, self.movie_url)
        db.cursor.close()
        db.conn.close()
