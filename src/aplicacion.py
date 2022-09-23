from clases import *
import os
import requests
import PySimpleGUI as sg
import operaciones_bbdd
import time
import log




def generar_archivos(busqueda:str, respuesta:str) -> str:
    """
        Creación de archivos tras obtener las respuestas
        A partir de un txt se creará el PDF con ConverApi
        Si falla el PDF se ofrece el txt
        Todo el contenido se guarda en la bbdd
        Retorna la ruta del pdf (elegida o por defecto)
        Retorna false si se produce error
    """
    ruta_busquedas = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'busquedas'))
    ruta_archivo_txt = os.path.join(ruta_busquedas, f'{busqueda}.txt')
    ruta_archivo_pdf = os.path.join(ruta_busquedas, f'{busqueda}.pdf')
    with open(ruta_archivo_txt, 'w+', encoding='utf-8') as manejador:
        manejador.write(respuesta)

    parametros = (
        ('Secret', 'OLzJh7PNaj245xfl'),
    )

    archivo = {
        'File': (f'{busqueda}.txt', open(ruta_archivo_txt, 'rb')),
        'StoreFile': (None, 'true'),
    }

    peticion = requests.post('https://v2.convertapi.com/convert/txt/to/pdf', params=parametros, files=archivo)
    if peticion.status_code != 200:
        return ''
    try:
        respuesta_api = peticion.json()
        url_descarga = respuesta_api["Files"][0]["Url"]
        peticion_descarga = requests.get(url_descarga)
        with open(ruta_archivo_pdf, 'wb+') as manejador:
            manejador.write(peticion_descarga.content)
        ### Insertar en base de datos los resultados
        operaciones_bbdd.insertar_resultados(busqueda, int(time.time()), respuesta, peticion_descarga.content)
        ruta_archivo_pdf_usuario = sg.popup_get_file('Guarda el informe generado en PDF',
            title = 'Guardar como',
            save_as = True,
            file_types = (('PDF', '*.pdf'),))
        if ruta_archivo_pdf_usuario != None:
            os.rename(ruta_archivo_pdf, ruta_archivo_pdf_usuario)
            return ruta_archivo_pdf_usuario
        else:
            return ruta_archivo_pdf
    except:
        return ''

#<--------------------------------------------------------  Lógica de la aplicación ----------------------------------------

""""
     1. Comprobar si la búsqueda se ha realizado antes
        Si es afirmativo recupera el contenido de la bbdd
        Se ofrece la posibilidad de su borrado para actualizarlo
     2. Búsqueda del término en:
        RAE, DuckDuckGo, Enciclonet, WordReference
     3. Generar PDF con los contenidos
     4. Aconsejar nueva búsqueda si no hay resultados
"""


def sabelotodo(busqueda:str) -> bool:
    busqueda_previa = operaciones_bbdd.busqueda_previa(busqueda)
    if busqueda_previa != '':
        ruta_busquedas = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'busquedas'))
        ruta_archivo_pdf = os.path.join(ruta_busquedas, f'{busqueda}.pdf')
        with open(ruta_archivo_pdf, 'wb+') as manejador:
            manejador.write(busqueda_previa)
        aviso_busqueda_previa = sg.popup_ok_cancel("Ya se realizó esta búsqueda. Pulsa 'OK' si quieres borrarla y hacer una nueva consulta",
            title = "Búsqueda realizada previamente")
        if aviso_busqueda_previa == 'OK':
            operaciones_bbdd.eliminar_busqueda(busqueda)
            return True
        print(f""" La búsqueda ya se realizó con anterioridad.
        Puedes encontrar el informe en PDF en {ruta_archivo_pdf}
        """)
        return True
    print('Acudo a mis fuentes de conocimiento.')
    rae = RAE(busqueda)
    rae.peticion(f'https://dle.rae.es/{busqueda}')
    rae.analizar()
    log.gestion_log(f'Búsqueda de {busqueda} en la RAE', 'info', True)
    duckduckgo = DuckDuckGo(busqueda)
    duckduckgo_parametros = {
        'q': busqueda,
        'kl': 'es-es',
        'format': 'json'
    }
    duckduckgo.peticion(f'https://api.duckduckgo.com/', duckduckgo_parametros)
    duckduckgo.analizar()
    log.gestion_log(f'Búsqueda de {busqueda} en DuckDuckGo', 'info', True)

    enciclonet = Enciclonet(busqueda)
    enciclonet.peticion(f'https://www.enciclonet.com/busqueda?q={busqueda}')
    enciclonet.analizar()
    log.gestion_log(f'Búsqueda de {busqueda} en Enciclonet', 'info', True)

    wordreference = WordReference(busqueda)
    wordreference.peticion(f'https://www.wordreference.com/definicion/{busqueda}')
    wordreference.analizar()
    log.gestion_log(f'Búsqueda de {busqueda} en WordReference', 'info', True)

    resultados = len(rae.contenido) + len(duckduckgo.contenido) + len(enciclonet.contenido) + len(wordreference.contenido)
    if resultados > 4:
        respuesta = f"""Definición de {busqueda}:
        {rae.contenido}
        {duckduckgo.contenido}
        {enciclonet.contenido}
        {wordreference.contenido}"""
        print(respuesta)
        generar = generar_archivos(busqueda, respuesta)
        if generar != '':
            log.gestion_log(f'Se ha generado un informe en PDF de la búsqueda en el directorio {generar}', 'info', False)
            return True
        else:
            ruta_txt = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'busquedas', f'{busqueda}.txt'))
            log.gestion_log(f'Ha fallado el sistema de generación de PDF. Busca el siguiente archivo de texto: {ruta_txt}', 'warning', True)
    else:
        log.gestion_log(f'El término {busqueda} no ha ofrecido ningún resultado', 'warning', True)
        return False