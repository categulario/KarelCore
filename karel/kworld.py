#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mundo.py
#
#  Copyright 2012 Abraham Toriz Cruz <abraham@botero-dev>
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

from pprint import pprint

class kworld:
    """ Representa el mundo de Karel """

    def __init__ (self, filas=100, columnas=100, karel_pos=(1,1), orientacion='norte', mochila=0, casillas=dict(), archivo=None):
        """ Inicializa el mundo, con Karel en la esquina 1,1 del mundo
        orientado al norte.

        El mundo es un diccionario con dos llaves:

        * karel indica mediante una tupla la fila y la columna en la que
        se encuentra el robot
        * casillas indica cómo está construido el mundo mediante un
        diccionario, que tiene por llaves las tuplas con la posicion que
        representan: (fila, columna) """
        #TODO habilitar lectura y escritura desde archivo
        if archivo is not None:
            print "Lectura de archivo no implementada"
        else:
            self.mundo = {
                'karel': {
                    'posicion': karel_pos,
                    'orientacion': orientacion,
                    'mochila': mochila #Zumbadores en la mochila
                },
                'dimensiones': {
                    'filas': filas,
                    'columnas': columnas
                },
                'casillas': casillas
            }

    def agrega_pared (self, coordenadas, posicion):
        """ Agrega una pared al mundo, es que está permitido, el
        atributo 'coordenadas' es una tupla con la fila y columna de la
        casilla afectada, posicion es una cadena que indica si se pone
        arriba, abajo, a la izquierda o a la derecha. """
        if 0<coordenadas[0]<self.mundo['dimensiones']['filas']+1 and 0<coordenadas[1]<self.mundo['dimensiones']['columnas']+1:
            #Los dats de las coordenadas son validos
            try:
                self.mundo['casillas'][coordenadas]['paredes'].add(posicion)
            except KeyError:
                self.mundo['casillas'].update({
                    coordenadas: {
                        'zumbadores': 0,
                        'paredes': set([posicion])
                    }
                })
            try:
                self.mundo['casillas'][self.obten_casilla(coordenadas, posicion)]['paredes'].add(self.contrario(posicion))
            except KeyError:
                self.mundo['casillas'].update({
                    self.obten_casilla(coordenadas, posicion): {
                        'zumbadores': 0,
                        'paredes': set([self.contrario(posicion)])
                    }
                })

    def obten_casilla (self, casilla, direccion):
        """ Obtiene una casilla contigua dada una casilla de inicio y
        una direccion de avance"""
        if direccion == 'norte':
            return (casilla[0]+1, casilla[1])
        elif direccion == 'sur':
            return (casilla[0]-1, casilla[1])
        elif direccion == 'este':
            return (casilla[0], casilla[1]+1)
        elif direccion == 'oeste':
            return (casilla[0], casilla[1]-1)

    def contrario (self, cardinal):
        """ Suena ridículo, pero obtiene el punto cardinal contrario al
        dado. """
        puntos = {
            'norte': 'sur',
            'sur': 'norte',
            'este': 'oeste',
            'oeste': 'este'
        }
        return puntos[cardinal]


if __name__ == '__main__':
    casillas_prueba = {
        (1, 1) : {
            'zumbadores': 0,
            'paredes': set(['este'])
        },
        (1, 2): {
            'zumbadores': 0,
            'paredes': set(['oeste'])
        },
        (5, 5): {
            'zumbadores': 'inf',
            'paredes': set()
        },
        (2, 1): {
            'zumbadores': 2,
            'paredes': set()
        }
    } #Representa la estructura de un mundo consistente
    mundo = kworld(casillas = casillas_prueba)
    mundo.agrega_pared((8,8), 'norte')
    pprint(casillas_prueba)

