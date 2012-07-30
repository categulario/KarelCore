PyRel
=====

Xalapa, Ver. 2012

Descripción
-----------

Te gustaba tanto jugar con Karel que decidiste que lo querías en tu plataforma favorita: Linux, así que programaste como poseído en python hasta lograr que Karel corra en Linux, Windows, Mac, Solaris y cualquier otra bestia...

Problema
--------

Karel requiere algunas librerías privativas para correr, escribe un programa que no las requiera, y que permita ejecutar códigos de Karel en un mundo.

Consideraciones
---------------

* Karel necesita recursión para poder resolver problemas.
* Las estructuras se heredan del lenguaje en que es programado.
* Karel se lleva muy bien con los pingüinos.
* Un autómata finito o máquina de estado finito es un modelo computacional que realiza cómputos en forma automática sobre una entrada para producir una salida.
* No importa la posición ni orientación final de Karel.
* Solo tienes el verano para hacerlo.

Proyecto
--------

Karel el robot, escrito completamente en python. Por [@Categulario](https://twitter.com/categulario)

El objetivo de este proyecto es ofrecer el lenguaje ''Karel'' orientado al aprendizaje de la programación para todas las plataformas y sin requerir librerías privativas.

Hasta el momento sólo está soportada la sintaxis 'pascal' de Karel, algunos cambios en la sintaxis pueden haber sido influenciados por la sintaxis de Python, sin embargo cualquier código en la sintaxis original de Karel será reconocido (Excepto por los códigos con comentarios de una sola línea con `//`).

Necesito ayuda!
---------------

Si conoces Karel el robot y tienes códigos escritos en PASCAL (el pascal de Karel) puedes hacer dos cosas por mi:

* Probar que los codigos sean correctamente reconocidos por el analizador sintáctico.
* Hecho lo anterior, poner un error de sintaxis en los códigos y ver si el analizador lo reconoce.

Cualquier irregularidad me avisan a a.wonderful.code@gmail.com, información sobre cómo verificar la sintaxis de los archivos está abajo.

Testing
-------

Para probar alguno de los componentes hay que ejecutar el archivo `karel` en la carpeta raiz.

Ejemplo:

`$ python karel check -k archivo.karel`

O también

`$ python karel run -k archivo.karel`

Es posible obtener una poca de ayuda con:

`$ python karel --help`

TODO
----

Cosas importantes por hacer:

* Asegurar el buen funcionamiento de `sal-de-instruccion` y de `apagate` en `krunner` y `kgrammar`.
* Ajustar `ktokenizer.py` para agrupar símbolos como '++', '--', '&&', '||', '==', '//', '/\*', '\*/' etc...
* Implementar la ejecucion paso a paso o step_run.
* Implementar la GUI del IDE.
* Hacer un editor de mundos.
* Soportar la sintaxis Java de pascal.
* Extender la ayuda.

Algunas buenas ideas por implementar en este proyecto:

* Poner una sección con un tutorial de Karel a modo de 'misiones'.

Notas
-----

* Añadí (para evitar conflictos y confusiones frecuentes) soporte para 'repetir' y 'repite' como bucles, ambos con la misma funcionalidad. Cualquier comentario me avisan. (Cuando competí en la OMI no saben cuánta lata me dio esto :) )
* Trato de hacer los mensajes de error lo más comprensibles posible, se aceptan comentarios.
* Se pueden hacer comentarios en una línea usando `#`, los comentarios de varias lineas se hacen con `/`, `"` y `'`.
* Los procedimientos tienen soporte para varias variables, quién sabe, con suerte esto abre las puertas a mas problemas.
* También en un delirio de locura podría incluir las variables `verdadero` y `falso`, actualmente ya son palabras reservadas.
* Se usará Scintilla para el editor de código y pygame para el visor del mundo, la interfaz correrá por cuenta de wxPython.
* Provisionalmente estoy usando JSON para el almacenamiento de los mundos, es la magia de los diccionarios en python.
* Se implementó la instruccion `sal-de-bucle` que rompe un ciclo, equivalente al `break` en otros lenguajes, para usarse en conjunto con las condiciones `verdadero` y `falso`.
* En `kgrammar.py` hay una directiva llamada `futuro` en el constructor, que activa las palabras `verdadero`, `falso` y `sal-de-instruccion`.

Todo el desarrollo del proyecto se llevó a cabo en Debian Wheezy, Ubuntu 12.04 y OpenSUSE usando el IDE Geany Tavira. Otras herramientas incluyen Git como sistema de control de versiones, Git-cola como interfaz para Git, y la magia del escritorio Gnome shell!!

