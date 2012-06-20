#coding:iso-8859-1
"""
Verifica que la gramática del archivo sea correcto según la sintaxis seleccionada
"""
import sys
from ktokenizer import ktokenizer

PROGRAM_NAME = "check_grammar"

def grammar(buff, lang='pascal'):
    """
    realiza la verificación de la gramatica
    """
    alexer = ktokenizer(buff)
    num_tokens = 0
    while True:
        token = alexer.get_token()
        if token:
            num_tokens += 1
            print token
        else:
            print "Se encontraron", num_tokens, "tokens"
            break

if __name__ == "__main__":
    lenguaje = 'pascal'
    verbose = False
    archivo = ""
    if len(sys.argv) > 1:
        #print sys.argv
        i = 1
        while i < len(sys.argv):
            if sys.argv[i] == '-l' or sys.argv[i] == '--lenguaje':
                lenguaje = sys.argv[i+1];
                i +=1
                #print "El lenguaje será", lenguaje
            elif sys.argv[i] == '-v' or sys.argv[i] == '--verbose':
                verbose = True
            elif sys.argv[i] == '-vl' or sys.argv[i] == '-lv':
                verbose = True
                lenguaje = sys.argv[i+1]
                #print "El lenguaje será", lenguaje
                i +=1
            else:
                archivo = open(sys.argv[i])
                #print sys.argv[i]
                break
            i +=1
        grammar(archivo, lenguaje)
    else:
        #TODO explicar mejor los argumentos
        print """
Modo de empleo: %s [OPCION] FICHERO

Revisa que la sintaxis de fichero sea la correcta en el lenguaje karel, por
defecto hace la revisión en Pascal

  -l, --lenguaje          Establece el lenguaje en que está escrito el fichero
  -v, --verbose           muestra un mensaje por cada error encontrado

Los archivos de karel son archivos de texto plano

Comunicar errores en %s
Página inicial de GNU coreutils: <http://www.gnu.org/software/coreutils/>
Ayuda general sobre el uso de software de GNU: <http://www.gnu.org/gethelp/>
Informe de errores de traducción chmod a <http://translationproject.org/team/>
Para la documentación completa, ejecute: info coreutils `chmod invocation'
        """%(PROGRAM_NAME, PROGRAM_NAME)
