import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
MOVIE_IMAGES_PATH = os.path.join(ROOT_DIR, 'static', 'movie_images')
JSON_PATH = os.path.join(ROOT_DIR, 'database')
DB_PATH = os.path.join(ROOT_DIR, 'database', 'movies.db')
DB_LIB_PATH = os.path.join(ROOT_DIR, 'functions', 'dal') ## NOT USED
LOG_PATH = os.path.join(ROOT_DIR, 'logs')

