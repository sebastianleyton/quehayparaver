import shutil

import requests
import bs4


def get_titles_list(url, selector_css):
    # Cargar pagina
    html = bs4.BeautifulSoup(requests.get(url).raw, features="html.parser")


    # Listar todos los titulos en formato de objeto bs4
    movies_list_bs = html.select(selector_css)

    # Pasar a la lista de bs4 a lista de strings
    movies_list_str = []
    for movie in movies_list_bs:
        movies_list_str.append(movie.text)

    # la misma lista usando list comprehension
    # movies_list_str = [movie.text for movie in movies_list_bs]

    return movies_list_str

# Codigo para descargar una imagen
"""
imagen = "https://www.grupocine.com.uy:443/SIGE_CN/PublicTempStorage/multimedia/cropedFile05600879773351204crop_13749935f7ee4e719f4adee7d6a8a763.jpg"
r = requests.get(imagen, stream=True)
with open(f'images.png', 'wb') as f:
    shutil.copyfileobj(r.raw, f)
"""
