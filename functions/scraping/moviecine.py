import os
import shutil
import requests
from selenium.common import NoSuchElementException
from definitions import MOVIE_IMAGES_PATH, JSON_PATH, DB_LIB_PATH, DB_PATH
from entities.movies import Movie
from scraping_helper import Scraper, download_image
from functions.dal.db import DBConnection, CinemecNames
import datetime
import uuid
import time


URL = 'https://www.movie.com.uy/movies'
SELECTOR_CSS_MOVIE_LINKS = ".row div h2 a"
SELECTOR_FULL_MOVIE = ".img-poster"
SELECTOR_TITLE = '.row h1'
SELECTOR_DESCRIPTION = '#target p'
SELECTOR_IMAGEN_URL = '.img-poster'
SELECTOR_DURATION = '.hidden-xs li:nth-child(2)'
SELECTOR_GENERO = '.hidden-xs li:nth-child(3)'
SELECTOR_COMPLEX = '.schedules h5'
JSON_NAME = 'mc.json'

def scrape_data():
    # Inicializacion de nav que es de de Clase Scraper
    nav = Scraper()

    # Cargar URL
    nav.cargar_sitio(URL)

    time.sleep(10)
    # Guardar links de pelis
    movies_links_str = nav.extraer_url_de_lista(SELECTOR_CSS_MOVIE_LINKS)

    # Inicar loop por cada link de peli
    contador = 0
    for movie_url in movies_links_str:
        contador += 1
        print(f"Iterando lista: {contador} de {len(movies_links_str)}")
        nav.cargar_sitio(movie_url)
        time.sleep(1)

        #### SCRAPING POR PELICULA
        try:
            # Obtener titulo
            titulo = nav.extraer_texto(SELECTOR_TITLE)
        except NoSuchElementException as e:
            print(f"Excepcion al buscar titulo: {e}")
            continue

        # Crear nombre de imagen reemplazando los simbolos invalidos en windows por su equivalente textual

        # if '?' in titulo:
        #     imagen = imagen.replace('?', 'SIGNODEPREGUNTA')
        # if ':' in titulo:
        #     imagen = imagen.replace(':', 'DOSPUNTOS')

        # Obtener descripcion
        descripcion = nav.extraer_texto(SELECTOR_DESCRIPTION)

        # Obtener Duracion
        d1 = nav.extraer_texto(SELECTOR_DURATION)
        duracion = nav.normalizar_duracion(d1)

        # Obtener Genero
        genero = nav.extraer_texto(SELECTOR_GENERO)

        # Obtener Complejos
        complejos = nav.extraer_texto_de_lista(SELECTOR_COMPLEX)
        complejos = list(filter(None, complejos))
        print(complejos)

        # Descargar Imagen
        imagen = str(uuid.uuid1())
        imagen_url = nav.extraer_atributo_generico(SELECTOR_IMAGEN_URL, 'src')
        download_image(imagen_url, imagen)

        movie_url = nav.chrome.current_url

        # Poner timestamp en el nombre de la imagen al almacenarla
        timestamp = datetime.date.today().strftime('%m-%d')
        imagen = timestamp + "/" + imagen

        for complejo in complejos:
            movie = Movie(titulo, descripcion, duracion, genero, complejo, CinemecNames.moviecinema, imagen, movie_url)
            movie.save()

    nav.cerrar_navegador()
