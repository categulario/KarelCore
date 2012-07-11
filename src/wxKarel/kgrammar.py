#!coding:iso-8859-1
"""
Define la gramatica de Karel
"""

from ktokenizer import ktokenizer
import sys

class kgrammar:
    """
    Clase que contiene y conoce la gramatica de karel
    """
    def __init__(self, flujo=None, archivo=None):
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
        self.tokenizador = ktokenizer(flujo, archivo)
        self.token_actual = self.tokenizador.get_token().lower()
        self.estado = True #Almacena el estado del programa, cambia si se encuentra un error
    
    def avanza_token (self):
        """ Avanza un token en el archivo """
        siguiente_token = self.tokenizador.get_token().lower()
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
        while self.token_actual == 'define-nueva-instruccion' or self.token_actual == 'define-prototipo-instruccion' or self.token_actual == 'externo':
            if self.token_actual == 'define-nueva-instruccion':
                self.declaracion_de_procedimiento()
            elif self.token_actual == 'define-prototipo-instruccion':
                self.declaracion_de_prototipo()
            else:
                #Se trata de una declaracion de enlace 
                #TODO averiguar que cosa es esa
                self.declaracion_de_enlace()

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
        pass

    def clausula_no(self):
        """
        Define una clausula de negacion
        {
            ClausulaNo ::= ["NO"] ClausulaAtomica
        }
        """
        pass

    def clausula_y(self):
        """
        Define una clausula conjuntiva
        {
            ClausulaY ::= ClausulaNo ["Y" ClausulaNo]...
        }
        """
        pass

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
        self.avanza_token()
        

    def declaracion_de_prototipo(self):
        """
        Define una declaracion de prototipo
        {
            DeclaracionDePrototipo ::= "DEFINE-PROTOTIPO-INSTRUCCION" Identificador ["(" Identificador ")"]
        }
        """
        pass

    def declaracion_de_enlace (self):
        """ Se utilizará para tomar funciones de librerías externas,
        aun no implementado"""
        pass

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
        pass

    def expresion_entera(self):
        """
        Define una expresion numerica entera
        {
            ExpresionEntera ::= { Decimal | Identificador | "PRECEDE" "(" ExpresionEntera ")" | "SUCEDE" "(" ExpresionEntera ")" }{
        }
        """
        pass

    def expresion_general(self):
        """
        Define una expresion general
        { Expresion | ExpresionVacia }
        """
        pass

    def expresion_mientras(self):
        """
        Define la expresion del bucle MIENTRAS
        {
        ExpresionMientras ::= "Mientras" Termino "hacer"
                                  Expresion
        }
        """
        pass

    def expresion_repite(self):
        """
        Define la expresion del bucle REPITE
        {
        ExpresionRepite::= "repetir" ExpresionEntera "veces"
                              Expresion
        }
        """
        pass

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
        pass

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
        """
        pass

    def termino(self):
        """
        Define un termino
        {
            Termino ::= ClausulaY [ "o" ClausulaY] ...
        }
        """
        pass
    
    def verificar (self):
        """ Verifica que este correcta la gramatica de un programa
        en karel """
        if self.token_actual == 'iniciar-programa':
            if self.avanza_token():
                self.bloque()
                if self.token_actual != 'finalizar-programa':
                    print "Se esperaba 'finalizar-programa' al final del codigo"
                    self.estado = False
            else:
                self.estado = False
                print "Codigo mal formado"
        else:
            print "Se esperaba 'iniciar-programa' al inicio del programa"
            self.estado = False
        

if __name__ == "__main__":
    if len(sys.argv) == 1:
        gramar = kgrammar()
    else:
        fil = sys.argv[1]
        gramar = kgrammar(open(fil), fil)
    gramar.verificar()
    if gramar.estado:
        print "El programa esta correcto"
    else:
        print "Hay problemas con la sintaxis"
