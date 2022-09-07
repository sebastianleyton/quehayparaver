import scraping_helper

URL = "https://lifecinemas.com.uy/pelicula/cartelera"
SELECTOR_CSS = "ul#ultimos_estrenos li div.text-cont-movie h1"


def get_data():
    title_list = scraping_helper.get_titles_list(URL, SELECTOR_CSS)
    return title_list
