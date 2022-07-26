import shutil
import os
import requests
import datetime
from selenium import webdriver
from definitions import MOVIE_IMAGES_PATH, LOG_PATH
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, log_level=3):
        self.log_level = log_level
        self.chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        log("Abriendo navegador", 3, self.log_level)

    def cargar_sitio(self, url):
        log(f"Cargando sitio: {url}", 3, self.log_level)
        self.chrome.get(url)

    def obtener_objeto_por_css_selector(self, css_selector):
        log(f"Obteniendo elemento con selector: {css_selector}", 3, self.log_level)
        elemento_html = self.chrome.find_element(By.CSS_SELECTOR, css_selector)
        return elemento_html

    def obtener_objeto_por_xpath(self, xpath_selector):
        log(f"Obteniendo elemento con selector: {xpath_selector}", 3, self.log_level)
        elemento_html = self.chrome.find_element(By.XPATH, xpath_selector)
        return elemento_html

    def obtener_lista_objetos_por_css_selector(self, css_selector):
        log(f"Obteniendo elementos con selector: {css_selector}", 3, self.log_level)
        elementos_html = self.chrome.find_elements(By.CSS_SELECTOR, css_selector)
        log(f"Obtenidos {len(elementos_html)} elementos", 3, self.log_level)
        return elementos_html

    def obtener_lista_objetos_por_xpath(self, xpath_selector):
        log(f"Obteniendo elementos con selector: {xpath_selector}", 3, self.log_level)
        elementos_html = self.chrome.find_elements(By.XPATH, xpath_selector)
        log(f"Obtenidos {len(elementos_html)} elementos", 3, self.log_level)
        return elementos_html

    def extraer_texto(self, css_selector):
        log("Extrayendo texto", 3, self.log_level)
        elemento_html = self.obtener_objeto_por_css_selector(css_selector)
        texto = elemento_html.text
        log(f"Texto extraido: {texto}", 3, self.log_level)
        return texto

    def extraer_texto_por_xpath(self, xpath_selector):
        log("Extrayendo texto", 3, self.log_level)
        elemento_html = self.obtener_objeto_por_xpath(xpath_selector)
        texto = elemento_html.text
        log(f"Texto extraido: {texto}", 3, self.log_level)
        return texto

    def extraer_texto_de_lista(self, css_selector):
        log("Extrayendo texto", 3, self.log_level)
        elemento_htmls = self.obtener_lista_objetos_por_css_selector(css_selector)
        lista_texto = []
        for e in elemento_htmls:
            lista_texto.append(e.text)
        log(f"Cantidad textos extraidos: {len(lista_texto)}", 3, self.log_level)
        return lista_texto

    def extraer_texto_de_lista_por_xpath(self, xpath_selector):
        log("Extrayendo texto", 3, self.log_level)
        elemento_htmls = self.obtener_lista_objetos_por_xpath(xpath_selector)
        lista_texto = []
        for e in elemento_htmls:
            lista_texto.append(e.text)
        log(f"Cantidad textos extraidos: {len(lista_texto)}", 3, self.log_level)
        return lista_texto

    def extraer_url(self, css_selector):
        log("Extrayendo URL", 3, self.log_level)
        elemento_html = self.obtener_objeto_por_css_selector(css_selector)
        url = elemento_html.get_attribute('href')
        log(f"URL extraida: {url}", 3, self.log_level)
        return url

    def extraer_url_por_xpath(self, xpath_selector):
        log("Extrayendo URL", 3, self.log_level)
        elemento_html = self.extraer_texto_de_lista_por_xpath(xpath_selector)
        url = elemento_html.get_attribute('href')
        log(f"URL extraida: {url}", 3, self.log_level)
        return url

    def extraer_url_de_lista(self, css_selector):
        log("Extrayendo urls", 3, self.log_level)
        elemento_htmls = self.obtener_lista_objetos_por_css_selector(css_selector)
        lista_urls = []
        for e in elemento_htmls:
            lista_urls.append(e.get_attribute('href'))
        log(f"Cantidad URLs extraidos: {len(lista_urls)}", 3, self.log_level)
        return lista_urls

    def extraer_url_de_lista_por_xpath(self, xpath_selector):
        log("Extrayendo urls", 3, self.log_level)
        elemento_htmls = self.obtener_lista_objetos_por_xpath(xpath_selector)
        lista_urls = []
        for e in elemento_htmls:
            lista_urls.append(e.get_attribute('href'))
        log(f"Cantidad URLs extraidos: {len(lista_urls)}", 3, self.log_level)
        return lista_urls

    def extraer_atributo_generico(self, css_selector, atributo):
        log(f"Extrayendo atributo {atributo}", 3, self.log_level)
        elemento_html = self.obtener_objeto_por_css_selector(css_selector)
        atributo = elemento_html.get_attribute(atributo)
        log(f"Atributo extraido: {atributo}", 3, self.log_level)
        return atributo

    def extraer_atributo_generico_por_xpath(self, xpath_selector, atributo):
        log(f"Extrayendo atributo {atributo}", 3, self.log_level)
        elemento_html = self.obtener_objeto_por_xpath(xpath_selector)
        atributo = elemento_html.get_attribute(atributo)
        log(f"Atributo extraido: {atributo}", 3, self.log_level)
        return atributo

    def extraer_lista_atributo_generico(self, css_selector, atributo):
        log(f"Extrayendo atributo: {atributo}", 3, self.log_level)
        elemento_htmls = self.obtener_lista_objetos_por_css_selector(css_selector)
        lista_attr = []
        for e in elemento_htmls:
            lista_attr.append(e.get_attribute(atributo))
        log(f"Cantidad attr {atributo} extraidos: {len(lista_attr)}", 3, self.log_level)
        return lista_attr

    def extraer_lista_atributo_generico_por_xpath(self, xpath_selector, atributo):
        log(f"Extrayendo atributo: {atributo}", 3, self.log_level)
        elemento_htmls = self.obtener_lista_objetos_por_xpath(xpath_selector)
        lista_attr = []
        for e in elemento_htmls:
            lista_attr.append(e.get_attribute(atributo))
        log(f"Cantidad attr {atributo} extraidos: {len(lista_attr)}", 3, self.log_level)
        return lista_attr

    # def download_image(url, imagen, save_path=os.path.join(MOVIE_IMAGES_PATH)):
    #     # Crear timestamp para la carpeta donde se va a guardar
    #     # si la carpeta no existe, crearla, si existe, no hacer nada
    #     # pasar parametero timestamp al nombre de la imagen para guardar en la db
    #     timestamp = datetime.date.today().strftime('%m-%d')
    #
    #     # Crear directorio con la fecha de hoy si no existe
    #     if not os.path.exists(os.path.join(save_path, timestamp)):
    #         os.makedirs(os.path.join(save_path, timestamp))
    #
    #     # Crear directorio con la fecha de hoy si no existe
    #     if not os.path.exists(os.path.join(save_path, 'current')):
    #         os.makedirs(os.path.join(save_path, 'current'))
    #
    #     r = requests.get(url, stream=True)
    #     print(r.status_code)
    #     filename = os.path.join(save_path, timestamp, f'{imagen}.png')
    #     print(filename)
    #     with open(filename, 'w+b') as f:
    #         shutil.copyfileobj(r.raw, f)
    #
    #     filename = os.path.join(save_path, 'current', f'{imagen}.png')
    #     print(filename)
    #     with open(filename, 'w+b') as f:
    #         shutil.copyfileobj(r.raw, f)

    def cerrar_navegador(self):
        self.chrome.close()


    def normalizar_duracion(self, duracion_text):
        duracion_text = str(duracion_text)
        if "h" in duracion_text:
            if "m" in duracion_text:
                x = duracion_text.split('h')
                hora = int(x[0])
                minutos = int(x[1].replace('m', ''))
                return hora * 60 + minutos
            return int(duracion_text.replace('h', '')) * 60
        elif "m" in duracion_text:
            x = duracion_text.split('m')
            minutos = int(x[0])
            return minutos
        else:
            return int(duracion_text)

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
    filename = os.path.join(save_path, timestamp, f'{imagen}.png')
    with open(filename, 'w+b') as f:
        shutil.copyfileobj(r.raw, f)

    filename = os.path.join(save_path, 'current', f'{imagen}.png')
    with open(filename, 'w+b') as f:
        shutil.copyfileobj(r.raw, f)


def log(msg, log_type, set_level):
    if log_type > set_level:
        return

    if log_type == 1:
        msg = f"[ERROR] - {msg}"
    elif log_type == 2:
        msg = f"[WARNING] - {msg}"
    elif log_type == 3:
        msg = f"[INFO] - {msg}"

    time = datetime.date.today().strftime('%m-%d-%Y')
    timestamp = datetime.datetime.today().strftime('%H:%M:%S')
    filename = f"log_{time}.txt"
    with open(os.path.join(LOG_PATH, filename), 'a') as f:
        f.write(f"{timestamp} - {msg}\n")