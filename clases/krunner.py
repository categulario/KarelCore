#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
#  krunner.py
#
#  Copyright 2012 Developingo <a.wonderful.code@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""
Clase capaz de ejecutar archivos de Karel, tomando el resultado de un
análizis sintáctico, y un mundo.
"""

from kworld import kworld
from kgrammar import kgrammar
from kutil import KarelException
from ktokenizer import ktokenizer
import sys

class krunner:
    """ Ejecuta codigos compilados de Karel hasta el final o hasta
    encontrar un error relacionado con las condiciones del mundo. """

    def __init__ (self):
        """ Inicializa el ejecutor dados un codigo fuente y un mundo. """
        pass

    def expresion_entera (self):
        """ Obtiene el resultado de una evaluacion entera y lo devuelve
        """
        pass

    def expresion_si (self):
        """ Ejecuta una estructura condicional """
        pass

    def expresion_mientras (self):
        """ Ejecuta un bucle 'mientras' """
        pass

    def expresion_repite (self):
        """ Ejecuta un bucle 'repite' """
        pass

    def bloque (self):
        """ Ejecuta una cola de instrucciones dentro de una estructura
        mayor """
        pass

    def termino_logico (self):
        """ Obtiene el resultado de la evaluacion de un termino logico 'o'
        para el punto en que se encuentre Karel al momento de la llamada
        """
        pass

    def clausula_y (self):
        """ Obtiene el resultado de una comparación 'y' entre terminos
        logicos """
        pass

    def clausula_no (self):
        """ Obtiene el resultado de una negacion 'no' o de un termino
        logico """
        pass

    def clausula_atomica (self):
        """ Obtiene el valor logico de una expresion, o de un conjunto
        agrupado de ellas mediante parentesis """
        pass

    def run (self):
        """ Ejecuta el codigo compilado de Karel en el mundo
        proporcionado, comenzando por el bloque 'main' o estructura
        principal. """
        pass

if __name__ == '__main__':
    print "TODO terminar el krunner"

