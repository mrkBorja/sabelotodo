#!/usr/bin/python3
import PySimpleGUI as sg
import aplicacion
import operaciones_bbdd
import log

#<-------------------------------------------  Lógica de la Interfaz gráfica ----------------------------------------------------------

"""
         PySimpleGUI es un wrapper para Tkinter
         Elementos principales de la GUI:
            key busqueda (texto)
            key buscar (botón)
"""


def main():

    sg.theme('DarkAmber')

    layout = [
        [sg.Text('¡Hola! Soy un Sabelotodo !!! =)')],
        [sg.Text('Pregunta y te daré respuesta. Mi especialidad es definir términos. \
        \nEvita, por favor, los nombres propios, adjetivos, adverbios, etc. \
        \nEscribe un concepto por búsqueda.')],
        [sg.InputText(key='busqueda', size=(70, None))],
        [sg.Button('¿Que quieres Saber? ...', key='buscar')],
        [sg.Output(size=(70,10))],
        [sg.Text('Borja Fajardo - Proyecto Final 2021 ', size=(70, None), justification='center')]
        ]
    ventana = sg.Window('Sabelotodo V.1.0', layout)
    while True:
        evento, valores = ventana.read()
        if evento == sg.WIN_CLOSED:
            log.gestion_log(f'Aplicación cerrada', 'info', False) 
            break
        if evento == 'buscar':
            if valores["busqueda"] != '':
                aplicacion.sabelotodo(valores["busqueda"].lower().strip())
            else:
                log.gestion_log('No se ha definido ningún término de búsqueda', 'warning', True)
    ventana.close()


if __name__ == "__main__":
    log.gestion_log('Aplicación iniciada', 'info', False)
    operaciones_bbdd.crear_base_datos()
    main()