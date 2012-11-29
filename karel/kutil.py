# -*- coding: utf-8 -*-
"""
Clases y funciones utiles para Karel
"""

__all__ = ['KarelException', 'xml_prepare']

class ktoken(object): #TODO determinar usabilidad
    """Define un token de la gramática de karel. Esencialmente un token
    es un trozo de cadena, sin embargo para esta gramática podría ser un"""
    #TODO probablemente necesite una función hash
    POSICION_INICIO = 'ini'
    POSICION_FIN = 'fin'
    POSICION_MEDIO = 'med'
    def __init__(self, s_token, linea, columna, posicion):
        """Inicializa el token con un token cadena"""
        self.token = s_token.lower()
        self.linea = linea
        self.columna = columna
        self.posicion = posicion

    def __str__(self):
        return self.token

    def __repr__(self):
        return repr(self.token)

    def __int__(self):
        return int(self.token)

    def __eq__(self, cad):
        return self.token == cad

    def __ne__(self, cad):
        return self.token != cad

    def __iter__(self):
        return (i for i in self.token)

    def __hash__(self):
        return hash(self.token)

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

if __name__ == '__main__':
    print ktoken('(') == '('
