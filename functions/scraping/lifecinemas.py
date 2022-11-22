
import datetime
import uuid
from selenium.common import NoSuchElementException
from definitions import DB_PATH
from scraping_helper import Scraper, download_image
from functions.dal.db import DBConnection, CinemecNames, create_db_from_scratch
import time

URL = 'https://lifecinemas.com.uy/pelicula/cartelera'
SELECTOR_CSS_MOVIE_LINKS = ".movie-container a"
SELECTOR_CSS_URL_MOVIE = ".movie-sucursal div.title-cont-2 h2 a"
SELECTOR_TITLE = 'div.tech-data dd:nth-child(4)'
SELECTOR_DESCRIPTION = 'div.sipnosis p'
SELECTOR_IMAGEN_URL = '.img-movie img'
SELECTOR_DURATION = 'div.tech-data dd:nth-child(6)'
SELECTOR_CAST = 'div.tech-data dt:nth-child(9)'
# 'div.tech-data dt:nth-child(9)'
# /html/body/div[2]/div/div[1]/div[3]/div/dl/dd[5]
SELECTOR_GENRE_1 = 'div.tech-data dd:nth-child(12)'
SELECTOR_GENRE_2 = 'div.tech-data dd:nth-child(10)'
SELECTOR_COMPLEX = '.date-data h3'
JSON_NAME = 'lc.json'

DEBUG_FLAG = 1


def get_links():
    nav = Scraper()
    db = DBConnection(DB_PATH)

    # Cargar URL CARTELERA DE PELIS
    nav.cargar_sitio(URL)

    # Guardar links de pelis
    movies_links_str = nav.extraer_url_de_lista(SELECTOR_CSS_MOVIE_LINKS)

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
        else:
            lista_completa_de_URLS.append(movie_url)
    contador = 0
    for movie_url in  lista_completa_de_URLS:
        contador += 1
        print(f"Iterando lista: {contador} de {len(lista_completa_de_URLS)}")
        nav.cargar_sitio(movie_url)
        time.sleep(1)
        ### SCRAPING POR PELICULA
        try:
            # Obtener titulo
            titulo = nav.extraer_texto(SELECTOR_TITLE)
        except NoSuchElementException as e:
            print(f"Excepcion al buscar titulo: {e}")
            continue

        # Crear nombre de imagen reemplazando los simbolos invalidos en windows por su equivalente textual
        imagen = titulo
        ## Armar Funcion?
        if '?' in titulo:
            imagen = imagen.replace('?', 'SIGNODEPREGUNTA')
        if ':' in titulo:
            imagen = imagen.replace(':', 'DOSPUNTOS')
#
        # Obtener descripcion
        descripcion = nav.extraer_texto(SELECTOR_DESCRIPTION)

        # Obtener Duracion
        duracion = nav.extraer_texto(SELECTOR_DURATION)

        # Obtener Genero dependiendo de la pagina (Casos en que no existe el row Actores)
        if nav.extraer_texto(SELECTOR_CAST) == 'Actores:':
            genero = nav.extraer_texto(SELECTOR_GENRE_1)
        else:
            genero = nav.extraer_texto(SELECTOR_GENRE_2)

        # Obtener cinema
        cinema = CinemecNames.lifecinema

        # Obtener Complejos
        complejos = nav.extraer_texto_de_lista(SELECTOR_COMPLEX)

        # Descargar Imagen
        imagen = str(uuid.uuid1())
        imagen_url = nav.extraer_atributo_generico(SELECTOR_IMAGEN_URL, 'src')
        download_image(imagen_url, imagen)

        movie_url = nav.chrome.current_url
        # Poner timestamp en el nombre de la imagen al almacenarla
        timestamp = datetime.date.today().strftime('%m-%d')
        imagen = timestamp + "/" + imagen

        # Guardar en DB
        for complejo in complejos:
            db.insert_movie(titulo, descripcion, duracion, genero, complejo, cinema, imagen, movie_url)
    db.cursor.close()
    db.conn.close()
    nav.cerrar_navegador()


get_links()
# db = DBConnection(DB_PATH)
# test2 = db.DBConnection(DB_PATH)
# create_db_from_scratch()
# all_data = test2.get_all_movies()
# print(all_data)`
