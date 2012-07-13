#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_all.py
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

from os import listdir
from kgrammar import kgrammar
from kutil import KarelException

if __name__ == '__main__':
    archivos = listdir("./")
    for arch in archivos:
        if arch.endswith(".txt") or arch.endswith(".karel"):
            grammar = kgrammar(flujo=open(arch), archivo=arch, debug=False)
            try:
                grammar.verificar_sintaxis()
            except KarelException, ke:
                print "El archivo %s tiene errores:"%arch
                print "\t", ke[0], "en la línea", grammar.tokenizador.lineno
                break
    else:
        print "Todo está bien"

