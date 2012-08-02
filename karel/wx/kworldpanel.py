#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  kworldpanel.py
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

import wx

class kworldpanel(wx.Panel):
    """ Define específicamente el área del mundo, de 100 x 100 casillas
    y las instrucciones básicas para su operación. """

    def __init__ (self, parent):
        """ Crea una instancia del mundo gráfico de Karel. """
        super(kworldpanel, self).__init__(parent, -1)
        self.SetMinSize((2040, 2040))
        #Carga de las imágenes necesarias
        self.bkarel = wx.Bitmap('images/challenger/bkarel.png')
        self.knorte = wx.Bitmap('images/challenger/knorte.png')
        self.keste = wx.Bitmap('images/challenger/keste.png')
        self.koeste = wx.Bitmap('images/challenger/koeste.png')
        self.ksur = wx.Bitmap('images/challenger/ksur.png')
        self.zumbadores = dict()
        for i in xrange(100):
            self.zumbadores.update({i+1: wx.Bitmap('zumbadores/bkarel_'+str(i+1)+'.png')})
        self.zumbadores.update({'inf': wx.Bitmap('zumbadores/bkarel_inf.png')})
        #Construcción del mundo
        self.orientacion = 'norte'
        self.casillas = []

        self.pared_h = wx.Bitmap('images/challenger/pared_h.png')
        self.pared_v = wx.Bitmap('images/challenger/pared_v.png')
        opciones = ['Karel al norte', 'Karel al sur', 'Karel al este', 'Karel al oeste', 'sin zumbadores', '1 zumbador']
        opciones += [str(i)+' zumbadores' for i in xrange(2, 5)]
        opciones += ['n zumbadores', 'infinitos zumbadores']
        self.menu_contextual = wx.Menu()
        self.ultima_posicion = (0, 0)
        for text in opciones:
            item = self.menu_contextual.Append(-1, text)
            if 'oeste' in text:
                self.menu_contextual.AppendSeparator()
            self.Bind(wx.EVT_MENU, self.menu_contextual_item_seleccionado, item)

        self.Bind(wx.EVT_CONTEXT_MENU, self.menu_contextual_evt)
        self.Bind(wx.EVT_BUTTON, self.click_en_mundo)

        self.__inicializar()

    def click_en_mundo (self, event):
        """ Agrega paredes en ciertas zonas """
        print "hey!"

    def menu_contextual_evt(self, event):
        """Muestra el menu contextual de Karel"""
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.ultima_posicion = pos
        self.PopupMenu(self.menu_contextual, pos)

    def menu_contextual_item_seleccionado (self, event):
        """ Function doc """
        item = self.menu_contextual.FindItemById(event.GetId())
        texto = item.GetText()
        if 'zumbador' in texto:
            wx.MessageBox("Seleccionaste: '%s'" % texto)
        else:
            casilla = self.pixeles_a_filas(self.ultima_posicion)
            #wx.MessageBox("Estoy moviendo a Karel a "+str(casilla))
            self.karel_a_casilla(casilla[0], casilla[1])

    def pixeles_a_filas(self, posicion):
        """Obtiene una tupla en 'posicion' con coordenadas en pixeles y
        obtiene la fila y la columna a la que corresponde"""
        return (101-posicion[1]/20, posicion[0]/20)

    def __inicializar(self):
        """inicializa el mundo gráfico"""
        #Numeros de fila y columna
        fuente = wx.Font(10, wx.SCRIPT, wx.NORMAL, wx.NORMAL)
        for i in xrange(1, 101):
            wx.StaticText(self, -1, str(101-i), (2, i*20)).SetFont(fuente)
        for i in xrange(1, 101):
            wx.StaticText(self, -1, str(i), (i*20+3, 2022)).SetFont(fuente)

        self.casillas = [[wx.StaticBitmap(self, -1, self.bkarel) for i in xrange(100)] for i in xrange(100)]
        i = 0
        j = 0
        for fila in self.casillas:
            j = 0
            for casilla in fila:
                casilla.SetPosition((i*20+20, j*20+20))
                j += 1
            i += 1

        self.karel = wx.StaticBitmap(self, -1, self.knorte)
        self.karel.SetPosition((20, 2000))

        for i in xrange(100):
            pared = wx.StaticBitmap(self, -1, self.pared_h)
            pared.SetPosition((i*20+20, 2018))

        for i in xrange(100):
            pared = wx.StaticBitmap(self, -1, self.pared_v)
            pared.SetPosition((20, 1998-i*20))

        for i in xrange(100):
            pared = wx.StaticBitmap(self, -1, self.pared_h)
            pared.SetPosition((i*20+20, 18))

        for i in xrange(100):
            pared = wx.StaticBitmap(self, -1, self.pared_v)
            pared.SetPosition((2018, 1998-i*20))

    def gira_izquierda(self):
        """gira a la izquierda"""
        if self.orientacion == 'norte':
            self.karel.SetBitmap(self.koeste)
            self.orientacion = 'oeste'
        elif self.orientacion == 'este':
            self.karel.SetBitmap(self.knorte)
            self.orientacion = 'norte'
        elif self.orientacion == 'sur':
            self.karel.SetBitmap(self.keste)
            self.orientacion = 'este'
        elif self.orientacion == 'oeste':
            self.karel.SetBitmap(self.ksur)
            self.orientacion = 'sur'

    def avanza(self):
        """Avanza a karel una casilla hacia donde se encuentre orientado
        """
        pos = self.karel.GetPosition()
        if self.orientacion == 'norte':
            self.karel.SetPosition((pos[0], pos[1]-20))
        elif self.orientacion == 'este':
            self.karel.SetPosition((pos[0]+20, pos[1]))
        elif self.orientacion == 'sur':
            self.karel.SetPosition((pos[0], pos[1]+20))
        elif self.orientacion == 'oeste':
            self.karel.SetPosition((pos[0]-20, pos[1]))

    def deja_zumbador(self, fila, columna):
        """deja un zumbador en la posicion actual"""
        self.casillas[fila-1][100-columna].SetBitmap(self.zumbadores[1])

    def pon_zumbadores(self, fila, columna, cantidad):
        """Pone una cantidad arbitraria de zumbadores en la posicion
        actual"""
        self.casillas[fila-1][100-columna].SetBitmap(self.zumbadores[cantidad])

    def agrega_pared (self, casilla, orientacion):
        """ Agrega una pared al mundo y la pinta.
        casilla es una tupla con la fila, columna
        orientacion es la cadena que dice pa'donde' """
        if orientacion == 'norte':
            #Se trata de una pared horizontal
            pass
        elif orientacion == 'este':
            #Se trata de una pared vertical
            pass

    def karel_a_casilla(self, fila, columna):
        """Manda a karel a una casilla especifica identificada por su
        fila y su columna. """
        self.karel.SetPosition((20+(columna-1)*20, 2000-(fila-1)*20))

    def orienta_a_karel (self, orientacion):
        """ Cambia la orientacion de Karel. """
        if orientacion in ['norte', 'este', 'sur', 'oeste']:
            self.orientacion = orientacion
            eval('self.karel.SetBitmap(self.k'+orientacion+')')



if __name__ == '__main__':
    class MyFrame(wx.Frame):
        def __init__(self, *args, **kwds):
            # begin wxGlade: MyFrame.__init__
            kwds["style"] = wx.DEFAULT_FRAME_STYLE
            wx.Frame.__init__(self, *args, **kwds)
            self.panel_1 = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)
            self.mundoGUI = kworldpanel(self.panel_1)

            self.__set_properties()
            self.__do_layout()
            # end wxGlade

        def __set_properties(self):
            # begin wxGlade: MyFrame.__set_properties
            self.SetTitle("Pruebas con el mundo de Karel")
            self.SetSize((400, 300))
            #self.mundoGUI.SetMinSize((2040, 2040))
            self.panel_1.SetScrollRate(20, 20)
            # end wxGlade

        def __do_layout(self):
            # begin wxGlade: MyFrame.__do_layout
            sizer_1 = wx.BoxSizer(wx.VERTICAL)
            sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_2.Add(self.mundoGUI, 1, wx.EXPAND, 0)
            self.panel_1.SetSizer(sizer_2)
            sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
            self.SetSizer(sizer_1)
            self.Layout()
            self.panel_1.Scroll(0, 1900)


    app = wx.App()
    frame = MyFrame(None)
    frame.mundoGUI.karel_a_casilla(1, 3)

    frame.mundoGUI.pon_zumbadores(2, 2, 'inf')
    frame.mundoGUI.pon_zumbadores(8, 2, 100)
    frame.mundoGUI.pon_zumbadores(2, 8, 45)
    frame.mundoGUI.pon_zumbadores(3, 5, 1)
    frame.mundoGUI.pon_zumbadores(6, 7, 19)

    #frame.mundoGUI.orienta_a_karel('este')

    #frame.mundoGUI.avanza()
    #frame.mundoGUI.gira_izquierda()
    #frame.mundoGUI.gira_izquierda()
    #frame.mundoGUI.gira_izquierda()
    #frame.mundoGUI.avanza()
    #frame.mundoGUI.gira_izquierda()

    frame.Show(True)
    app.MainLoop()

