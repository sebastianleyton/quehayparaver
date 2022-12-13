import os.path
from flask import Flask, render_template
from definitions import JSON_PATH, DB_PATH
from functions.dal import db
#from functions.scraping.lifecinemas import get_links

# from functions.scraping import grupocine
# from functions.scraping import lifecinemas
app = Flask(__name__)

# / peliculas / grupocine
# / peliculas / lifecinema
# / peliculas / cinemovie
# / peliculas / all


@app.route('/')
def hello_world():
    # pelis_grupocine = grupocine.get_data()
    # pelis_lifecinema = lifecinemas.get_links()
    json_exists = os.path.exists(JSON_PATH)
    if not json_exists:
        pelis_lifecinema = '[]'
    else:
        pelis_lifecinema = get_all_movies()

    return render_template('index.html', pelis_lifecinema=pelis_lifecinema)
    # return render_template('index.html')



@app.route('/movies/grupocine')
def get_all_movies_grupocine():
    # pelis_grupocine = grupocine.get_data()
    # pelis_lifecinema = lifecinemas.get_links()
    db_conn = db.DBConnection(DB_PATH)
    cinema = db.CinemecNames.grupocine
    # json_exists = os.path.exists(JSON_PATH)
    # if not json_exists:
    #     pelis_grupocine = '[]'
    # else:
    pelis_grupocine = db_conn.get_latest_movies_title_from_cinema(cinema)


    # En realidad esto deberia convertirse en un json con ¿jsonify?
    titles = [{'title': t['title']} for t in pelis_grupocine]
    return titles
    # return render_template('index.html')

@app.route('/movies/titles')
def get_all_movies():
    # pelis_grupocine = grupocine.get_data()
    # pelis_lifecinema = lifecinemas.get_links()
    json_exists = os.path.exists(JSON_PATH)
    if not json_exists:
        pelis_lifecinema = '[]'
    else:
        pelis_lifecinema = get_all_movies()


    # En realidad esto deberia convertirse en un json con ¿jsonify?
    titles = [{'title': t['title']} for t in pelis_lifecinema]
    return titles
    # return render_template('index.html')

def get_all_movies():
    db_conn = db.DBConnection(DB_PATH)
    movies = db_conn.get_all_movies()
    return movies

# def arreglar_caracteres_en_titulos(lista):
#     print(lista)
#     for lala in lista:
#         print(lala)
#         if 'SIGNODEPREGUNTA' in lala['titulo']:
#             lala['titulo'] = lala['titulo'].replace('SIGNODEPREGUNTA', '?')
#         if 'DOSPUNTOS' in lala['titulo']:
#             lala['titulo'] = lala['titulo'].replace('DOSPUNTOS', ':')
#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

