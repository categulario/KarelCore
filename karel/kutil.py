# -*- coding: iso-8859-1 -*-
"""
Clases y funciones utiles para Karel
"""

class KarelException(Exception):
    """ Define un error sintactico de Karel """
    pass

def xml_prepare(lista):
    """ prepara una lista para ser mostrada por sus parametros en un
    atributo de etiqueta XML"""
    s = ""
    for i in lista:
        s += str(i)+" "
    return s[:-1]

class kcompiled:
    """ Define un programa compilado de Karel """
    def __init__(self):
        self.funciones = dict()
        self.main = [] #La cola principal de funciones