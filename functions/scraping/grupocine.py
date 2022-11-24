import os
import shutil
import json
import requests
import uuid
import datetime
from selenium.common import NoSuchElementException
from definitions import MOVIE_IMAGES_PATH, JSON_PATH, DB_PATH
from entities.movies import Movie
from scraping_helper import Scraper, download_image, minute_trim
from functions.dal.db import DBConnection
import time



URL = "https://www.grupocine.com.uy/SIGE_CN/servlet/com.sigecn.cartelera"
SELECTOR_CSS_MOVIE_LINKS = "#GridpeliculasContainerTbl a"
URL_BASE = "https://www.grupocine.com.uy"
SELECTOR_FULL_MOVIE = ".movie-sucursal"
SELECTOR_TITLE = '#TXTTITLEPELICULA'
SELECTOR_DESCRIPTION = '#TXTDESCRIPCIONVAL'
SELECTOR_DURATION = '#TXTDURACIONVAL'
SELECTOR_GENRE = '#TXTGENEROVAL'
SELECTOR_ADDRESS = 'input.BtnCRRed'
SELECTOR_IMAGEN_URL = '#TABLEPELICULACONTAINER img'
CINEMA = 'Grupocine'
JSON_NAME = 'gc.json'


DEBUG_FLAG = 0


def get_links():
    nav = Scraper()
    db = DBConnection(DB_PATH)

    # Cargar URL
    nav.cargar_sitio(URL)

    # Guardar links de pelis
    movies_links_str = nav.extraer_url_de_lista(SELECTOR_CSS_MOVIE_LINKS)
    if DEBUG_FLAG:
        print(movies_links_str)

    # Inicializar lista final de datos
    lista_completa_de_datos = []

    # Inicar loop por cada link de peli
    contador = 0
    for movie_url in movies_links_str:
        contador += 1
        print(f"Iterando lista: {contador} de {len(movies_links_str)}")
        # if "/festival/" in movie_url:
        #     print("Ignorando url...")
        #     continue
        nav.cargar_sitio(movie_url)
        time.sleep(1)

        try:
            # Obtener titulo
            titulo = nav.extraer_texto(SELECTOR_TITLE)
        except NoSuchElementException as e:
            print(f"Excepcion al buscar titulo: {e}")
            continue

        # Obtener descripcion
        descripcion = nav.extraer_texto(SELECTOR_DESCRIPTION)

        # Obtener duracion
        duracion = minute_trim(nav.extraer_texto(SELECTOR_DURATION))

        # Obtener genero
        genero = nav.extraer_texto(SELECTOR_GENRE)

        # Obtener direccion
        direccion = nav.extraer_atributo_generico(SELECTOR_ADDRESS, 'title')

        # Obtener cinema
        cinema = CINEMA

        # Obtener imagen url
        SELECTOR_IMAGEN_URL = '#TABLEPELICULACONTAINER img'

        imagen = str(uuid.uuid1())
        imagen_url = nav.extraer_atributo_generico(SELECTOR_IMAGEN_URL, 'src')

        download_image(imagen_url, imagen)

        # Obtenre URL de la pelicula
        movie_url = nav.chrome.current_url


        # Poner timestamp en el nombre de la imagen al almacenarla
        timestamp = datetime.date.today().strftime('%m-%d')
        imagen = timestamp + "/" + imagen

        movie = Movie(titulo, descripcion, duracion, genero, direccion, cinema, imagen, movie_url)
        movie.save()


    db.cursor.close()
    db.conn.close()
    nav.cerrar_navegador()




get_links()