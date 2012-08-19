# -*- coding: utf-8 -*-
"""
Clases y funciones utiles para Karel
"""

__all__ = ['KarelException', 'xml_prepare']

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

