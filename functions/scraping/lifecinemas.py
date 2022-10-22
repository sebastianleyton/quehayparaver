import os
import shutil
import json
import sys
import requests
from selenium.common import NoSuchElementException
from definitions import MOVIE_IMAGES_PATH, JSON_PATH, DB_LIB_PATH, DB_PATH
from scraping_helper import Scraper
from functions.dal import db

URL = 'https://lifecinemas.com.uy/pelicula/cartelera'
SELECTOR_CSS_MOVIE_LINKS = ".movie-container a"
SELECTOR_CSS_URL_MOVIE = ".movie-sucursal div.title-cont-2 h2 a"
#SELECTOR_CSS_URL_MOVIE = "div.title-cont-1 h2 a"
SELECTOR_TITLE = 'div.tech-data dd:nth-child(4)'
SELECTOR_DESCRIPTION = 'div.sipnosis p'
SELECTOR_IMAGEN_URL = '.img-movie img'
SELECTOR_DURATION = 'div.tech-data dd:nth-child(6)'
SELECTOR_GENERO = 'div.tech-data dd:nth-child(12)'
JSON_NAME = 'lc.json'

DEBUG_FLAG = 1


def get_links():
    nav = Scraper()

    # Cargar URL CARTELERA DE PELIS
    nav.cargar_sitio(URL)

    # Guardar links de pelis
    movies_links_str = nav.extraer_url_de_lista(SELECTOR_CSS_MOVIE_LINKS)
    # for movies in movies_links_str:
    #     print(movies)
    #     nav.cargar_sitio(movies)
    #     lista_completa_de_datos.append(nav.extraer_url(SELECTOR_CSS_URL_MOVIE))
    #     print(lista_completa_de_datos)
    # movies_links_str_final = nav.extraer_url_de_lista()
    #     # Inicializar lista final de datos
    #     lista_completa_de_datos = []

    # Inicar loop por cada link de peli
    lista_completa_de_URLS = []
    contador = 0
    for movie_url in movies_links_str:
        # Este FOR hace la primer pasada para armar el array lista_completa_de_datos
        print(movie_url)
        contador += 1
        print(f"Iterando lista: {contador} de {len(movies_links_str)}")
        ## Caso de que es un festival
        if "/festival/" in movie_url:
            print("Ignorando url...")
            continue
        ## Caso de que es una pelicula y hay que sacar el link final
        elif "/pelicula/agrupacion" in movie_url:
            nav.cargar_sitio(movie_url)
            lista_completa_de_URLS.append(nav.extraer_url(SELECTOR_CSS_URL_MOVIE))
        ## Caso en que la pelicula ya tiene la descripcion
        else: lista_completa_de_URLS.append(movie_url)
    contador = 0
    for movie_url in  lista_completa_de_URLS:
        contador += 1
        print(f"Iterando lista: {contador} de {len(lista_completa_de_URLS)}")
        nav.cargar_sitio(movie_url)
        ### SCRAPING POR PELICULA
        try:
            # Obtener titulo
            titulo = nav.extraer_texto(SELECTOR_TITLE)
        except NoSuchElementException as e:
            print(f"Excepcion al buscar titulo: {e}")
            continue

        # Crear nombre de imagen reemplazando los simbolos invalidos en windows por su equivalente textual
        imagen = titulo
        if '?' in titulo:
            imagen = imagen.replace('?', 'SIGNODEPREGUNTA')
        if ':' in titulo:
            imagen = imagen.replace(':', 'DOSPUNTOS')
#
        # Obtener descripcion
        descripcion = nav.extraer_texto(SELECTOR_DESCRIPTION)

        # Obtener URL imagen
        imagen_url = nav.extraer_atributo_generico(SELECTOR_IMAGEN_URL, 'src')

        # Obtener Duracion
        duracion = nav.extraer_texto(SELECTOR_DURATION)

        # Obtener Genero
        genero = nav.extraer_texto(SELECTOR_GENERO)

        # Descargar Imagen
        download_image(imagen_url, titulo)

        # Guardar en DB
        mc = db.DBConnection(DB_PATH)
        mc.insert_movie(titulo, descripcion, duracion, genero, 'Complejo', db.CinemecNames.lifecinema, imagen, movie_url)
#

#         dict = {"titulo": titulo, "descripcion": descripcion, "imagen": imagen}
#         lista_completa_de_datos.append(dict)
#
    nav.cerrar_navegador()
#       TO BE DELETED SOON
#     # json_object = json.dumps(lista_completa_de_datos, indent=4)
#     with open(os.path.join(JSON_PATH, JSON_NAME), "w+") as json_file:
#         json.dump(lista_completa_de_datos, json_file)
#     # return lista_completa_de_datos
#
def download_image(url, titulo, save_path=os.path.join(MOVIE_IMAGES_PATH)):
    r = requests.get(url, stream=True)
    print(r.status_code)
    filename = os.path.join(save_path, f'{titulo}.png')
    print(filename)
    with open(filename, 'w+b') as f:
        shutil.copyfileobj(r.raw, f)


get_links()
#test2 = db.DBConnection(DB_PATH)
#db.create_db_from_scratch()
#all_data = test2.get_all_movies()
#print(all_data)
