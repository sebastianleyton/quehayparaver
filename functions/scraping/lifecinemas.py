import os
import shutil
import json
import sys
import requests

from selenium.common import NoSuchElementException
from definitions import MOVIE_IMAGES_PATH, JSON_PATH, DB_LIB_PATH, DB_PATH
from scraping_helper import Scraper
from functions.dal import db

URL = "https://lifecinemas.com.uy/pelicula/cartelera"
SELECTOR_CSS_MOVIE_LINKS = "#ultimos_estrenos .movie-container a"
URL_BASE = "https://lifecinemas.com.uy"
SELECTOR_FULL_MOVIE = ".movie-sucursal"
JSON_NAME = 'life.json'

def get_links():
    nav = Scraper()

    # Cargar URL
    nav.cargar_sitio(URL)

    # Guardar links de pelis
    movies_links_str = nav.extraer_url_de_lista(SELECTOR_CSS_MOVIE_LINKS)
    # prit(movies_elements)

    # Inicializar lista final de datos
    lista_completa_de_datos = []

    # Inicar loop por cada link de peli
    contador = 0
    for movie_url in movies_links_str:
        contador += 1
        print(f"Iterando lista: {contador} de {len(movies_links_str)}")
        if "/festival/" in movie_url:
            print("Ignorando url...")
            continue

        nav.cargar_sitio(movie_url)

        try:
            # Obtener titulo
            selector_titulo = SELECTOR_FULL_MOVIE + ' div.title-cont-2 h2 a'
            print(selector_titulo)
            titulo = nav.extraer_texto(selector_titulo)
        except NoSuchElementException as e:
            print(f"Excepcion al buscar titulo: {e}")
            continue


        # Crear nombre de imagen reemplazando los simbolos invalidos en windows por su equivalente textual
        imagen = titulo
        if '?' in titulo:
            imagen = imagen.replace('?', 'SIGNODEPREGUNTA')
        if ':' in titulo:
            imagen = imagen.replace(':', 'DOSPUNTOS')

        # Obtener descripcion
        selector_descripcion = SELECTOR_FULL_MOVIE + ' div p'
        descripcion = nav.extraer_texto(selector_descripcion)

        # Obtener imagen url
        selector_imagen_url = SELECTOR_FULL_MOVIE + ' div.img-movie a img'
        imagen_url = nav.extraer_atributo_generico(selector_imagen_url, 'src')

        download_image(imagen_url, titulo)

        # TODO: Scrapear los campos nuevos title, description, duration, genre, address, cinema, image_name
        # TODO: Guardar la información en la base de datos
        dict = {"titulo": titulo, "descripcion": descripcion, "imagen": imagen}

        lista_completa_de_datos.append(dict)

    nav.cerrar_navegador()
    # json_object = json.dumps(lista_completa_de_datos, indent=4)
    with open(os.path.join(JSON_PATH, JSON_NAME), "w+") as json_file:
        json.dump(lista_completa_de_datos, json_file)
    # return lista_completa_de_datos

def download_image(url, titulo, save_path=os.path.join(MOVIE_IMAGES_PATH)):
    r = requests.get(url, stream=True)
    print(r.status_code)
    filename = os.path.join(save_path, f'{titulo}.png')
    print(filename)
    with open(filename, 'w+b') as f:
        shutil.copyfileobj(r.raw, f)

get_links()