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

class kworld:
    """ Representa el mundo de Karel """

    def __init__ (self, filas=100, columnas=100, karel_pos=(1,1), orientacion='norte', archivo=None):
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
                'karel': karel_pos,
                'casillas': {
                    (1, 1) : {
                        'zumbadores': 0,
                        'paredes': ['derecha']
                    },
                    (1, 2): {
                        'zumbadores': 0,
                        'paredes': ['izquierda']
                    },
                    (5, 5): {
                        'zumbadores': 'inf',
                        'paredes': []
                    }
                }
            }


if __name__ == '__main__':
    mundo = kworld()

