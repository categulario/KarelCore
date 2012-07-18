#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
#  kgrammar.py
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
Define la gramatica de Karel
"""

from ktokenizer import ktokenizer
from kutil import KarelException
from kutil import xml_prepare
import sys

class kgrammar:
    """
    Clase que contiene y conoce la gramatica de karel
    """
    def __init__(self, flujo=None, archivo=None, debug=False):
        self.palabras_reservadas = [
            "iniciar-programa",
            "inicia-ejecucion",
            "termina-ejecucion",
            "finalizar-programa"
            "si-es-cero",
            "no",
            "y",
            "o",
            "define-nueva-instruccion",
            "define-prototipo-instruccion",
            "apagate",
            "gira-izquierda",
            "avanza",
            "coge-zumbador",
            "deja-zumbador",
            "sal-de-instruccion",
            "inicio",
            "fin",
            "precede",
            "sucede",
            "mientras",
            "hacer",
            "repite",
            "repetir",
            "veces",
            "si",
            "entonces",
            "sino",
            "frente-libre"
            "frente-bloqueado",
            "derecha-libre",
            "derecha-bloqueada",
            "izquierad-libre",
            "izquierda-bloqueada",
            "junto-a-zumbador",
            "no-junto-a-zumbador",
            "algun-zumbador-en-la-mochila",
            "ningun-zumbador-en-la-mochila",
            "orientado-al-norte",
            "no-orientado-al-norte",
            "orientado-al-este",
            "no-orientado-al-este",
            "orientado-al-sur",
            "no-orientado-al-sur",
            "orientado-al-oeste",
            "no-orientado-al-oeste",
            "verdadero", #Reservadas para futuros usos
            "falso" #reservadas para futuros usos
        ]
        self.debug = debug
        self.tokenizador = ktokenizer(flujo, archivo)
        self.token_actual = self.tokenizador.get_token().lower()
        self.prototipo_funciones = dict()
        self.funciones = dict()
        # Un diccionario que tiene por llaves los nombres de las funciones
        # y que tiene por valores listas con las variables de dichas
        # funciones
        if self.debug:
            print "<avanza_token new_token='%s' line='%d' />"%(self.token_actual, self.tokenizador.lineno)

    def avanza_token (self):
        """ Avanza un token en el archivo """
        siguiente_token = self.tokenizador.get_token().lower()
        if self.debug:
            print "<avanza_token new_token='%s' line='%d' />"%(siguiente_token, self.tokenizador.lineno)

        if siguiente_token:
            self.token_actual = siguiente_token
            return True
        else:
            return False

    def bloque(self):
        """
        Define un bloque en la sitaxis de karel
        {BLOQUE ::=
                [DeclaracionDeProcedimiento ";" | DeclaracionDeEnlace ";"] ...
                "INICIA-EJECUCION"
                   ExpresionGeneral [";" ExpresionGeneral]...
                "TERMINA-EJECUCION"
        }
        Un bloque se compone de todo el codigo admitido entre iniciar-programa
        y finalizar-programa
        """
        if self.debug:
            print "<bloque>"

        while self.token_actual == 'define-nueva-instruccion' or self.token_actual == 'define-prototipo-instruccion' or self.token_actual == 'externo':
            if self.token_actual == 'define-nueva-instruccion':
                self.declaracion_de_procedimiento()
            elif self.token_actual == 'define-prototipo-instruccion':
                self.declaracion_de_prototipo()
            else:
                #Se trata de una declaracion de enlace
                self.declaracion_de_enlace()
        #Toca verificar que todos los prototipos se hayan definido
        for funcion in self.prototipo_funciones.keys():
            if not self.funciones.has_key(funcion):
                raise KarelException("La instrucción '%s' tiene prototipo pero no fue definida"%funcion)
        #Sigue el bloque con la lógica del programa
        if self.token_actual == 'inicia-ejecucion':
            self.avanza_token()
            self.expresion_general([])
            if self.token_actual != 'termina-ejecucion':
                raise KarelException("Se esperaba 'termina-ejecucion' al final del bloque lógico del programa, encontré '%s'"%self.token_actual)
            else:
                self.avanza_token()

        if self.debug:
            print "</bloque>"

    def clausula_atomica(self, lista_variables):
        """
        Define una clausila atomica
        {
        ClausulaAtomica ::=  {
                              "SI-ES-CERO" "(" ExpresionEntera ")" |
                              FuncionBooleana |
                              "(" Termino ")"
                             }{
        }
        """
        if self.debug:
            print "<clausula_atomica params='%s'>"%xml_prepare(lista_variables)

        if self.token_actual == 'si-es-cero':
            self.avanza_token()
            if self.token_actual == '(':
                self.avanza_token()
                self.expresion_entera(lista_variables)
                if self.token_actual == ')':
                    self.avanza_token()
                else:
                    raise KarelException("Se esperaba ')'")
            else:
                raise KarelException("Se esperaba '('")
        elif self.token_actual == '(':
            self.avanza_token()
            self.termino(lista_variables)
            if self.token_actual == ')':
                self.avanza_token()
            else:
                raise KarelException("Se esperaba ')'")
        else:
            self.funcion_booleana()

        if self.debug:
            print "</clausula_atomica>"

    def clausula_no(self, lista_variables):
        """
        Define una clausula de negacion
        {
            ClausulaNo ::= ["NO"] ClausulaAtomica
        }
        """
        if self.debug:
            print "<clausula_no params='%s'>"%xml_prepare(lista_variables)

        if self.token_actual == 'no':
            self.avanza_token()
            self.clausula_atomica(lista_variables)
        else:
            self.clausula_atomica(lista_variables)

        if self.debug:
            print "</clausula_no>"

    def clausula_y(self, lista_variables):
        """
        Define una clausula conjuntiva
        {
            ClausulaY ::= ClausulaNo ["Y" ClausulaNo]...
        }
        """
        if self.debug:
            print "<clausula_y params='%s'>"%xml_prepare(lista_variables)

        self.clausula_no(lista_variables)

        while self.token_actual == 'y':
            self.avanza_token()
            self.clausula_no(lista_variables)

        if self.debug:
            print "</clausula_y>"

    def declaracion_de_procedimiento(self):
        """
        Define una declaracion de procedimiento
        {
            DeclaracionDeProcedimiento ::= "DEFINE-NUEVA-INSTRUCCION" Identificador ["(" Identificador ")"] "COMO"
                                         Expresion
        }
        Aqui se definen las nuevas funciones que extienden el lenguaje
        de Karel, como por ejemplo gira-derecha
        """
        if self.debug:
            print "<declaracion_de_procedimiento>"

        self.avanza_token()

        requiere_parametros = False #Indica si la funcion a definir tiene parametros
        nombre_funcion = ''

        if self.token_actual in self.palabras_reservadas or not self.es_identificador_valido(self.token_actual):
            raise KarelException("Se esperaba un nombre de procedimiento vÃ¡lido, '%s' no lo es"%self.token_actual)

        if self.funciones.has_key(self.token_actual):
            raise KarelException("Ya se ha definido una funcion con el nombre '%s'"%self.token_actual)
        else:
            self.funciones.update({self.token_actual: []})
            nombre_funcion = self.token_actual

        self.avanza_token()

        if self.token_actual == 'como':
            self.avanza_token()
        elif self.token_actual == '(':
            self.avanza_token()
            requiere_parametros = True
            while True:
                if self.token_actual in self.palabras_reservadas or not self.es_identificador_valido(self.token_actual):
                    raise KarelException("Se esperaba un nombre de variable, '%s' no es válido"%self.token_actual)
                else:
                    if self.token_actual in self.funciones[nombre_funcion]:
                        raise KarelException("La funcion '%s' ya tiene un parámetro con el nombre '%s'"%(nombre_funcion, self.token_actual))
                    else:
                        self.funciones[nombre_funcion].append(self.token_actual)
                        self.avanza_token()

                    if self.token_actual == ')':
                        self.tokenizador.push_token(')') #Devolvemos el token a la pila
                        break
                    elif self.token_actual == ',':
                        self.avanza_token()
                    else:
                        raise KarelException("Se esperaba ',', encontré '%s'"%self.token_actual)
        else:
            raise KarelException("Se esperaba la palabra clave 'como' o un parametro")

        if requiere_parametros:
            self.avanza_token()
            if self.token_actual != ')':
                raise KarelException("Se esperaba ')'")
            self.avanza_token()
            if self.token_actual != 'como':
                raise KarelException("se esperaba la palabra clave 'como'")
            self.avanza_token()

        if self.prototipo_funciones.has_key(nombre_funcion):
            #Hay que verificar que se defina como se planeó
            if len(self.prototipo_funciones[nombre_funcion]) != len(self.funciones[nombre_funcion]):
                raise KarelException("La función '%s' no está definida como se planeó en el prototipo, verifica el número de variables"%nombre_funcion)

        self.expresion(self.funciones[nombre_funcion]) #Le mandamos las variables existentes

        if self.token_actual != ';':
            raise KarelException("Se esperaba ';'")
        else:
            self.avanza_token()

        if self.debug:
            print "</declaracion_de_procedimiento>"

    def declaracion_de_prototipo(self):
        """
        Define una declaracion de prototipo
        {
            DeclaracionDePrototipo ::= "DEFINE-PROTOTIPO-INSTRUCCION" Identificador ["(" Identificador ")"]
        }
        Los prototipos son definiciones de funciones que se hacen previamente
        para poderse utilizar dentro de una función declarada antes.
        """
        if self.debug:
            print "<declaracion_de_prototipo>"

        requiere_parametros = False
        nombre_funcion = ''
        self.avanza_token()

        if self.token_actual in self.palabras_reservadas or not self.es_identificador_valido(self.token_actual):
            raise KarelException("Se esperaba un nombre de función, '%s' no es válido"%self.token_actual)
        if self.prototipo_funciones.has_key(self.token_actual):
            raise KarelException("Ya se ha definido un prototipo de funcion con el nombre '%s'"%self.token_actual)
        else:
            self.prototipo_funciones.update({self.token_actual: []})
            nombre_funcion = self.token_actual

        self.avanza_token()

        if self.token_actual == ';':
            self.avanza_token();
        elif self.token_actual == '(':
            self.avanza_token()
            requiere_parametros = True
            while True:
                if self.token_actual in self.palabras_reservadas or not self.es_identificador_valido(self.token_actual):
                    raise KarelException("Se esperaba un nombre de variable, '%s' no es válido"%self.token_actual)
                else:
                    if self.token_actual in self.prototipo_funciones[nombre_funcion]:
                        raise KarelException("El prototipo de función '%s' ya tiene un parámetro con el nombre '%s'"%(nombre_funcion, self.token_actual))
                    else:
                        self.prototipo_funciones[nombre_funcion].append(self.token_actual)
                        self.avanza_token()

                    if self.token_actual == ')':
                        self.tokenizador.push_token(')') #Devolvemos el token a la pila
                        break
                    elif self.token_actual == ',':
                        self.avanza_token()
                    else:
                        raise KarelException("Se esperaba ',', encontré '%s'"%self.token_actual)
        else:
            raise KarelException("Se esperaba ';' o un parámetro")

        if requiere_parametros:
            self.avanza_token()
            if self.token_actual != ')':
                raise KarelException("Se esperaba ')'")
            self.avanza_token()
            if self.token_actual != ';':
                raise KarelException("Se esperaba ';'")
            self.avanza_token()

        if self.debug:
            print "</declaracion_de_prototipo>"

    def declaracion_de_enlace (self):
        """ Se utilizara para tomar funciones de librerias externas,
        aun no implementado"""
        if self.debug:
            print "<declaracion_de_enlace/>"

    def expresion(self, lista_variables):
        """
        Define una expresion
        {
        Expresion :: = {
                          "apagate"
                          "gira-izquierda"
                          "avanza"
                          "coge-zumbador"
                          "deja-zumbador"
                          "sal-de-funcion"
                          ExpresionLlamada
                          ExpresionSi
                          ExpresionRepite
                          ExpresionMientras
                          "inicio"
                              ExpresionGeneral [";" ExpresionGeneral] ...
                          "fin"
                       }{

        }
        Recibe para comprobar una lista con las variables válidas en
        este contexto
        """
        if self.debug:
            print "<expresion params='%s'>"%xml_prepare(lista_variables)

        if self.token_actual == 'apagate':
            self.avanza_token()
        elif self.token_actual == 'gira-izquierda':
            self.avanza_token()
        elif self.token_actual == 'avanza':
            self.avanza_token()
        elif self.token_actual == 'coge-zumbador':
            self.avanza_token()
        elif self.token_actual == 'deja-zumbador':
            self.avanza_token()
        elif self.token_actual == 'sal-de-instruccion':
            self.avanza_token()
        elif self.token_actual == 'si':
            self.expresion_si(lista_variables)
        elif self.token_actual == 'mientras':
            self.expresion_mientras(lista_variables)
        elif self.token_actual == 'repite' or self.token_actual == 'repetir':
            self.expresion_repite(lista_variables)
        elif self.token_actual == 'inicio':
            self.avanza_token()
            self.expresion_general(lista_variables)
            if self.token_actual == 'fin':
                self.avanza_token()
            else:
                raise KarelException("Se esperaba 'fin' para concluir el bloque, encontré '%s'"%self.token_actual)
        elif self.token_actual not in self.palabras_reservadas and self.es_identificador_valido(self.token_actual):
            #Se trata de una instrucción creada por el usuario
            if self.prototipo_funciones.has_key(self.token_actual) or self.funciones.has_key(self.token_actual):
                nombre_funcion = self.token_actual
                self.avanza_token()
                requiere_parametros = True
                num_parametros = 0
                if self.token_actual == '(':
                    self.avanza_token()
                    while True:
                        self.expresion_entera(lista_variables)
                        num_parametros += 1
                        if self.token_actual == ')':
                            #self.tokenizador.push_token(')') #Devolvemos el token a la pila
                            break
                        elif self.token_actual == ',':
                            self.avanza_token()
                        else:
                            raise KarelException("Se esperaba ',', encontré '%s'"%self.token_actual)

                    if self.prototipo_funciones.has_key(nombre_funcion):
                        if num_parametros != len(self.prototipo_funciones[nombre_funcion]):
                            raise KarelException("Estas intentando llamar la funcion '%s' con %d parámetros, pero así no fue definida"%(nombre_funcion, num_parametros))
                    else:
                        if num_parametros != len(self.funciones[nombre_funcion]):
                            raise KarelException("Estas intentando llamar la funcion '%s' con %d parámetros, pero así no fue definida"%(nombre_funcion, num_parametros))
                    self.avanza_token()
            else:
                raise KarelException("La instrucción '%s' no ha sido previamente definida, pero es utilizada"%self.token_actual)
        else:
            raise KarelException("Se esperaba un procedimiento, '%s' no es válido"%self.token_actual)

        if self.debug:
            print "</expresion>"

    def expresion_entera(self, lista_variables):
        """
        Define una expresion numerica entera
        {
            ExpresionEntera ::= { Decimal | Identificador | "PRECEDE" "(" ExpresionEntera ")" | "SUCEDE" "(" ExpresionEntera ")" }{
        }
        """
        if self.debug:
            print "<expresion_entera params='%s'>"%xml_prepare(lista_variables)
        #En este punto hay que verificar que se trate de un numero entero
        try:
            #Intentamos convertir el numero
            int(self.token_actual, 10)
        except ValueError:
            #No era un entero
            if self.token_actual == 'precede':
                self.avanza_token()
                if self.token_actual == '(':
                    self.avanza_token()
                    self.expresion_entera(lista_variables)
                    if self.token_actual == ')':
                        self.avanza_token()
                    else:
                        raise KarelException("Se esperaba ')'")
                else:
                    raise KarelException("Se esperaba '('")
            elif self.token_actual == 'sucede':
                self.avanza_token()
                if self.token_actual == '(':
                    self.avanza_token()
                    self.expresion_entera(lista_variables)
                    if self.token_actual == ')':
                        self.avanza_token()
                    else:
                        raise KarelException("Se esperaba ')'")
                else:
                    raise KarelException("Se esperaba '('")
            elif self.token_actual not in self.palabras_reservadas and self.es_identificador_valido(self.token_actual):
                #Se trata de una variable definida por el usuario
                if self.token_actual not in lista_variables:
                    raise KarelException("La variable '%s' no está definida en este contexto"%self.token_actual)
                self.avanza_token()
            else:
                raise KarelException("Se esperaba un entero, variable, sucede o predece, '%s' no es válido"%self.token_actual)
        else:
            #Si se pudo convertir, avanzamos
            self.avanza_token()

        if self.debug:
            print "</expresion_entera>"

    def expresion_general(self, lista_variables):
        """
        Define una expresion general
        { Expresion | ExpresionVacia }
        Generalmente se trata de una expresión dentro de las etiquetas
        'inicio' y 'fin' o entre 'inicia-ejecucion' y 'termina-ejecucion'
        """
        if self.debug:
            print "<expresion_general params='%s'>"%xml_prepare(lista_variables)

        while self.token_actual != 'fin' and self.token_actual != 'termina-ejecucion':
            self.expresion(lista_variables)
            if self.token_actual != ';' and self.token_actual != 'fin' and self.token_actual != 'termina-ejecucion':
                raise KarelException("Se esperaba ';'")
            elif self.token_actual == ';':
                self.avanza_token()
            elif self.token_actual == 'fin':
                raise KarelException("Se esperaba ';'")
            elif self.token_actual == 'termina-ejecucion':
                raise KarelException("Se esperaba ';'")

        if self.debug:
            print "</expresion_general>"

    def expresion_mientras(self, lista_variables):
        """
        Define la expresion del bucle MIENTRAS
        {
        ExpresionMientras ::= "Mientras" Termino "hacer"
                                  Expresion
        }
        """
        if self.debug:
            print "<expresion_mientras params='%s'>"%xml_prepare(lista_variables)
        self.avanza_token()

        self.termino(lista_variables)

        if self.token_actual != 'hacer':
            raise KarelException("Se esperaba 'hacer'")
        self.avanza_token()
        self.expresion(lista_variables)

        if self.debug:
            print "</expresion_mientras>"

    def expresion_repite(self, lista_variables):
        """
        Define la expresion del bucle REPITE
        {
        ExpresionRepite::= "repetir" ExpresionEntera "veces"
                              Expresion
        }
        """
        if self.debug:
            print "<expresion_repite params='%s'>"%xml_prepare(lista_variables)

        self.avanza_token()
        self.expresion_entera(lista_variables)

        if self.token_actual != 'veces':
            raise KarelException("Se esperaba la palabra 'veces', '%s' no es válido"%self.token_actual)

        self.avanza_token()
        self.expresion(lista_variables)

        if self.debug:
            print "</expresion_repite>"

    def expresion_si(self, lista_variables):
        """
        Define la expresion del condicional SI
        {
        ExpresionSi ::= "SI" Termino "ENTONCES"
                             Expresion
                        ["SINO"
                               Expresion
                        ]
        }
        """
        if self.debug:
            print "<expresion_si params='%s'>"%xml_prepare(lista_variables)

        self.avanza_token()
        self.termino(lista_variables)

        if self.token_actual != 'entonces':
            raise KarelException("Se esperaba 'entonces'")

        self.avanza_token()

        self.expresion(lista_variables)

        if self.token_actual == 'sino':
            self.avanza_token()
            self.expresion(lista_variables)

        if self.debug:
            print "</expresion_si>"

    def funcion_booleana(self):
        """
        Define una funcion booleana del mundo de karel
        {
        FuncionBooleana ::= {
                               "FRENTE-LIBRE"
                               "FRENTE-BLOQUEADO"
                               "DERECHA-LIBRE"
                               "DERECHA-BLOQUEADA"
                               "IZQUIERAD-LIBRE"
                               "IZQUIERDA-BLOQUEADA"
                               "JUNTO-A-ZUMBADOR"
                               "NO-JUNTO-A-ZUMBADOR"
                               "ALGUN-ZUMBADOR-EN-LA-MOCHILA"
                               "NINGUN-ZUMBADOR-EN-LA-MOCHILA"
                               "ORIENTADO-AL-NORTE"
                               "NO-ORIENTADO-AL-NORTE"
                               "ORIENTADO-AL-ESTE"
                               "NO-ORIENTADO-AL-ESTE"
                               "ORIENTADO-AL-SUR"
                               "NO-ORIENTADO-AL-SUR"
                               "ORIENTADO-AL-OESTE"
                               "NO-ORIENTADO-AL-OESTE"
                               "VERDADERO"
                               "FALSO"
                            }{
        }
        Son las posibles funciones booleanas para Karel
        """
        if self.debug:
            print "<funcion_booleana>"

        if self.token_actual == 'frente-libre':
            self.avanza_token()
        elif self.token_actual == 'frente-bloqueado':
            self.avanza_token()
        elif self.token_actual == 'derecha-libre':
            self.avanza_token()
        elif self.token_actual == 'derecha-bloqueada':
            self.avanza_token()
        elif self.token_actual == 'izquierda-libre':
            self.avanza_token()
        elif self.token_actual == 'izquierda-bloqueada':
            self.avanza_token()
        elif self.token_actual == 'junto-a-zumbador':
            self.avanza_token()
        elif self.token_actual == 'no-junto-a-zumbador':
            self.avanza_token()
        elif self.token_actual == 'algun-zumbador-en-la-mochila':
            self.avanza_token()
        elif self.token_actual == 'ningun-zumbador-en-la-mochila':
            self.avanza_token()
        elif self.token_actual == 'orientado-al-norte':
            self.avanza_token()
        elif self.token_actual == 'no-orientado-al-norte':
            self.avanza_token()
        elif self.token_actual == 'orientado-al-este':
            self.avanza_token()
        elif self.token_actual == 'no-orientado-al-este':
            self.avanza_token()
        elif self.token_actual == 'orientado-al-sur':
            self.avanza_token()
        elif self.token_actual == 'no-orientado-al-sur':
            self.avanza_token()
        elif self.token_actual == 'orientado-al-oeste':
            self.avanza_token()
        elif self.token_actual == 'no-orientado-al-oeste':
            self.avanza_token()
        else:
            raise KarelException("Se esperaba una condición como 'frente-libre', %s no es una condición"%self.token_actual)

        if self.debug:
            print "</funcion_booleana>"

    def termino(self, lista_variables):
        """
        Define un termino
        {
            Termino ::= ClausulaY [ "o" ClausulaY] ...
        }
        Se usan dentro de los condicionales 'si' y el bucle 'mientras'
        """
        if self.debug:
            print "<termino params='%s'>"%xml_prepare(lista_variables)

        self.clausula_y(lista_variables)

        while self.token_actual == 'o':
            self.avanza_token()
            self.clausula_y(lista_variables)

        if self.debug:
            print "</termino>"

    def verificar_sintaxis (self):
        """ Verifica que este correcta la gramatica de un programa
        en karel """
        if self.token_actual == 'iniciar-programa':
            if self.avanza_token():
                self.bloque()
                if self.token_actual != 'finalizar-programa':
                    raise KarelException("Se esperaba 'finalizar-programa' al final del codigo")
            else:
                raise KarelException("Codigo mal formado")
        else:
            raise KarelException("Se esperaba 'iniciar-programa' al inicio del programa")

    def es_identificador_valido(self, token):
        """ Identifica cuando una cadena es un identificador valido,
        osea que puede ser usado en el nombre de una variable, las
        reglas son:
        * Debe comenzar en una letra
        * Sólo puede tener letras, números, '-' y '_' """
        es_valido = True
        i = 0
        for caracter in token:
            if i == 0:
                if caracter not in 'abcdefghijklmnopqrstuvwxyz':
                    #Un identificador válido comienza con una letra
                    es_valido = False
                    break
            else:
                if caracter not in self.tokenizador.wordchars:
                    es_valido = False
                    break
            i += 1
        return es_valido

if __name__ == "__main__":
    deb = True
    if deb:
        print "<xml>" #Mi grandiosa idea del registro XML, Ajua!!
    if len(sys.argv) == 1:
        grammar = kgrammar(debug=deb)
    else:
        fil = sys.argv[1]
        grammar = kgrammar(flujo=open(fil), archivo=fil, debug=deb)
    try:
        grammar.verificar_sintaxis()
    except KarelException, ke:
        print ke.args[0], "en la línea", grammar.tokenizador.lineno
        print
        print "<syntax status='bad'/>"
    else:
        print "<syntax status='good'/>"
    if deb:
        print "</xml>"
