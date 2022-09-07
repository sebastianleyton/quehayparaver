import scraping_helper

URL = "https://www.grupocine.com.uy/SIGE_CN/servlet/com.sigecn.comprar"
SELECTOR_CSS = "select#vPELICULAID option:not([selected])"


def get_data():
    title_list = scraping_helper.get_titles_list(URL, SELECTOR_CSS)
    return title_list
