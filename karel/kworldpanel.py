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
import wxversion
wxversion.select("2.8")

import wx
import time
from kworld import kworld
from random import choice

if __name__ == "__main__":
    from pprint import pprint

class kworldpanel(wx.Panel, kworld):
    """ Define específicamente el área del mundo, de 100 x 100 casillas
    y las instrucciones básicas para su operación. """

    def __init__ (self, parent):
        """ Crea una instancia del mundo gráfico de Karel. """
        #super(kworldpanel, self).__init__(parent, -1)
        wx.Panel.__init__(self, parent, -1)
        kworld.__init__(self)
        self.SetMinSize((2040, 2040))
        #Carga de las imágenes necesarias
        self.bkarel = wx.Bitmap('wx/images/challenger/bkarel.png')
        self.knorte = wx.Bitmap('wx/images/challenger/knorte.png')
        self.keste = wx.Bitmap('wx/images/challenger/keste.png')
        self.koeste = wx.Bitmap('wx/images/challenger/koeste.png')
        self.ksur = wx.Bitmap('wx/images/challenger/ksur.png')
        self.zumbadores = dict()
        for i in xrange(100):
            self.zumbadores.update({i+1: wx.Bitmap('wx/zumbadores/bkarel_'+str(i+1)+'.png')})
        self.zumbadores.update({0:self.bkarel})
        self.zumbadores.update({'inf': wx.Bitmap('wx/zumbadores/bkarel_inf.png')})
        #Construcción del mundo
        self.mundo['karel']['orientacion'] = 'norte'
        self.casillas = []

        self.pared_h = wx.Bitmap('wx/images/challenger/pared_h.png')
        self.pared_v = wx.Bitmap('wx/images/challenger/pared_v.png')
        opciones = ['Karel al norte', 'Karel al sur', 'Karel al este', 'Karel al oeste', 'sin zumbadores', '1 zumbador']
        opciones += [str(i)+' zumbadores' for i in xrange(2, 5)]
        opciones += ['n zumbadores', 'infinitos zumbadores', 'muchos zumbadores']
        self.menu_contextual = wx.Menu()
        self.ultima_posicion = (0, 0)
        for text in opciones:
            item = self.menu_contextual.Append(-1, text)
            if 'oeste' in text:
                self.menu_contextual.AppendSeparator()
            self.Bind(wx.EVT_MENU, self.menu_contextual_item_seleccionado, item)

        self.Bind(wx.EVT_CONTEXT_MENU, self.menu_contextual_evt)

        self.paredes = dict() #Diccionario con las paredes del mundo
        #Utilerías para pintar rápido
        self.brocha_rapida = False #Activa la brocha rápida
        self.valor_brocha = 1 #Indica cuántos zumbadores pinta la brocha
        self.valores = [i for i in xrange(1, 101)]
        #El valor anterior puede ser 0..100, 'inf' o 'random'

        self.__inicializar()

    def click_en_mundo (self, event):
        """ Agrega paredes en ciertas zonas, o pinta con la brocha
        rápida si es posible """
        casilla = event.GetEventObject()
        fila, columna = self.pixeles_a_filas(casilla.GetPosition())
        if self.brocha_rapida:
            if self.valor_brocha == 'random':
                self.pon_zumbadores(fila, columna, choice(self.valores))
            else:
                self.pon_zumbadores(fila, columna, self.valor_brocha)
        else:
            x, y = event.GetPosition()
            orientacion = ''
            if x < 6 or x > 14 or y < 6 or y > 14:
                #No esta en el centro de 8*8
                if x > y:
                    #zona noreste
                    if 20-y<x:
                        #este
                        orientacion = 'este'
                    else:
                        #norte
                        orientacion = 'norte'
                else:
                    #zona sudoeste
                    if 20-y<x:
                        #sur
                        orientacion = 'norte'
                        fila -= 1
                    else:
                        #oeste
                        orientacion = 'este'
                        columna -= 1
                if 0<fila<101 and 0<columna<101:
                    self.conmuta_pared(fila, columna, orientacion)

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
            #wx.MessageBox("Seleccionaste: '%s'" % texto)
            num_zumbadores = texto.split(' ')[0]
            cantidad_zumbadores = 0
            if num_zumbadores in '123456789':
                cantidad_zumbadores = int(num_zumbadores)
            elif num_zumbadores == 'infinitos':
                cantidad_zumbadores = 'inf'
            elif num_zumbadores == 'muchos':
                #TODO mejorar la brocha
                if not self.brocha_rapida:
                    dlg = wx.TextEntryDialog(None, "Indica cuántos zumbadores ha de pintar la brocha,\nvalores válidos para esta brocha son inf, random,\n y números del 0 al 100",
                        "Brocha rápida")
                    if dlg.ShowModal() == wx.ID_OK:
                        if dlg.GetValue() in ['inf', 'random']:
                            self.valor_brocha = dlg.GetValue()
                            self.brocha_rapida = True
                        else:
                            try:
                                cantidad_zumbadores = int(dlg.GetValue())
                                if cantidad_zumbadores<1 or cantidad_zumbadores>100:
                                    wx.MessageBox("El numero que me diste no esta en el rango de los permitidos")
                                    #obtener numero de zumbadores en casilla actual
                                    cantidad_zumbadores = 0 #TODO quitar
                                self.brocha_rapida = True
                                self.valor_brocha = cantidad_zumbadores
                            except ValueError:
                                wx.MessageBox("Vamos, eso no es un numero entero")
                else:
                    self.brocha_rapida = False
            elif num_zumbadores == 'n':
                dlg = wx.TextEntryDialog(None, "Cuantos zumbadores?",'Dame un numero de zumbadores')
                if dlg.ShowModal() == wx.ID_OK:
                    try:
                        cantidad_zumbadores = int(dlg.GetValue())
                        if cantidad_zumbadores<1 or cantidad_zumbadores>100:
                            wx.MessageBox("El numero que me diste no esta en el rango de los permitidos")
                            #obtener numero de zumbadores en casilla actual
                            cantidad_zumbadores = 0 #TODO quitar
                    except ValueError:
                        wx.MessageBox("Vamos, eso no es un numero entero")
                dlg.Destroy()
            fila, columna = self.pixeles_a_filas(self.ultima_posicion)
            if 0<fila<101 and 0<columna<101 and not self.brocha_rapida:
                self.pon_zumbadores(fila, columna, cantidad_zumbadores)
        else:
            fila, columna = self.pixeles_a_filas(self.ultima_posicion)
            if 0<fila<101 and 0<columna<101:
                self.karel_a_casilla(fila, columna, texto.split(' ')[2])

    def pixeles_a_filas(self, posicion):
        """Obtiene una tupla en 'posicion' con coordenadas en pixeles y
        obtiene la fila y la columna a la que corresponde"""
        return (101-posicion[1]/20, posicion[0]/20)

    def __inicializar(self):
        """inicializa el mundo gráfico, es un metodo privado"""
        #Numeros de fila y columna
        fuente = wx.Font(10, wx.SCRIPT, wx.NORMAL, wx.NORMAL)
        for i in xrange(1, 101):
            #Paredes de las orillas en las filas
            wx.StaticText(self, -1, str(101-i), (2, i*20)).SetFont(fuente)
            wx.StaticText(self, -1, str(101-i), (2022, i*20)).SetFont(fuente)
        for i in xrange(1, 101):
            #paredes en las orillas de las columnas
            wx.StaticText(self, -1, str(i), (i*20+3, 2022)).SetFont(fuente)
            wx.StaticText(self, -1, str(i), (i*20+3, 2)).SetFont(fuente)

        self.casillas = [[wx.StaticBitmap(self, -1, self.bkarel) for i in xrange(100)] for i in xrange(100)]
        i = 0
        j = 0
        for fila in self.casillas:
            j = 0
            for casilla in fila:
                casilla.SetPosition((i*20+20, j*20+20))
                casilla.Bind(wx.EVT_LEFT_UP, self.click_en_mundo)
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
        if self.mundo['karel']['orientacion'] == 'norte':
            self.karel.SetBitmap(self.koeste)
            self.mundo['karel']['orientacion'] = 'oeste'
        elif self.mundo['karel']['orientacion'] == 'este':
            self.karel.SetBitmap(self.knorte)
            self.mundo['karel']['orientacion'] = 'norte'
        elif self.mundo['karel']['orientacion'] == 'sur':
            self.karel.SetBitmap(self.keste)
            self.mundo['karel']['orientacion'] = 'este'
        elif self.mundo['karel']['orientacion'] == 'oeste':
            self.karel.SetBitmap(self.ksur)
            self.mundo['karel']['orientacion'] = 'sur'

    def avanza(self):
        """Avanza a karel una casilla hacia donde se encuentre orientado
        """
        if super(kworldpanel, self).avanza():
            pos = self.karel.GetPosition()
            if self.mundo['karel']['orientacion'] == 'norte':
                self.karel.SetPosition((pos[0], pos[1]-20))
            elif self.mundo['karel']['orientacion'] == 'este':
                self.karel.SetPosition((pos[0]+20, pos[1]))
            elif self.mundo['karel']['orientacion'] == 'sur':
                self.karel.SetPosition((pos[0], pos[1]+20))
            elif self.mundo['karel']['orientacion'] == 'oeste':
                self.karel.SetPosition((pos[0]-20, pos[1]))
        else:
            wx.MessageBox("Karel ha chocado con una pared!")

    def deja_zumbador(self):
        """deja un zumbador en la posicion actual"""
        fila, columna = self.mundo['karel']['posicion']
        if super(kworldpanel, self).deja_zumbador():
            self.casillas[fila-1][100-columna].SetBitmap(
                self.zumbadores[self.mundo['casillas'][(fila, columna)]['zumbadores']]
            )
        else:
            wx.MessageBox(u"Karel quizo dejar un zumbador pero su mochila estaba vacía")

    def coge_zumbador(self):
        """deja un zumbador en la posicion actual"""
        fila, columna = self.mundo['karel']['posicion']
        if super(kworldpanel, self).coge_zumbador():
            self.casillas[fila-1][100-columna].SetBitmap(
                self.zumbadores[self.mundo['casillas'][(fila, columna)]['zumbadores']]
            )
        else:
            wx.MessageBox(u"Karel quizo coger un zumbador pero no había de donde")

    def pon_zumbadores(self, fila, columna, cantidad):
        """Pone una cantidad arbitraria de zumbadores en la posicion
        actual"""
        super(kworldpanel, self).pon_zumbadores((fila, columna), cantidad)
        self.casillas[columna-1][100-fila].SetBitmap(self.zumbadores[cantidad])

    def conmuta_pared (self, fila, columna, orientacion):
        """ Agrega una pared al mundo y la pinta.
        casilla es una tupla con la fila, columna
        orientacion es la cadena que dice pa'donde' """
        super(kworldpanel, self).conmuta_pared((fila, columna), orientacion)
        if orientacion == 'norte':
            #Se trata de una pared horizontal
            if self.paredes.has_key((fila, columna)):
                if self.paredes[(fila, columna)]['norte']:
                    self.paredes[(fila, columna)]['norte'].Destroy()
                else:
                    self.paredes[(fila, columna)]['norte'] = wx.StaticBitmap(self, -1, self.pared_h)
                    self.paredes[(fila, columna)]['norte'].SetPosition((20+(columna-1)*20, 1998-(fila-1)*20))
            else:
                self.paredes.update({
                    (fila, columna): {
                        'norte': wx.StaticBitmap(self, -1, self.pared_h),
                        'este': None
                    }
                })
                self.paredes[(fila, columna)]['norte'].SetPosition((20+(columna-1)*20, 1998-(fila-1)*20))
        elif orientacion == 'este':
            #Se trata de una pared vertical
            if self.paredes.has_key((fila, columna)):
                if self.paredes[(fila, columna)]['este']:
                    self.paredes[(fila, columna)]['este'].Destroy()
                else:
                    self.paredes[(fila, columna)]['este'] = wx.StaticBitmap(self, -1, self.pared_v)
                    self.paredes[(fila, columna)]['este'].SetPosition((38+(columna-1)*20, 1998-(fila-1)*20))
            else:
                self.paredes.update({
                    (fila, columna): {
                        'norte': None,
                        'este': wx.StaticBitmap(self, -1, self.pared_v)
                    }
                })
                self.paredes[(fila, columna)]['este'].SetPosition((38+(columna-1)*20, 1998-(fila-1)*20))

    def karel_a_casilla(self, fila, columna, orientacion='norte'):
        """Manda a karel a una casilla especifica identificada por su
        fila y su columna. """
        if 0<fila<101 and 0<columna<101 and orientacion in ['norte', 'este', 'sur', 'oeste']:
            self.karel.SetPosition((20+(columna-1)*20, 2000-(fila-1)*20))
            eval('self.karel.SetBitmap(self.k'+orientacion+')')
            self.mundo['karel']['posicion'] = (fila, columna)
            self.mundo['karel']['orientacion'] = orientacion



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
    #frame.mundoGUI.karel_a_casilla(1, 3)
    #~ for i in xrange(1, 11):
        #~ frame.mundoGUI.conmuta_pared(i, 1, 'norte')
        #~ frame.mundoGUI.conmuta_pared(i, 1, 'este')
    #frame.mundoGUI.conmuta_pared(1, 1, 'norte')
    #frame.mundoGUI.conmuta_pared(1, 1, 'norte')
    #pprint(frame.mundoGUI.mundo)
    #
    #frame.mundoGUI.pon_zumbadores(8, 2, 100)
    #frame.mundoGUI.pon_zumbadores(2, 8, 45)
    #frame.mundoGUI.pon_zumbadores(3, 5, 1)
    #frame.mundoGUI.pon_zumbadores(6, 7, 19)

    #frame.mundoGUI.orienta_a_karel('este')

    frame.Show(True)
    app.MainLoop()

