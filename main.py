from flask import Flask, render_template
import grupocine as gc
import lifecinemas as lc


app = Flask(__name__)

@app.route('/')
def hello_world():
    #pelis_grupocine = gc.get_data()
    #pelis_lifecinema = lc.get_data()
    dict = [
            {"titulo": "Dragon ball", "descripcion":"la peli de dbz", "duracion":"120"},
            {"titulo": "Minions", "descripcion":"la peli de los minions", "duracion":"20"},
            {"titulo": "NOP", "descripcion": "la peli ovnis", "duracion": "620"}
            ]
    return render_template('index.html', pelis_lifecinema=dict)
    #return render_template('index.html')
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)