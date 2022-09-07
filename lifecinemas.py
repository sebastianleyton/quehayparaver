import scraping_helper
import bs4
import requests

URL = "https://lifecinemas.com.uy/pelicula/cartelera"
SELECTOR_CSS_MOVIE_LINKS = "#ultimos_estrenos .movie-container a"
URL_BASE = "https://lifecinemas.com.uy/"
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
    for movie_url in movies_links_str:
        if "/festival/" in movie_url:
            print(movie_url)
            continue
        movie_url_full = URL_BASE + movie_url
        #print(movie_url_full)
        html = bs4.BeautifulSoup(requests.get(movie_url_full).text, features="html.parser")
        movie_full_desc = html.select(SELECTOR_CSS_MOVIE)
        #print(movie_full_desc)

get_links()