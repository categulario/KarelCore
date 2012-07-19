PyRel
=====

Karel el robot, escrito completamente en python. Por [@Categulario](https://twitter.com/categulario)

El objetivo de este proyecto es ofrecer el lenguaje ''Karel'' orientado al aprendizaje de la programación para todas las plataformas y sin requerir librerías privativas.

Hasta el momento sólo está soportada la sintaxis 'pascal' de Karel, algunos cambios en la sintaxis pueden haber sido influenciados por la sintaxis de Python, sin embargo cualquier código en la sintaxis original de Karel será reconocido (Excepto por los códigos con comentarios de una sola línea con `//`).

Necesito ayuda!
---------------

Si conoces Karel el robot y tienes códigos escritos en PASCAL (el pascal de Karel) puedes hacer dos cosas por mi:

* Probar que los codigos sean correctamente reconocidos por el analizador sintáctico.
* Hecho lo anterior, poner un error de sintaxis en los códigos y ver si el analizador lo reconoce.

Cualquier irregularidad me avisan a a.wonderful.code@gmail.com

Testing
-------

Para probar alguno de los componentes hay que ir a la carpeta `/clases` y correr el script elegido

Ejemplo:

`$ python kgrammar.py`

O también

`$ python ktokenizer.py`

También es posible pasar un archivo como parámetro, se supondrá que el archivo contiene un programa en karel. En la misma carpeta que los scripts existen archivos con código karel para pruebas.

* `codigo.karel` contiene un programa correcto sintácticamente
* `malo.karel` tiene algún error de sintaxis

Un ejemplo de cómo pasar un archivo como parámetro:

`$ python kgrammar.py codigo.karel`

TODO
----

Algunas buenas ideas por implementar en este proyecto

* Implementar la GUI del IDE.
* Poner una sección con un tutorial de Karel a modo de 'misiones'.
* Hacer un editor de mundos.
* Soportar la sintaxis Java de pascal.
* Terminar la clase `krunner.py`.
* Ajustar `ktokenizer.py` para agrupar símbolos como '++', '--', '&&', '||', '==', '//', '/\*', '\*/' etc...

Notas
-----

* Añadí (para evitar conflictos y confusiones frecuentes) soporte para 'repetir' y 'repite' como bucles, ambos con la misma funcionalidad. Cualquier comentario me avisan. (Cuando competí en la OMI no saben cuánta lata me dio esto :) )
* Trato de hacer los mensajes de error lo más comprensibles posible, se aceptan comentarios.
* Se pueden hacer comentarios en una línea usando `#`, los comentarios de varias lineas se hacen con `/`, `"` y `'`.
* Los procedimientos tienen soporte para varias variables, quién sabe, con suerte esto abre las puertas a mas problemas.
* También en un delirio de locura podría incluir las variables `verdadero` y `falso`, actualmente ya son palabras reservadas.
* Se usará Scintilla para el editor de código y pygame para el visor del mundo, la interfaz correrá por cuenta de wxPython.
* Provisionalmente estoy usando JSON para el almacenamiento de los mundos, es la magia de los diccionarios en python.

Todo el desarrollo del proyecto se llevó a cabo en Debian Wheezy, Ubuntu 12.04 y OpenSUSE usando el IDE Geany Tavira. Otras herramientas incluyen Git como sistema de control de versiones, Git-cola como interfaz para Git, y la magia del escritorio Gnome shell!!

