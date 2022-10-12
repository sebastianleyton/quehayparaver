import os
import shutil
import json
import requests
from selenium.common import NoSuchElementException
from definitions import MOVIE_IMAGES_PATH, JSON_PATH
from scraping_helper import Scraper

URL = "https://www.grupocine.com.uy/SIGE_CN/servlet/com.sigecn.cartelera"
SELECTOR_CSS_MOVIE_LINKS = "#GridpeliculasContainerTbl a"
URL_BASE = "https://www.grupocine.com.uy"
SELECTOR_FULL_MOVIE = ".movie-sucursal"
SELECTOR_TITLE = '#TXTTITLEPELICULA'
SELECTOR_DESCRIPTION = '#TXTDESCRIPCIONVAL'
SELECTOR_IMAGEN_URL = '#TABLEPELICULACONTAINER img'
JSON_NAME = 'gc.json'
# Se me ocurre que se puede armar como una lista de parametros para pasarle con todos los selectores


DEBUG_FLAG = 0


def get_links():
    nav = Scraper()

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

        # Obtener descripcion
        descripcion = nav.extraer_texto(SELECTOR_DESCRIPTION)

        # Obtener imagen url
        # SELECTOR_IMAGEN_URL = '#TABLEPELICULACONTAINER img'

        imagen_url = nav.extraer_atributo_generico(SELECTOR_IMAGEN_URL, 'src')

        download_image(imagen_url, imagen)
        # TODO: Expandir el json para guardar
        dict = {"titulo": titulo, "descripcion": descripcion, "imagen": imagen}
        lista_completa_de_datos.append(dict)
    #
    nav.cerrar_navegador()
    # json_object = json.dumps(lista_completa_de_datos, indent=4)

    # TODO: Scrapear los campos nuevos title, description, duration, genre, address, cinema, image_name
    # TODO: Guardar la información en la base de datos
    with open(os.path.join(JSON_PATH, JSON_NAME), "w+") as json_file:
        json.dump(lista_completa_de_datos, json_file)
    # return lista_completa_de_datos


def download_image(url, imagen, save_path=os.path.join(MOVIE_IMAGES_PATH)):
    r = requests.get(url, stream=True)
    print(r.status_code)
    filename = os.path.join(save_path, f'{imagen}.png')
    print(filename)
    with open(filename, 'w+b') as f:
        shutil.copyfileobj(r.raw, f)
