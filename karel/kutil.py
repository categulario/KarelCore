# -*- coding: iso-8859-1 -*-
"""
Clases y funciones útiles para Karel
"""

class KarelException(Exception):
    """ Define un error sint�ctico de Karel """
    pass

def xml_prepare(lista):
    """ prepara una lista para ser mostrada por sus parametros en un
    atributo de etiqueta XML"""
    s = ""
    for i in lista:
        s += str(i)+" "
    return s[:-1]
