#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  kworld.py
#
#  Copyright 2012 Abraham Toriz Cruz <a.wonderful.code@gmail.com>
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

import json

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
        self.mundo = dict()
        if archivo is not None and isinstance(archivo, basestring):
            self.carga_archivo(archivo)
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
        """ Agrega una pared al mundo, si es que está permitido, el
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
                self.mundo['casillas'][self.obten_casilla_avance(coordenadas, posicion)]['paredes'].add(self.contrario(posicion))
            except KeyError:
                self.mundo['casillas'].update({
                    self.obten_casilla_avance(coordenadas, posicion): {
                        'zumbadores': 0,
                        'paredes': set([self.contrario(posicion)])
                    }
                })

    def agrega_zumbadores (self, posicion, cantidad):
        """ Agrega zumbadores al mundo en la posicion dada """
        if 0<posicion[0]<self.mundo['dimensiones']['filas']+1 and 0<posicion[1]<self.mundo['dimensiones']['columnas']+1:
            try:
                self.mundo['casillas'][posicion]['zumbadores'] = cantidad
            except KeyError:
                self.mundo['casillas'].update({
                    posicion: {
                        'zumbadores': cantidad,
                        'paredes': set()
                    }
                })

    def avanza (self, test=False):
        """ Determina si puede karel avanzar desde la posición en la que
        se encuentra, de ser posible avanza. Si el parámetro test es
        verdadero solo ensaya. """
        #Determino primero si está en los bordes
        if self.frente_libre():
            self.mundo['karel']['posicion'] = self.obten_casilla_avance(self.mundo['karel']['posicion'], self.mundo['karel']['orientacion'])
            return True
        else:
            return False

    def gira_izquierda (self, test=False):
        """ Gira a Karel 90° a la izquierda, obteniendo una nueva
        orientación. Si el parámetro test es verdadero solo ensaya"""
        if not test:
            self.mundo['karel']['orientacion'] = self.rotado(self.mundo['karel']['orientacion'])

    def coge_zumbador (self, test=False):
        """ Determina si Karel puede coger un zumbador, si es posible lo
        toma, devuelve Falso si no lo logra. Si el parámetro test es
        verdadero solo ensaya. """
        posicion = self.mundo['karel']['posicion']
        if self.junto_a_zumbador():
            if self.mundo['casillas'][posicion]['zumbadores'] == 'inf':
                if not test:
                    if self.mundo['karel']['mochila'] != 'inf':
                        self.mundo['karel']['mochila'] += 1
            elif self.mundo['casillas'][posicion]['zumbadores']>0:
                if not test:
                    if self.mundo['karel']['mochila'] != 'inf':
                        self.mundo['karel']['mochila'] += 1
                    self.mundo['casillas'][posicion]['zumbadores'] -= 1
            return True
        else:
            return False

    def deja_zumbador (self, test=False):
        """ Determina si Karel puede dejar un zumbador en la casilla
        actual, si es posible lo deja. Si el parámetro test es verdadero
        solo ensaya  """
        posicion = self.mundo['karel']['posicion']
        if self.algun_zumbador_en_la_mochila():
            if not test:
                try:
                    if self.mundo['casillas'][posicion]['zumbadores'] != 'inf':
                        self.mundo['casillas'][posicion]['zumbadores'] += 1
                        if self.mundo['karel']['mochila'] != 'inf':
                            self.mundo['karel']['mochila'] -= 1
                except KeyError:
                    self.mundo['casillas'].update({
                        posicion: {
                            'zumbadores': 1,
                            'paredes': set()
                        }
                    })
                    if self.mundo['karel']['mochila'] != 'inf':
                        self.mundo['karel']['mochila'] -= 1
            return True
        else:
            return False

    def frente_libre(self):
        """ Determina si Karel tiene el frente libre """
        direccion = self.mundo['karel']['orientacion']
        posicion = self.mundo['karel']['posicion']
        if direccion == 'norte':
            if posicion[0] == self.mundo['dimensiones']['filas']:
                return False
        elif direccion == 'sur':
            if posicion[0] == 1:
                return False
        elif direccion == 'este':
            if posicion[1] == self.mundo['dimensiones']['columnas']:
                return False
        elif direccion == 'oeste':
            if posicion[1] == 1:
                return False
        if not self.mundo['casillas'].has_key(posicion):
            return True #No hay un registro para esta casilla, no hay paredes
        else:
            if direccion in self.mundo['casillas'][posicion]['paredes']:
                return False
            else:
                return True

    def izquierda_libre (self):
        """ Determina si Karel tiene la izquierda libre """
        direccion = self.mundo['karel']['orientacion']
        posicion = self.mundo['karel']['posicion']
        if direccion == 'norte':
            if posicion[1] == 1:
                return False
        elif direccion == 'sur':
            if posicion[1] == self.mundo['dimensiones']['columnas']:
                return False
        elif direccion == 'este':
            if posicion[0] == self.mundo['dimensiones']['filas']:
                return False
        elif direccion == 'oeste':
            if posicion[0] == 1:
                return False
        if not self.mundo['casillas'].has_key(posicion):
            return True #No hay un registro para esta casilla, no hay paredes
        else:
            if self.rotado(direccion) in self.mundo['casillas'][posicion]['paredes']:
                return False
            else:
                return True

    def derecha_libre (self):
        """ Determina si Karel tiene la derecha libre """
        direccion = self.mundo['karel']['orientacion']
        posicion = self.mundo['karel']['posicion']
        if direccion == 'norte':
            if posicion[1] == self.mundo['dimensiones']['columnas']:
                return False
        elif direccion == 'sur':
            if posicion[1] == 1:
                return False
        elif direccion == 'este':
            if posicion[0] == 1:
                return False
        elif direccion == 'oeste':
            if posicion[0] == self.mundo['dimensiones']['filas']:
                return False
        if not self.mundo['casillas'].has_key(posicion):
            return True #No hay un registro para esta casilla, no hay paredes extra
        else:
            if self.rotado(self.rotado(self.rotado(direccion))) in self.mundo['casillas'][posicion]['paredes']:
                return False
            else:
                return True

    def junto_a_zumbador (self):
        """ Determina si Karel esta junto a un zumbador. """
        if self.mundo['casillas'].has_key(self.mundo['karel']['posicion']):
            if self.mundo['casillas'][self.mundo['karel']['posicion']]['zumbadores'] == 'inf':
                return True
            elif self.mundo['casillas'][self.mundo['karel']['posicion']]['zumbadores'] > 0:
                return True
            else:
                return False
        else:
            return False

    def orientado_al(self, direccion):
        """ Determina si karel esta orientado al norte """
        if self.mundo['karel']['orientacion'] == direccion:
            return True
        else:
            return False

    def algun_zumbador_en_la_mochila(self):
        """ Determina si karel tiene algun zumbador en la mochila """
        if self.mundo['karel']['mochila'] > 0:
            return True
        else:
            return False

    def obten_casilla_avance (self, casilla, direccion):
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

    def rotado (self, cardinal):
        """ Obtiene la orientación resultado de un gira-izquierda en
        Karel """
        puntos = {
            'norte': 'oeste',
            'oeste': 'sur',
            'sur': 'este',
            'este': 'norte'
        }
        return puntos[cardinal]

    def exporta_mundo (self, nombrearchivo, expandir=False):
        """ Exporta las condiciones actuales del mundo usando algun
        lenguaje de marcado """
        mundo = {
            'karel': {
                'posicion': self.mundo['karel']['posicion'],
                'orientacion': self.mundo['karel']['orientacion'],
                'mochila': self.mundo['karel']['mochila']
            },
            'dimensiones': {
                'filas': self.mundo['dimensiones']['filas'],
                'columnas': self.mundo['dimensiones']['columnas']
            },
            'casillas': []
        }
        for llave, valor in self.mundo['casillas'].iteritems():
            mundo['casillas'].append({
                'casilla': {
                    'fila': llave[0],
                    'columna': llave[1],
                    'zumbadores': valor['zumbadores'],
                    'paredes': list(valor['paredes'])
                }
            })
        f = file(nombrearchivo, 'w')
        if expandir:
            f.write(json.dumps(mundo, indent=2))
        else:
            f.write(json.dumps(mundo))
        f.close()

    def carga_archivo (self, nombrearchivo):
        """ Carga el contenido de un archivo con la configuración del
        mundo """
        f = file(nombrearchivo, 'r')
        mundo = json.load(f)
        #Lo cargamos al interior
        self.mundo_backup = self.mundo
        try:
            self.mundo = {
                'karel': {
                    'posicion': mundo['karel']['posicion'],
                    'orientacion': mundo['karel']['orientacion'],
                    'mochila': mundo['karel']['mochila'] #Zumbadores en la mochila
                },
                'dimensiones': {
                    'filas': mundo['dimensiones']['filas'],
                    'columnas': mundo['dimensiones']['columnas']
                },
                'casillas': dict()
            }
            for casilla in mundo['casillas']:
                self.mundo['casillas'].update({
                    (casilla['fila'], casilla['columna']): {
                        'zumbadores': casilla['zumbadores'],
                        'paredes': set(casilla['paredes'])
                    }
                })
        except KeyError:
            self.mundo = self.mundo_backup
            del(self.mundo_backup)
            return False
        else:
            del(self.mundo_backup)
            return True

    def limpiar (self):
        """ Limpia el mundo y lo lleva a un estado inicial """
        self.mundo = {
            'karel': {
                'posicion': mundo['karel']['posicion'],
                'orientacion': mundo['karel']['orientacion'],
                'mochila': mundo['karel']['mochila'] #Zumbadores en la mochila
            },
            'dimensiones': {
                'filas': mundo['dimensiones']['filas'],
                'columnas': mundo['dimensiones']['columnas']
            },
            'casillas': dict()
        }




if __name__ == '__main__':
    #Pruebas
    from pprint import pprint
    casillas_prueba = {
        (1, 1) : {
            'zumbadores': 'inf',
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
    mundo = kworld()
    mundo.exporta_mundo('cosa.json', True)
    mundo.agrega_pared((8, 8), 'norte')
    mundo.agrega_pared((5, 5), 'oeste')
    #mundo.agrega_pared((1, 1), 'norte')
    #mundo.avance_valido()
    mundo.avanza()
    mundo.avanza()
    mundo.avanza()
    mundo.avanza()
    #print mundo.coge_zumbador()
    mundo.deja_zumbador()
    mundo.gira_izquierda()
    mundo.agrega_zumbadores((5, 5), 50)

    #pprint(mundo.mundo)
    mundo.exporta_mundo('mundo.json', True)
    mundo.carga_archivo('cosa.json')
    pprint(mundo.mundo)

