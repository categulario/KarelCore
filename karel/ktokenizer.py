# -*- coding: iso-8859-1 -*-
"""
Un analizador lexico para archivos Karel, basado en el módulo shlex de python
"""

import os.path
import sys
from collections import deque
from kutil import KarelException

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class ktokenizer:
    """ Un tokenizador diseñado para la sintaxis de Karel el Robot,
    osea un analizador léxico"""
    def __init__(self, instream=None, infile=None):
        if isinstance(instream, basestring):
            instream = StringIO(instream)
        if instream is not None:
            self.instream = instream
            self.infile = infile
        else:
            self.instream = sys.stdin
            self.infile = None
        self.eof = ''
        self.commenters = ('#')
        self.wordchars = ('abcdfeghijklmnopqrstuvwxyz'
                          'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-')
        self.whitespace = ' \t\r\n'
        self.whitespace_split = False
        self.quotes = '\'"/' #Comillas agrupadoras, se usaran como comentarios multi-linea
        self.escape = '\\'  #Caracter de escape
        self.escapedquotes = '"'
        self.state = ' '
        #El estado en que se encuentra el tokenizador
        self.pushback = deque()
        self.lineno = 1
        self.has_lineno_change = False #Indica cuando hay que cambiar de linea, usado para corregir el conteo de lineas
        self.debug = 0
        self.token = ''
        self.filestack = deque()
        self.source = None
        if self.debug:
            print 'shlex: reading from %s, line %d' \
                  % (self.instream, self.lineno)

    def push_token(self, tok):
        "Pone un token en la pila obtenido por el método get_token"
        if self.debug >= 1:
            print "shlex: pushing token " + repr(tok)
        self.pushback.appendleft(tok)

    def push_source(self, newstream, newfile=None):
        "Push an input source onto the lexer's input source stack."
        if isinstance(newstream, basestring):
            newstream = StringIO(newstream)
        self.filestack.appendleft((self.infile, self.instream, self.lineno))
        self.infile = newfile
        self.instream = newstream
        self.lineno = 1
        if self.debug:
            if newfile is not None:
                print 'shlex: pushing to file %s' % (self.infile,)
            else:
                print 'shlex: pushing to stream %s' % (self.instream,)

    def pop_source(self):
        "Pop the input source stack."
        self.instream.close()
        (self.infile, self.instream, self.lineno) = self.filestack.popleft()
        if self.debug:
            print 'shlex: popping to %s, line %d' \
                  % (self.instream, self.lineno)
        self.state = ' '

    def get_token(self):
        "Obtiene un token del buffer de entrada (O de la pila si no esta vacia)"
        if self.pushback:
            tok = self.pushback.popleft()
            if self.debug >= 1:
                print "shlex: popping token " + repr(tok)
            return tok
        # No pushback.  Get a token.
        raw = self.read_token()
        # Handle inclusions
        if self.source is not None:
            while raw == self.source:
                spec = self.sourcehook(self.read_token())
                if spec:
                    (newfile, newstream) = spec
                    self.push_source(newstream, newfile)
                raw = self.get_token()
        # Maybe we got EOF instead?
        while raw == self.eof:
            if not self.filestack:
                return self.eof
            else:
                self.pop_source()
                raw = self.get_token()
        # Neither inclusion nor EOF
        if self.debug >= 1:
            if raw != self.eof:
                print "shlex: token=" + repr(raw)
            else:
                print "shlex: token=EOF"
        return raw

    def read_token(self):
        """
        Lee solamente un Token del archivo de entrada y lo devuelve
        """
        quoted = False
        escapedstate = ' '

        while True:
            if self.has_lineno_change:
                self.lineno +=1
                self.has_lineno_change = False

            nextchar = self.instream.read(1) #Lee un caracter del bufer de entrada
            if nextchar == '\n':
                self.has_lineno_change = True
            if self.debug >= 3:
                print "shlex: in state", repr(self.state), \
                      "I see character:", repr(nextchar)
            if self.state is None:
                self.token = ''        # past end of file
                break
            elif self.state == ' ':
                #WiteSpace state
                if not nextchar:
                    self.state = None  # end of file
                    break
                elif nextchar in self.whitespace:
                    if self.debug >= 2:
                        print "shlex: I see whitespace in whitespace state"
                    if self.token:
                        break   # emit current token
                    else:
                        continue
                elif nextchar in self.commenters: #Si es un comentario nos comemos la linea completa
                    self.instream.readline()
                    #self.lineno = self.lineno + 1
                    self.has_lineno_change = True
                elif nextchar in self.wordchars:
                    self.token = nextchar
                    self.state = 'a'
                elif nextchar in self.quotes:
                    self.token = nextchar
                    self.state = nextchar
                elif self.whitespace_split:
                    self.token = nextchar
                    self.state = 'a'
                else:
                    self.token = nextchar
                    if self.token:
                        break   # emit current token
                    else:
                        continue
            elif self.state in self.quotes:
                quoted = True
                if not nextchar:      # end of file
                    if self.debug >= 2:
                        print "shlex: I see EOF in quotes state"
                    # XXX what error should be raised here?
                    raise KarelException("Hay un comentario de varias lineas que no termina")
                if nextchar == self.state:
                    self.token = ''
                    self.state = ' '
                else:
                    self.token = self.token + nextchar
            elif self.state in self.escape:
                if not nextchar:      # end of file
                    if self.debug >= 2:
                        print "shlex: I see EOF in escape state"
                    # XXX what error should be raised here?
                    raise KarelException("Se colocó caracter de escape, pero no hay de dónde escapar =)")
                # character may be escaped within quotes.
                if escapedstate in self.quotes and \
                   nextchar != self.state and nextchar != escapedstate:
                    self.token = self.token + self.state
                self.token = self.token + nextchar
                self.state = escapedstate
            elif self.state == 'a':
                #Word state
                if not nextchar:
                    self.state = None   # end of file
                    break
                elif nextchar in self.whitespace:
                    if self.debug >= 2:
                        print "shlex: I see whitespace in word state"
                    self.state = ' '
                    break   # emit current token
                elif nextchar in self.commenters:
                    self.instream.readline()
                    #self.lineno = self.lineno + 1
                    self.has_lineno_change = True
                elif nextchar in self.wordchars or nextchar in self.quotes \
                    or self.whitespace_split:
                    self.token = self.token + nextchar
                else:
                    self.pushback.appendleft(nextchar)
                    if self.debug >= 2:
                        print "shlex: I see punctuation in word state"
                    self.state = ' '
                    if self.token:
                        break   # emit current token
                    else:
                        continue
        result = self.token
        self.token = ''
        if self.debug > 1:
            if result:
                print "shlex: raw token=" + repr(result)
            else:
                print "shlex: raw token=EOF"
        return result

    def sourcehook(self, newfile):
        "Hook called on a filename to be sourced."
        if newfile[0] == '"':
            newfile = newfile[1:-1]
        # This implements cpp-like semantics for relative-path inclusion.
        if isinstance(self.infile, basestring) and not os.path.isabs(newfile):
            newfile = os.path.join(os.path.dirname(self.infile), newfile)
        return (newfile, open(newfile, "r"))

    def error_leader(self, infile=None, lineno=None):
        "Emit a C-compiler-like, Emacs-friendly error-message leader."
        if infile is None:
            infile = self.infile
        if lineno is None:
            lineno = self.lineno
        return "\"%s\", line %d: " % (infile, lineno)

    def __iter__(self):
        return self

    def next(self):
        token = self.get_token()
        if token == self.eof:
            raise StopIteration
        return token

def split(s, comments=False):
    lex = ktokenizer(s)
    lex.whitespace_split = True
    if not comments:
        lex.commenters = ''
    return list(lex)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        lexer = ktokenizer()
    else:
        fil = sys.argv[1]
        lexer = ktokenizer(open(fil), fil)
    while True:
        tt = lexer.get_token()
        if tt:
            print "Token: " + repr(tt), "\t\t","Line: " + str(lexer.lineno)
        else:
            break

"""
FIN @Categulario
"""
