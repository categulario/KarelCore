# -*- coding: iso-8859-1 -*-
"""
Define la gramatica de Karel
"""

from ktokenizer import ktokenizer
from kutil import KarelException
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
            "sal-de-funcion",
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
            "verdadero",
            "falso"
        ]
        self.debug = debug
        self.tokenizador = ktokenizer(flujo, archivo)
        self.token_actual = self.tokenizador.get_token().lower()
        self.estado = True #Almacena el estado del programa, cambia si se encuentra un error
        if self.debug:
            print "debug:", "Primer token:", self.token_actual

    def avanza_token (self):
        """ Avanza un token en el archivo """
        siguiente_token = self.tokenizador.get_token().lower()
        if self.debug:
            print "debug:", "avanza_token()", "'"+siguiente_token+"'"
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
            print "debug:", "bloque()"
        while self.token_actual == 'define-nueva-instruccion' or self.token_actual == 'define-prototipo-instruccion' or self.token_actual == 'externo':
            if self.token_actual == 'define-nueva-instruccion':
                self.declaracion_de_procedimiento()
            elif self.token_actual == 'define-prototipo-instruccion':
                self.declaracion_de_prototipo()
            else:
                #Se trata de una declaracion de enlace
                #TODO averiguar que cosa es esa
                self.declaracion_de_enlace()
        #Sigue el bloque con la lÃ³gica del programa
        if self.token_actual == 'inicia-ejecucion':
            self.avanza_token()
            self.expresion_general()
            if self.token_actual != 'termina-ejecucion':
                raise KarelException("Se esperaba 'termina-ejecucion' al final del bloque lógico del programa, encontré '%s'"%self.token_actual)
            else:
                self.avanza_token()

    def clausula_atomica(self):
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
            print "debug:", "clausula_atomica()"

        if self.token_actual == 'si-es-cero':
            self.avanza_token()
            if self.token_actual == '(':
                self.avanza_token()
                self.expresion_entera()
                if self.token_actual == ')':
                    self.avanza_token()
                else:
                    raise KarelException("Se esperaba ')'")
            else:
                raise KarelException("Se esperaba '('")
        elif self.token_actual == '(':
            self.avanza_token()
            self.termino()
            if self.token_actual == ')':
                avanza_token()
            else:
                raise KarelException("Se esperaba ')'")
        else:
            self.funcion_booleana()

    def clausula_no(self):
        """
        Define una clausula de negacion
        {
            ClausulaNo ::= ["NO"] ClausulaAtomica
        }
        """
        if self.debug:
            print "debug:", "clausula_no()"
        if self.token_actual == 'no':
            self.avanza_token()
            self.clausula_atomica()
        else:
            self.clausula_atomica()

    def clausula_y(self):
        """
        Define una clausula conjuntiva
        {
            ClausulaY ::= ClausulaNo ["Y" ClausulaNo]...
        }
        """
        if self.debug:
            print "debug:", "clausula_y()"
        self.clausula_no()

        while self.token_actual == 'y':
            self.avanza_token()
            self.clausula_no()

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
            print "debug:", "declaracion_de_procedimiento()"
        self.avanza_token()

        requiere_parametros = False #Indica si la funcion a definir tiene parametros

        if self.token_actual in self.palabras_reservadas:
            #No esta permitido usar una palabra reservada
            self.estado = False
            raise KarelException("Se esperaba un nombre de procedimiento vÃ¡lido, '%s' no lo es"%self.token_actual)

        self.avanza_token()

        if self.token_actual == 'como':
            self.avanza_token()
        elif self.token_actual == '(':
            self.avanza_token()
            requiere_parametros = True
            if self.token_actual in self.palabras_reservadas:
                raise KarelException("Se esperaba un nombre de variable")
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
        self.expresion()
        while self.token_actual == ';':
            self.avanza_token()

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
            print "debug:", "declaracion_de_prototipo()"
        requiere_parametros = False
        self.avanza_token()
        if self.token_actual in self.palabras_reservadas:
            raise KarelException("Se esperaba un nombre de función, '%s' no es válido"%self.token_actual)
        self.avanza_token()
        if self.token_actual == ';':
            self.avanza_token();
        elif self.token_actual == '(':
            requiere_parametros = True
            self.avanza_token()
            if self.token_actual in self.palabras_reservadas:
                raise KarelException("Se esperaba un nombre de variable, '%s' no es válido"%self.token_actual)
        else:
            raise KarelException("Se esperaba ';' o un parámetro")

        if requiere_parametros:
            self.avanza_token()
            if self.token_actual != ')':
                raise KarelException("Se esperaba ')'")
            self.avanza_token()
            if self.token_actual != ';':
                raise KarelException("Se esperaba ';' o una variable")
            self.avanza_token()

    def declaracion_de_enlace (self):
        """ Se utilizarÃ¡ para tomar funciones de librerÃ­as externas,
        aun no implementado"""
        if self.debug:
            print "debug:", "declaracion_de_enlace()"

    def expresion(self):
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
        """
        if self.debug:
            print "debug:", "expresion()"

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
            self.expresion_si()
        elif self.token_actual == 'mientras':
            self.expresion_mientras()
        elif self.token_actual == 'repite' or self.token_actual == 'repetir':
            self.expresion_repite()
        elif self.token_actual == 'inicio':
            self.avanza_token()
            self.expresion_general()
            if self.token_actual == 'fin':
                self.avanza_token()
            else:
                raise KarelException("Se esperaba 'fin' para concluir el bloque, encontré '%s'"%self.token_actual)
        elif self.token_actual not in self.palabras_reservadas:
            self.avanza_token()
        else:
            raise KarelException("Se esperaba un procedimiento, %s no es válido"%self.token_actual)

    def expresion_entera(self):
        """
        Define una expresion numerica entera
        {
            ExpresionEntera ::= { Decimal | Identificador | "PRECEDE" "(" ExpresionEntera ")" | "SUCEDE" "(" ExpresionEntera ")" }{
        }
        """
        if self.debug:
            print "debug:", "expresion_entera()"
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
                    self.expresion_entera()
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
                    self.expresion_entera()
                    if self.token_actual == ')':
                        self.avanza_token()
                    else:
                        raise KarelException("Se esperaba ')'")
                else:
                    raise KarelException("Se esperaba '('")
            elif self.token_actual not in self.palabras_reservadas:
                #Se trata de una variable definida por el usuario
                #TODO añadir verificacion de variables
                self.avanza_token()
            else:
                raise KarelException("Se esperaba un entero, variable, sucede o predece, %s no es válido"%self.token_actual)
        else:
            #Si se pudo convertir, avanzamos
            self.avanza_token()

    def expresion_general(self):
        """
        Define una expresion general
        { Expresion | ExpresionVacia }
        Generalmente se trata de una expresión dentro de las etiquetas
        'inicio' y 'fin'
        """
        if self.debug:
            print "debug:", "expresion_general()"
        while self.token_actual != 'fin' and self.token_actual != 'termina-ejecucion':
            self.expresion()
            if self.token_actual != ';' and self.token_actual != 'fin' and self.token_actual != 'termina-ejecucion':
                raise KarelException("Se esperaba ';'")
            elif self.token_actual == ';':
                self.avanza_token()

    def expresion_mientras(self):
        """
        Define la expresion del bucle MIENTRAS
        {
        ExpresionMientras ::= "Mientras" Termino "hacer"
                                  Expresion
        }
        """
        if self.debug:
            print "debug:", "expresion_mientras()"
        self.avanza_token()

        self.termino()

        if self.token_actual != 'hacer':
            raise KarelException("Se esperaba 'hacer'")
        self.avanza_token()
        self.expresion()

    def expresion_repite(self):
        """
        Define la expresion del bucle REPITE
        {
        ExpresionRepite::= "repetir" ExpresionEntera "veces"
                              Expresion
        }
        """
        if self.debug:
            print "debug:", "expresion_repite()"

        self.avanza_token()
        self.expresion_entera()

        if self.token_actual != 'veces':
            raise KarelException("Se esperaba la palabra 'veces'")

        self.avanza_token()
        self.expresion()

    def expresion_si(self):
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
            print "debug:", "expresion_si()"

        self.avanza_token()
        self.termino()

        if self.token_actual != 'entonces':
            raise KarelException("Se esperaba 'entonces'")

        self.avanza_token()

        self.expresion()

        if self.token_actual == 'sino':
            self.avanza_token()
            self.expresion()

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
            print "debug:", "funcion_booleana()"

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

    def termino(self):
        """
        Define un termino
        {
            Termino ::= ClausulaY [ "o" ClausulaY] ...
        }
        Se usan dentro de los condicionales 'si' y el bucle 'mientras'
        """
        if self.debug:
            print "debug:", "termino()"
        self.clausula_y()

        while self.token_actual == 'o':
            self.avanza_token()
            self.clausula_y()

    def verificar (self):
        """ Verifica que este correcta la gramatica de un programa
        en karel """
        if self.debug:
            print "debug:", "verificando la gramática"

        if self.token_actual == 'iniciar-programa':
            if self.avanza_token():
                self.bloque()
                if self.token_actual != 'finalizar-programa':
                    raise KarelException("Se esperaba 'finalizar-programa' al final del codigo")
                    self.estado = False
            else:
                self.estado = False
                raise KarelException("Codigo mal formado")
        else:
            raise KarelException("Se esperaba 'iniciar-programa' al inicio del programa")
            self.estado = False


if __name__ == "__main__":
    if len(sys.argv) == 1:
        grammar = kgrammar(debug=True)
    else:
        fil = sys.argv[1]
        grammar = kgrammar(flujo=open(fil), archivo=fil, debug=True)
    try:
        grammar.verificar()
        print
    except KarelException, ke:
        print ke.args[0], "cerca de la línea", grammar.tokenizador.lineno
        print
        print "El programa tiene errores de sintaxis"
    else:
        print
        print "La sintaxis está correcta"
    finally:
        print ">Sintaxis Verificada"
