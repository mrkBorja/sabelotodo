### Sabelotodo

Tenemos que desarrollar una aplicación que recoja información de Internet y nos responda con la máxima información posible sobre una palabra.

❑Debe de tener varias fuentes de información.
❑Tiene que tener cache con las búsquedas anteriores.
❑Podrá generar un PDF con la información que genere.


Opciones cerradas

La evaluación es distinta, ya que pediré cuestiones importantes en los ejercicios.

Hasta 6 puntos en
❑Programación orientada a objetos
❑Almacenamiento de datos (ficheros o base de datos)
❑Funciones❑Que la aplicación no tenga errores

Hasta 4 puntos en
❑Ofrecer la aplicación en varios idiomas
❑Validación de datos
❑Optimización de recursos
❑Buenas practicas

Desarrollo de la Aplicación

Aplicación desarrollada que recopila información sobre un término en español. Para ello se sirve de técnicas como el scraping y el uso de APIs. Se ofrece el resultado en formato PDF, aunque también es posible recuperar un archivo txt.
La aplicación tiene fines didácticos. Se recomienda la búsqueda de nombres comunes típicos que pueden aparecer en cualquier diccionario (perro, ardilla, tortuga).
La lógica de la aplicación es la siguiente:

- Comprobar si la búsqueda se ha realizado antes. Si es afirmativo recupera el contenido de la bbdd.Se ofrece la posibilidad de su borrado para actualizarlo
- Búsqueda del término en: RAE, DuckDuckGo, Enciclonet, WordReference
- Generar PDF con los contenidos
- Aconsejar nueva búsqueda si no hay resultados

El trabajo de GUI o interfaz gráfica se ha hecho con PySimpleGUI, un wrapper para Tkinter. Se ha utilizado un tema propio, campos de texto, botones, un output para retroalimentar los procesos, ventanas emergentes de confirmación, selector de archivos...
La lógica de las peticiones HTML a las páginas de donde se extrae la información se ha diseñado siguiendo los patrones de programación de orientación a objetos y el uso de herencia, métodos, etc.
Para la base de datos se ha utilizado sqlite3 y hay ejemplos de las consultas típicas (crear tablas, select, insert into, delete). Todas las consultas son "prepared statements" para evitar la inyección SQL que puede ocasionarse al utilizar inputs de texto por parte del usuario.
Existe un sistema de registro de logs en ./logs/logs.txt. Los campos se separan con punto y coma (;) para facilitar su lectura en hojas de cálculo como Microsoft Excel o Google Spreadsheet.
Aunque se ha intentado aprovechar al máximo el uso de Python Basico, son necesarios algunos paquetes o librerias externas: requests (utilizado para las peticiones http), beatifulsoup4 (parseado HTML) y PySimpleGUI como wrapper de Tkinter. Las 3 librerias son completamente básicas en el desarrollo y programación de Python.



LIBRERIAS NECESARIAS E INSTRUCCIONES DE INSTALACIÓN

En el caso de sistema Linux/GNU:


pip3 install requests
pip3 install beautifulsoup4
pip3 install PySimpleGUI

```
En el caso de Windows:


pip install requests
pip install beautifulsoup4
pip install PySimpleGUI

```
Para iniciar la aplicación debe utilizarse el siguiente comando desde la carpeta SRC:


python3 main.py

```

En el caso de Windows:



py main.py

```



RECURSOS

Stakeroverflow
El libro de Python
Aprende Python en un fin de semana
La web del programador
Grupos Telegram














B.Fajardo