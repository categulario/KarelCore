PyRel
=====

Karel el robot, escrito completamente en python. Por [@Categulario](https://twitter.com/categulario)

El objetivo de este proyecto es ofrecer la plataforma de aprendizaje de la programación ''Karel'' para todas las plataformas y sin requerir librerías privativas.

Hasta el momento sólo está soportada la sintaxis 'pascal' de Karel.

Testing
-------

Para probar alguno de los componentes hay que ir a la carpeta `/karel` y correr el script elegido

Ejemplo:

`python kgrammar.py`

O también

`python ktokenizer.py`

También es posible pasar un archivo como parámetro, se supondrá que el archivo contiene un programa en karel, en la misma carpeta que los scripts existen archivos con código karel.

* `codigo.karel` contiene un programa correcto sintácticamente
* `malo.karel` tiene algún error de sintaxis
