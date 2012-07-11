PyRel
=====

Karel el robot, escrito completamente en python. Por [@Categulario](https://twitter.com/categulario)

El objetivo de este proyecto es ofrecer la plataforma de aprendizaje de la programación ''Karel'' para todas las plataformas y sin requerir librerías privativas.

Hasta el momento sólo está soportada la sintaxis 'pascal' de Karel.

Testing
-------

Para probar alguno de los componentes hay que ir a la carpeta `/karel` y correr el script elegido

Ejemplo:

`$ python kgrammar.py`

O también

`$ python ktokenizer.py`

También es posible pasar un archivo como parámetro, se supondrá que el archivo contiene un programa en karel, en la misma carpeta que los scripts existen archivos con código karel.

* `codigo.karel` contiene un programa correcto sintácticamente
* `malo.karel` tiene algún error de sintaxis

Un ejemplo de cómo pasar un archivo como parámetro:

`$ python kgrammar.py codigo.karel`

TODO
----

Algunas buenas ideas por implementar en este proyecto

* Implementar la GUI del IDE
* Poner una sección con un tutorial de Karel a modo de 'misiones'
* El analizador sintáctico no verifica puntos y comas
* Implementar comentarios de varias lineas con `/`

Notas
-----

* Añadí (para evitar conflictos y confusiones frecuentes) soporte para 'repetir' y 'repite' como bucles, ambos con la misma funcionalidad. Cualquier comentario me avisan.
* Trato de hacer los mensajes de error lo más comprensibles posible.
* Se pueden hacer comentarios en una línea usando `#` y `/`, no hay soporte aun para comentarios de varias líneas, pero planeo que se abran y cierren con `/`
