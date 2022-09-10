import shutil
import json
import bs4
import requests

URL = "https://lifecinemas.com.uy/pelicula/cartelera"
SELECTOR_CSS_MOVIE_LINKS = "#ultimos_estrenos .movie-container a"
URL_BASE = "https://lifecinemas.com.uy"
SELECTOR_CSS_MOVIE = ".movie-sucursal"

def get_links():
    html = bs4.BeautifulSoup(requests.get(URL).text, features="html.parser")
    #print(html)

    # Listar todos los titulos en formato de objeto bs4
    movies_elements = html.select(SELECTOR_CSS_MOVIE_LINKS)
    #print(movies_elements)


    #Pasar a la lista de bs4 a lista de strings
    movies_links_str = []
    for movie in movies_elements:
        movies_links_str.append(movie['href'])

    # la misma lista usando list comprehension
    # movies_list_str = [movie.text for movie in movies_list_bs]
    #print(movies_links_str)
    # return movies_list_str
    lista_completa_de_datos = []

    contador = 0
    for movie_url in movies_links_str:
        contador += 1
        print(f"Iterando lista: {contador} de {len(movies_links_str)}")
        movie_url_full = URL_BASE + movie_url
        print(f"Trabajando con: {movie_url_full}")
        if "/festival/" in movie_url:
            print("Ignorando url...")
            continue
        #print(movie_url_full)
        print("Cargando URL...")
        html = bs4.BeautifulSoup(requests.get(movie_url_full).text, features="html.parser")
        print("URL Cargada.")
        try:
            movie_full = html.select(SELECTOR_CSS_MOVIE)[0]
        except:
            print(f"Problema con el link: {movie_url}")
            continue

        # Obtener titulo
        selector_titulo = 'div.title-cont-1 h2'

        titulo = movie_full.select(selector_titulo)[0].text
        if '?' in titulo:
            titulo = titulo.replace('?', 'SIGNODEPREGUNTA')
        if ':' in titulo:
            titulo = titulo.replace(':', 'DOSPUNTOS')
        print(f"Titulo scrapeado: {titulo}")

        # Obtener descripcion
        selector_descripcion = 'div p'
        descripcion = movie_full.select(selector_descripcion)[0].text
        print(f"Descripcion scrapeada: {descripcion}")


        # Obtener imagen url
        selector_imagen_url = 'div.img-movie a img'
        imagen_url = 'https:' + movie_full.select(selector_imagen_url)[0]['src']
        print(f"Imagen link scrapeado: {imagen_url}")

        download_image(imagen_url, titulo)

        #TODO: Guardar en el diccionario el titulo de la imagen tambien para luego no tener problemas al reemplazar el signo de pregunta en el nombre
        dict = {"titulo": titulo, "descripcion": descripcion}
        lista_completa_de_datos.append(dict)

    #json_object = json.dumps(lista_completa_de_datos, indent=4)
    with open("../../database/movies.json", "w") as json_file:
        json.dump(lista_completa_de_datos, json_file)
    #return lista_completa_de_datos
def download_image(url, titulo, save_path="/static/movie_images/"):
    r = requests.get(url, stream=True)
    with open(f'{save_path}{titulo}.png', 'wb') as f:
        shutil.copyfileobj(r.raw, f)

get_links()