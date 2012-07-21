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

sys.setrecursionlimit(10000) #Ampliamos el limite de recursion del sistema

class krunner:
    """ Ejecuta codigos compilados de Karel hasta el final o hasta
    encontrar un error relacionado con las condiciones del mundo. """

    def __init__ (self, programa_compilado, mundo=None, limite_recursion=6500):
        """ Inicializa el ejecutor dados un codigo fuente compilado y un
        mundo, tambien establece el limite para la recursion sobre una
        funcion antes de botar un error stack_overflow."""
        self.arbol = programa_compilado
        if mundo:
            self.mundo = mundo
        else:
            self.mundo = kworld() #En la 1,1 orientado al norte
        self.corriendo = True
        self.sal_de_instruccion = False
        self.limite_recursion = limite_recursion
        self.profundidad = 0 #El punto inicial en la recursion

    def bloque (self, cola, diccionario_variables):
        """ Ejecuta una cola de instrucciones dentro de una estructura
        mayor """
        for instruccion in cola:
            if type(instruccion) == dict:
                #Se trata de una estructura de control o una funcion definida
                if instruccion['estructura'] == 'si':
                    if self.termino_logico(instruccion['argumento']['o'], diccionario_variables):
                        self.bloque(instruccion['cola'], diccionario_variables)
                    elif instruccion.has_key('sino-cola'):
                        self.bloque(instruccion['sino-cola'], diccionario_variables)
                elif instruccion['estructura'] == 'repite':
                    for i in xrange(self.expresion_entera(instruccion['argumento'], diccionario_variables)):
                        self.bloque(instruccion['cola'], diccionario_variables)
                        if not self.corriendo or self.sal_de_instruccion:
                            return
                elif instruccion['estructura'] == 'mientras':
                    while self.termino_logico(instruccion['argumento']['o'], diccionario_variables):
                        self.bloque(instruccion['cola'], diccionario_variables)
                        if not self.corriendo or self.sal_de_instruccion:
                            return
                else:
                    #print 'INSTRUCCION: ', instruccion['nombre'] #TODO programar la llamada a funciones
                    if self.profundidad == self.limite_recursion:
                        raise KarelException(u"StackOverflow! Se ha alcanzado el límite de una recursion")
                    self.profundidad += 1
                    self.bloque(self.arbol['funciones'][instruccion['nombre']]['cola'], self.merge(self.arbol['funciones'][instruccion['nombre']]['params'], instruccion['argumento']))
                    self.profundidad -= 1
                    if self.sal_de_instruccion:
                        self.sal_de_instruccion = False
            else:
                #Es una instruccion predefinida de Karel
                if instruccion == 'avanza':
                    if not self.mundo.avanza():
                        raise KarelException('Karel se ha estrellado con una pared!')
                elif instruccion == 'gira-izquierda':
                    self.mundo.gira_izquierda()
                elif instruccion == 'coge-zumbador':
                    if not self.mundo.coge_zumbador():
                        raise KarelException('Karel quizo coger un zumbador pero no habia en su posicion')
                elif instruccion == 'deja-zumbador':
                    if not self.mundo.deja_zumbador():
                        raise KarelException('Karel quizo dejar un zumbador pero su mochila estaba vacia')
                elif instruccion == 'apagate':
                    self.corriendo = False
                    return
                elif instruccion == 'sal-de-instruccion':
                    self.sal_de_instruccion = True
                    return

    def expresion_entera (self, valor, diccionario_variables):
        """ Obtiene el resultado de una evaluacion entera y lo devuelve
        """
        if type(valor) == dict:
            #Se trata de un sucede o un precede
            if valor.has_key('sucede'):
                return self.expresion_entera(valor['sucede'])+1
            else:
                return self.expresion_entera(valor['precede'])-1
        elif type(valor) == int:
            return valor
        else:
            #Es una variable
            return diccionario_variables[valor]

    def termino_logico (self, lista_expresiones, diccionario_variables):
        """ Obtiene el resultado de la evaluacion de un termino logico 'o'
        para el punto en que se encuentre Karel al momento de la llamada,
        recibe una lista con los terminos a evaluar
        """
        for termino in lista_expresiones:
            if self.clausula_y(termino['y'], diccionario_variables):
                return True
        else:
            return False

    def clausula_y (self, lista_expresiones, diccionario_variables):
        """ Obtiene el resultado de una comparación 'y' entre terminos
        logicos """
        for termino in lista_expresiones:
            if not self.clausula_no(termino, diccionario_variables):
                return False #El resultado de una evaluacion 'y' es falso si uno de los terminos es falso
        else:
            return True

    def clausula_no (self, termino, diccionario_variables):
        """ Obtiene el resultado de una negacion 'no' o de un termino
        logico """
        if type(termino) == dict:
            #Se trata de una negacion, un 'o' o un 'si-es-cero'
            if termino.has_key('no'):
                return not self.clausula_no(termino['no'], diccionario_variables)
            elif termino.has_key('o'):
                return self.termino_logico(termino['o'], diccionario_variables)
            else:
                #Si es cero
                if self.expresion_entera(termino['si-es-cero']) == 0:
                    return True
                else:
                    return False
        else:
            #Puede ser una condicion relacionada con el mundo, o verdadero y falso
            if termino == 'verdadero':
                return True
            elif termino == 'falso':
                return False
            elif termino == 'frente-libre':
                return self.mundo.frente_libre()
            elif termino == 'frente-bloqueado':
                return not self.mundo.frente_libre()
            elif termino == 'izquierda-libre':
                return self.mundo.izquierda_libre()
            elif termino == 'izquierda-bloqueada':
                return not self.mundo.izquierda_libre()
            elif termino == 'derecha-libre':
                return self.mundo.derecha_libre()
            elif termino == 'derecha-bloqueada':
                return not self.mundo.derecha_libre()
            elif termino == 'junto-a-zumbador':
                return self.mundo.junto_a_zumbador()
            elif termino == 'no-junto-a-zumbador':
                return not self.mundo.junto_a_zumbador()
            elif termino == 'algun-zumbador-en-la-mochila':
                return self.mundo.algun_zumbador_en_la_mochila()
            elif termino == 'ningun-zumbador-en-la-mochila':
                return not self.mundo.algun_zumbador_en_la_mochila()
            else:
                #Es una preguna de orientacion
                if termino.startswith('no-'):
                    return not self.mundo.orientado_al(termino[16:]) #Que truco
                else:
                    return self.mundo.orientado_al(termino[16:]) #Oh si!

    def run (self):
        """ Ejecuta el codigo compilado de Karel en el mundo
        proporcionado, comenzando por el bloque 'main' o estructura
        principal. """
        self.bloque(self.arbol['main'], dict()) #Enviamos un diccionario vacio de variables para iniciar

    def merge (self, lista_llaves, lista_valores):
        """ Combina un par de listas de la misma longitud en un
        diccionario """
        d = dict()
        l_valores = lista_valores[:]
        #Hacemos una copia de la lista, por que no queremos modificar
        #la lista original, creeme, no lo queremos...
        l_valores.reverse()
        for i in lista_llaves:
            d.update({i: l_valores.pop()})
        return d


if __name__ == '__main__':
    from pprint import pprint
    from time import time
    inicio = 0
    fin = 0
    c_inicio = 0
    c_fin = 0
    if len(sys.argv) == 1:
        grammar = kgrammar(debug=deb, gen_arbol = True)
    else:
        fil = sys.argv[1]
        grammar = kgrammar(flujo=open(fil), archivo=fil, gen_arbol=True)
    try:
        c_inicio = time()
        grammar.verificar_sintaxis()
        c_fin = time()
        #grammar.guardar_compilado('codigo.kcmp', True)
        #pprint(grammar.arbol)
    except KarelException, ke:
        print ke.args[0], "en la línea", grammar.tokenizador.lineno
    else:
        mundo = kworld(mochila='inf')
        runner = krunner(grammar.arbol, mundo)
        try:
            inicio = time()
            runner.run()
            fin = time()
        except KarelException, kre:
            print 'Error:', kre.args[0]
        else:
            print 'Ejecucion terminada OK'
        #pprint(runner.mundo.mundo)
    print "tiempo: ", int((c_fin-c_inicio)*1000), "milisegundos en compilar"
    print "tiempo: ", int((fin-inicio)*1000), "milisegundos en ejecutar"
    print "total:", int((c_fin-c_inicio)*1000) + int((fin-inicio)*1000), "milisegundos"

