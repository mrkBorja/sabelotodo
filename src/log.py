import logging
import os

#<------------------------------------------------ Creo LOG para el Historico de la App

def gestion_log(informacion:str, tipo:str, gui:bool) -> bool:
    """
        Función para el logging (en archivo separado por ; para visualización en Excel) y por pantalla
    """
    logging.basicConfig(
        format = '%(asctime)s;%(levelname)s;%(message)s',
        level  = logging.INFO,
        filename = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'logs', 'logs.txt')),
        filemode = "a"
    )
    if tipo == 'warning':
        logging.warning(informacion)
    else:
        logging.info(informacion)
    if gui == True:
        print(informacion)
    return True