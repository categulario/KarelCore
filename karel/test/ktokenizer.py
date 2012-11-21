#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sin título.py
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

"""
Tokenizador para la sintaxis pascal de Karel el robot
"""

class ktokenizer(object):
    """Define el analizador léxico de python"""
    def __init__(self, archivo, debug = False):
        self.nombre_archivo = archivo
        self.archivo = open(archivo)
        self.pila_tokens = [] #Pila de tokens
        #Componentes requeridos
        self.eof = ''
        self.wordchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
        self.whitespace = ' \t\r\n'
        self.states = {
            "word" : 'a',
            "space": ' ',
            "eof"  : ''
        }
        self.state = self.states['space']
        self.lineno = 1
        self.has_lineno_change = False
        self.debug = debug
        if self.debug:
            print "Leyendo '%s'"%archivo

    def get_token(self):
        """Obtiene el siguiente token. Si la pila tiene tokens le quita
        uno, si no, obtiene el siguiente token del archivo"""
        if len(self.pila_tokens)>0:
            return self.pila_tokens.pop()
        else:
            return self.read_token()

    def read_token(self):
        """Lee el siguiente token del archivo.

        El procedimiento es el siguiente: se comen todos los espacios y
        comentarios hasta llegar al siguiente caracter, que será leido hasta el final"""
        token = ''
        while True:
            if self.has_lineno_change:
                self.lineno +=1
                self.has_lineno_change = False

            nextchar = self.archivo.read(1)

            if nextchar == '\n':
                self.has_lineno_change = True
            if nextchar in self.whitespace:
                self.state = self.states['space']
                continue
            elif nextchar in self.wordchars:
                pass

    def push_token(self, token):
        """Empuja un token en la pila"""
        self.pila_tokens.append(token)

    def __iter__(self):
        return self

    def next(self):
        """Devuelve un token de la pila si no está vacía o devuelve el
        siguiente token del archivo, esta función sirve al iterador de
        tokens"""
        token = self.get_token()
        if token == self.eof:
            raise StopIteration
        return token


if __name__ == '__main__':
    k = ktokenizer('prueba.karel', debug=True)


