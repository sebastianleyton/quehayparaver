import os.path
from flask import Flask, render_template
from definitions import JSON_PATH
import json
import ast

#from functions.scraping.lifecinemas import get_links

# from functions.scraping import grupocine
# from functions.scraping import lifecinemas
app = Flask(__name__)


@app.route('/')
def hello_world():
    # pelis_grupocine = grupocine.get_data()
    # pelis_lifecinema = lifecinemas.get_links()
    json_exists = os.path.exists(JSON_PATH)
    if not json_exists:
        pelis_lifecinema = '[]'
    else:
        pelis_lifecinema = cargar_json_como_lista_dictionarios(JSON_PATH)

    return render_template('index.html', pelis_lifecinema=pelis_lifecinema)
    # return render_template('index.html')

def cargar_json_como_lista_dictionarios(path):
    with open(path, "r") as json_file:
        contenido_del_archivo = json_file.read()
    contenido_del_archivo = ast.literal_eval(contenido_del_archivo)
    return contenido_del_archivo


# def arreglar_caracteres_en_titulos(lista):
#     print(lista)
#     for lala in lista:
#         print(lala)
#         if 'SIGNODEPREGUNTA' in lala['titulo']:
#             lala['titulo'] = lala['titulo'].replace('SIGNODEPREGUNTA', '?')
#         if 'DOSPUNTOS' in lala['titulo']:
#             lala['titulo'] = lala['titulo'].replace('DOSPUNTOS', ':')
#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

