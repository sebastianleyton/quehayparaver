import sqlite3
from definitions import DB_PATH


class DBConnection:
    def __init__(self, db_path):
        # Se crea el objeto DBConnection y se conecta a la base de datos que está en db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        # Se ejecuta la query con el cursor y se hace commit
        if not params:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.conn.commit()

    def query(self, query, params=None):
        # Se ejecuta la query y se devuelven los resultados en una lista
        result_list = []
        if not params:
            result = self.cursor.execute(query)
        else:
            result = self.cursor.execute(query, params)

        for row in result.fetchall(): # Recorro los rows devueltos por la query
            result_dict = {}
            for r in row.keys():
                result_dict[r] = row[r]
            result_list.append(result_dict)
        return result_list

    def get_all_pelis(self):
        result = self.query("select * from movies")
        return result

    def insertar_peli(self, titulo, descripction):
        tpl = (titulo, descripction)
        query = "insert into movies (title, description) values (?, ?)"
        self.execute(query, tpl)

    def insertar_muchas_pelis(self, lista_pelis):
        for peli in lista_pelis:
            self.insertar_peli(peli['titulo'], peli['descripcion'])

    def actualizar_descripcion(self, id, nueva_descripcion):
        tpl = (nueva_descripcion, id)
        query = "update movies set description = ? where id = ?"
        self.execute(query, tpl)

    def actualizar_titulo(self, id, nuevo_titulo):
        tpl = (nuevo_titulo, id)
        query = "update movies set title = ? where id = ?"
        self.execute(query, tpl)

