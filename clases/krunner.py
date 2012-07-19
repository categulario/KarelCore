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

    def __init__ (self, programa_compilado, mundo=None):
        """ Inicializa el ejecutor dados un codigo fuente compilado y un
        mundo. """
        self.arbol = programa_compilado
        if mundo:
            self.mundo = mundo
        else:
            self.mundo = kworld() #En la 1,1 orientado al norte

    def bloque (self, cola):
        """ Ejecuta una cola de instrucciones dentro de una estructura
        mayor """
        for instruccion in cola:
            if type(instruccion) == dict:
                #Se trata de una estructura de control o una funcion definida
                if instruccion['estructura'] == 'si':
                    print "SI"
                elif instruccion['estructura'] == 'repite':
                    print "REPITE"
                elif instruccion['estructura'] == 'mientras':
                    print 'MIENTRAS'
                else:
                    print 'INSTRUCCION: ', instruccion['nombre']
            else:
                #Es una instruccion predefinida de Karel
                if instruccion == 'avanza':
                    if not self.mundo.avanza():
                        raise KarelException('Karel se topo con una pared')
                elif instruccion == 'gira-izquierda':
                    self.mundo.gira_izquierda()
                elif instruccion == 'coge-zumbador':
                    if not self.mundo.coge_zumbador():
                        raise KarelException('Karel quizo coger un zumbador pero no habia en su posicion')
                elif instruccion == 'deja-zumbador':
                    if not self.mundo.deja_zumbador():
                        raise KarelException('Karel quizo dejar un zumbador pero su mochila estaba vacia')
                elif instruccion == 'apagate':
                    return

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
        self.bloque(self.arbol['main'])

if __name__ == '__main__':
    from pprint import pprint
    from time import time
    inicio = time()
    if len(sys.argv) == 1:
        grammar = kgrammar(debug=deb, gen_arbol = True)
    else:
        fil = sys.argv[1]
        grammar = kgrammar(flujo=open(fil), archivo=fil, gen_arbol=True)
    try:
        grammar.verificar_sintaxis()
        #grammar.guardar_compilado('codigo.kcmp', True)
        #pprint(grammar.arbol)
    except KarelException, ke:
        print ke.args[0], "en la línea", grammar.tokenizador.lineno
    else:
        mundo = kworld(karel_pos=(50, 50), mochila='inf', casillas={
            (50, 50) : {
            'zumbadores': 'inf',
            'paredes': set(['este'])
            },
            (51, 50): {
                'zumbadores': 1,
                'paredes': set(['oeste'])
            }
        })

        runner = krunner(grammar.arbol, mundo)
        try:
            runner.run()
        except KarelException, kre:
            print 'Error:', kre.args[0]
        else:
            print 'Ejecucion terminada'
        pprint(runner.mundo.mundo)
    fin = time()
    print "time: ", fin-inicio

