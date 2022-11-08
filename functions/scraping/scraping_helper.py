import shutil
import os
import requests
import datetime
from selenium import webdriver
from definitions import MOVIE_IMAGES_PATH
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By





class Scraper:
    def __init__(self):
        print("Abriendo navegador")
        self.chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def cargar_sitio(self, url):
        print(f"Cargando sitio: {url}")
        self.chrome.get(url)

    def obtener_objeto_por_css_selector(self, css_selector):
        print(f"Obteniendo elemento con selector: {css_selector}")
        elemento_html = self.chrome.find_element(By.CSS_SELECTOR, css_selector)
        return elemento_html

    def obtener_objeto_por_xpath(self, xpath_selector):
        print(f"Obteniendo elemento con selector: {xpath_selector}")
        elemento_html = self.chrome.find_element(By.XPATH, xpath_selector)
        return elemento_html

    def obtener_lista_objetos_por_css_selector(self, css_selector):
        print(f"Obteniendo elementos con selector: {css_selector}")
        elementos_html = self.chrome.find_elements(By.CSS_SELECTOR, css_selector)
        print(f"Obtenidos {len(elementos_html)} elementos")
        return elementos_html

    def obtener_lista_objetos_por_xpath(self, xpath_selector):
        print(f"Obteniendo elementos con selector: {xpath_selector}")
        elementos_html = self.chrome.find_elements(By.XPATH, xpath_selector)
        print(f"Obtenidos {len(elementos_html)} elementos")
        return elementos_html

    def extraer_texto(self, css_selector):
        print("Extrayendo texto")
        elemento_html = self.obtener_objeto_por_css_selector(css_selector)
        texto = elemento_html.text
        print(f"Texto extraido: {texto}")
        return texto

    def extraer_texto_por_xpath(self, xpath_selector):
        print("Extrayendo texto")
        elemento_html = self.obtener_objeto_por_xpath(xpath_selector)
        texto = elemento_html.text
        print(f"Texto extraido: {texto}")
        return texto

    def extraer_texto_de_lista(self, css_selector):
        print("Extrayendo texto")
        elemento_htmls = self.obtener_lista_objetos_por_css_selector(css_selector)
        lista_texto = []
        for e in elemento_htmls:
            lista_texto.append(e.text)
        print(f"Cantidad textos extraidos: {len(lista_texto)}")
        return lista_texto

    def extraer_texto_de_lista_por_xpath(self, xpath_selector):
        print("Extrayendo texto")
        elemento_htmls = self.obtener_lista_objetos_por_xpath(xpath_selector)
        lista_texto = []
        for e in elemento_htmls:
            lista_texto.append(e.text)
        print(f"Cantidad textos extraidos: {len(lista_texto)}")
        return lista_texto

    def extraer_url(self, css_selector):
        print("Extrayendo URL")
        elemento_html = self.obtener_objeto_por_css_selector(css_selector)
        url = elemento_html.get_attribute('href')
        print(f"URL extraida: {url}")
        return url

    def extraer_url_por_xpath(self, xpath_selector):
        print("Extrayendo URL")
        elemento_html = self.extraer_texto_de_lista_por_xpath(xpath_selector)
        url = elemento_html.get_attribute('href')
        print(f"URL extraida: {url}")
        return url

    def extraer_url_de_lista(self, css_selector):
        print("Extrayendo urls")
        elemento_htmls = self.obtener_lista_objetos_por_css_selector(css_selector)
        lista_urls = []
        for e in elemento_htmls:
            lista_urls.append(e.get_attribute('href'))
        print(f"Cantidad URLs extraidos: {len(lista_urls)}")
        return lista_urls

    def extraer_url_de_lista_por_xpath(self, xpath_selector):
        print("Extrayendo urls")
        elemento_htmls = self.obtener_lista_objetos_por_xpath(xpath_selector)
        lista_urls = []
        for e in elemento_htmls:
            lista_urls.append(e.get_attribute('href'))
        print(f"Cantidad URLs extraidos: {len(lista_urls)}")
        return lista_urls

    def extraer_atributo_generico(self, css_selector, atributo):
        print(f"Extrayendo atributo {atributo}")
        elemento_html = self.obtener_objeto_por_css_selector(css_selector)
        atributo = elemento_html.get_attribute(atributo)
        print(f"Atributo extraido: {atributo}")
        return atributo

    def extraer_atributo_generico_por_xpath(self, xpath_selector, atributo):
        print(f"Extrayendo atributo {atributo}")
        elemento_html = self.obtener_objeto_por_xpath(xpath_selector)
        atributo = elemento_html.get_attribute(atributo)
        print(f"Atributo extraido: {atributo}")
        return atributo

    def extraer_lista_atributo_generico(self, css_selector, atributo):
        print(f"Extrayendo atributo: {atributo}")
        elemento_htmls = self.obtener_lista_objetos_por_css_selector(css_selector)
        lista_attr = []
        for e in elemento_htmls:
            lista_attr.append(e.get_attribute(atributo))
        print(f"Cantidad attr {atributo} extraidos: {len(lista_attr)}")
        return lista_attr

    def extraer_lista_atributo_generico_por_xpath(self, xpath_selector, atributo):
        print(f"Extrayendo atributo: {atributo}")
        elemento_htmls = self.obtener_lista_objetos_por_xpath(xpath_selector)
        lista_attr = []
        for e in elemento_htmls:
            lista_attr.append(e.get_attribute(atributo))
        print(f"Cantidad attr {atributo} extraidos: {len(lista_attr)}")
        return lista_attr

    def download_image(url, imagen, save_path=os.path.join(MOVIE_IMAGES_PATH)):
        # Crear timestamp para la carpeta donde se va a guardar
        # si la carpeta no existe, crearla, si existe, no hacer nada
        # pasar parametero timestamp al nombre de la imagen para guardar en la db
        timestamp = datetime.date.today().strftime('%m-%d')

        # Crear directorio con la fecha de hoy si no existe
        if not os.path.exists(os.path.join(save_path, timestamp)):
            os.makedirs(os.path.join(save_path, timestamp))

        # Crear directorio con la fecha de hoy si no existe
        if not os.path.exists(os.path.join(save_path, 'current')):
            os.makedirs(os.path.join(save_path, 'current'))

        r = requests.get(url, stream=True)
        print(r.status_code)
        filename = os.path.join(save_path, timestamp, f'{imagen}.png')
        print(filename)
        with open(filename, 'w+b') as f:
            shutil.copyfileobj(r.raw, f)

        filename = os.path.join(save_path, 'current', f'{imagen}.png')
        print(filename)
        with open(filename, 'w+b') as f:
            shutil.copyfileobj(r.raw, f)

    def cerrar_navegador(self):
        self.chrome.close()

def normalizar_duracion(duracion_text):
    duracion_text = str(duracion_text)
    if "h" in duracion_text:
        if "m" in duracion_text:
            x = duracion_text.split('h')
            hora = int(x[0])
            minutos = int(x[1].replace('m', ''))
            return hora * 60 + minutos
        return int(duracion_text.replace('h', '')) * 60
    return int(duracion_text.replace('m', ''))

def download_image(url, imagen, save_path=os.path.join(MOVIE_IMAGES_PATH)):
    # Crear timestamp para la carpeta donde se va a guardar
    # si la carpeta no existe, crearla, si existe, no hacer nada
    # pasar parametero timestamp al nombre de la imagen para guardar en la db
    timestamp = datetime.date.today().strftime('%m-%d')

    # Crear directorio con la fecha de hoy si no existe
    if not os.path.exists(os.path.join(save_path, timestamp)):
        os.makedirs(os.path.join(save_path, timestamp))

    # Crear directorio con la fecha de hoy si no existe
    if not os.path.exists(os.path.join(save_path, 'current')):
        os.makedirs(os.path.join(save_path, 'current'))

    r = requests.get(url, stream=True)
    print(r.status_code)
    filename = os.path.join(save_path, timestamp, f'{imagen}.png')
    print(filename)
    with open(filename, 'w+b') as f:
        shutil.copyfileobj(r.raw, f)

    filename = os.path.join(save_path, 'current', f'{imagen}.png')
    print(filename)
    with open(filename, 'w+b') as f:
        shutil.copyfileobj(r.raw, f)