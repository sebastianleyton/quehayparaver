import sqlite3
from definitions import DB_PATH
import datetime


class DBConnection:
    def __init__(self, db_path):
        # Se crea el objeto DBConnection y se conecta a la base de datos que está en db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        # Se ejecuta la query con el cursor y se hace commit
        if not params:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.conn.commit()

    def query(self, query, params=None):
        # Se ejecuta la query y se devuelven los resultados en una lista
        result_list = []
        if not params:
            result = self.cursor.execute(query)
        else:
            result = self.cursor.execute(query, params)

        for row in result.fetchall():  # Recorro los rows devueltos por la query
            result_dict = {}
            for r in row.keys():
                result_dict[r] = row[r]
            result_list.append(result_dict)
        return result_list

    def get_all_movies(self):
        query = 'select * from movies'
        result = self.query(query)
        return result

    def get_latest_movies(self):
        query = 'select * from movies where created_date = (select max(created_date) from movies)'
        result = self.query(query)
        return result

    def get_latest_movies_from_cinema(self, cinema):
        query = 'select * from movies where cinema = ?'
        result = self.query(query, cinema)
        return result

    def get_movie_by_id(self, movie_id):
        query = 'select * from movies where id = ?'
        result = self.query(query, movie_id)
        return result

    def get_movie_by_title(self, title):
        query = 'select * from movies where title = ?'
        result = self.query(query, title)
        return result

    def insert_movie(self, title, description, duration, genre, address, cinema, image_name, url):
        timestamp = datetime.date.today()
        tpl = (title, description, duration, genre, address, cinema, image_name, url, timestamp, timestamp)
        query = 'insert into movies (title, description, duration, genre, address, cinema, image_name, movie_url, created_date, ' \
                'updated_date) values (?, ?, ?, ?, ?, ?, ? ,?, ?, ?) '
        self.execute(query, tpl)

class CinemeNames:
    grupocine = 'Cine Grupocine'
    lifecinema = 'Cine Life'
    moviecinema = 'Cine Movie'
def create_db_from_scratch():
    conn = DBConnection(DB_PATH)
    columns = 'id INTEGER PRIMARY KEY AUTOINCREMENT, title, description, duration, genre, address, cinema, ' \
              'image_name, movie_url, created_date, updated_date '
    query = f'CREATE TABLE movies ({columns})'
    conn.execute(query)

def test_db_functions():
    db = DBConnection(DB_PATH)
    db.insert_movie('Spiderman 1', 'El hombre araña nace, muere el tio Ben', '131', 'Accion', 'Complejo Ejido 123', 'Grupocine', 'test_image1')
    db.insert_movie('Spiderman 2', 'El doctor octopus nace, muere la tía May', '147', 'Accion', 'Complejo Ejido 123', 'Lifecinema', 'test_image2')
    db.insert_movie('Spiderman 3', 'El hombre de arena nace, muere Harry', '121', 'Accion', 'Complejo Ejido 123', 'Cinemovie', 'test_image3')
    all_data = db.get_all_movies()
