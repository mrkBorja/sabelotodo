import sqlite3
import os
import log

#<------------------------------------------------------- Funciones para la BBDD creada desde la linea de codigo. ------------------------------

def ruta_base_datos() -> str:
    """ Devuelve la ruta a la bbdd"""
    ruta_raiz = os.path.dirname(os.path.realpath(__file__))
    ruta_base_datos = os.path.join(ruta_raiz, 'bbdd.sqlite3')
    return ruta_base_datos

def crear_base_datos() -> bool:
    """ Creación de las 2 tablas de la bbdd"""
    conexion = sqlite3.connect(ruta_base_datos())
    cursor = conexion.cursor()
    consulta = """
        CREATE TABLE IF NOT EXISTS busquedas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            busqueda TEXT NOT NULL,
            fecha INTEGER NOT NULL,
            contenido TEXT
        );
    """
    cursor.execute(consulta)
    consulta = """
        CREATE TABLE IF NOT EXISTS pdf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            busqueda_id INTEGER KEY REFERENCES busquedas(id),
            contenido_bytes BLOB
        );
    """
    cursor.execute(consulta)
    conexion.commit()
    return True

def busqueda_previa(busqueda:str) -> str:
    """ Comprobación para determinar si la consulta se ha realizado anteriormente
    Retorna False en caso de que se haya realizado
    Retorna el contenido en bytes del PDF por si debe generarse nuevamente
    """
    conexion = sqlite3.connect(ruta_base_datos())
    cursor = conexion.cursor()
    consulta = """
        SELECT pdf.contenido_bytes FROM busquedas 
        JOIN pdf ON busquedas.id = pdf.busqueda_id
        WHERE busqueda = ?
    """
    argumentos = (busqueda,)
    cursor.execute(consulta, argumentos)
    resultados = cursor.fetchall()
    if len(resultados) > 0:
        log.gestion_log(f'Búsqueda de {busqueda} realizada previamente', 'info', False)
        return resultados[0][0]
    return ''

def insertar_resultados(busqueda:str, fecha:int, contenido:str, contenido_bytes:bytes) -> bool:
    """ Inserta una nueva búsqueda """
    conexion = sqlite3.connect(ruta_base_datos())
    cursor = conexion.cursor()
    consulta = """
        INSERT INTO busquedas (busqueda, fecha, contenido) VALUES (?, ?, ?)
    """
    argumentos = (busqueda, fecha, contenido)
    cursor.execute(consulta, argumentos)
    conexion.commit()
    consulta = """
        SELECT id FROM busquedas WHERE busqueda = ?
    """
    argumentos = (busqueda,)
    cursor.execute(consulta, argumentos)
    resultados = cursor.fetchall()
    id_busqueda = resultados[0][0]
    consulta = """
        INSERT INTO pdf (busqueda_id, contenido_bytes) VALUES (?, ?)
    """
    argumentos = (id_busqueda, contenido_bytes)
    cursor.execute(consulta, argumentos)
    conexion.commit()
    log.gestion_log(f'Resultados de {busqueda} incorporados en la base de datos', 'info', False)
    return True

def eliminar_busqueda(busqueda:str) -> bool:
    """ Elimina una búsqueda realizada previamente """
    conexion = sqlite3.connect(ruta_base_datos())
    cursor = conexion.cursor()
    consulta = """
        SELECT id FROM busquedas WHERE busqueda = ?
    """
    argumentos = (busqueda,)
    cursor.execute(consulta, argumentos)
    resultados = cursor.fetchall()
    id_busqueda = resultados[0][0]
    consulta = """
        DELETE FROM busquedas WHERE id = ?
    """
    argumentos = (id_busqueda,)
    cursor.execute(consulta, argumentos)
    conexion.commit()
    consulta = """
        DELETE FROM pdf WHERE busqueda_id = ?
    """
    argumentos = (id_busqueda,)
    cursor.execute(consulta, argumentos)
    conexion.commit()
    log.gestion_log(f'Búsqueda de {busqueda} eliminada de la base de datos', 'info', True)
    return True
