import requests
from bs4 import BeautifulSoup
import log

#<--------------------------------------------------------------Clases de las FUNCIONES DE BUSQUEDA ----------------------------------------------------

class Web:
    """ Construcción de la clase y petición """
    def __init__(self, concepto:str):
        self.concepto = concepto
    def peticion(self, url:str, parametros:dict={}):
        cabeceras = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }
        httpreq = requests.get(url, params=parametros, headers=cabeceras)
        if httpreq.status_code != 200:
            self.error = True
            self.respuesta = ''
        self.error = False
        self.respuesta = httpreq

class RAE(Web):
    """ Análisis de los respuesta de la peticion (scraping) """
    def analizar(self):
        if self.error:
            self.contenido = ''
        else:
            html_contenido = BeautifulSoup(self.respuesta.text, 'html.parser')
            acepciones = html_contenido.find_all('p', {'class': 'j'})
            contenido = ''
            for acepcion in acepciones:
                contenido += acepcion.text
            self.contenido = contenido

class DuckDuckGo(Web):
    """ Análisis de los respuesta de la peticion (json) """
    def analizar(self):
        if self.error:
            self.contenido = ''
        else:
            json_contenido = self.respuesta.json()
            try:
                self.contenido = json_contenido["AbstractText"]
            except:
                self.error = True
                self.contenido = ''

class Enciclonet(Web):
    """ Análisis de los respuesta de la peticion (scraping) """
    def analizar(self):
        if self.error:
            self.contenido = ''
        else:
            html_contenido = BeautifulSoup(self.respuesta.text, 'html.parser')
            try:
                acepcion = html_contenido.find('div', {'id': 'qryList'}).find('dd').text
                self.contenido = acepcion
            except:
                self.error = True
                self.contenido = ''

class WordReference(Web):
    """ Análisis de los respuesta de la peticion (scraping) """
    def analizar(self):
        if self.error:
            self.contenido = ''
        else:
            html_contenido = BeautifulSoup(self.respuesta.text, 'html.parser')
            try:
                acepciones_contenido = ''
                acepciones = html_contenido.find_all('ol', {'class': 'entry'})
                for acepcion in acepciones:
                    entradas = acepcion.find_all('li')
                    for entrada in entradas:
                        acepciones_contenido += entrada.text
                self.contenido = acepciones_contenido
            except:
                self.error = True
                self.contenido = False