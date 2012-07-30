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

        self.bkarel = wx.Bitmap('images/challenger/bkarel.png')
        self.knorte = wx.Bitmap('images/challenger/knorte.png')
        self.keste = wx.Bitmap('images/challenger/keste.png')
        self.koeste = wx.Bitmap('images/challenger/koeste.png')
        self.ksur = wx.Bitmap('images/challenger/ksur.png')

        self.pared_h = wx.Bitmap('images/challenger/pared_h.png')
        self.pared_v = wx.Bitmap('images/challenger/pared_v.png')

        for i in xrange(100):
            for j in xrange(100):
                fondo = wx.StaticBitmap(self, -1, self.bkarel)
                fondo.SetPosition((i*20+20, j*20+20))
        self.norte = wx.StaticBitmap(self, -1, self.knorte)
        self.norte.SetPosition((20, 2000))
        self.__dibujar_bordes()

    def __dibujar_bordes(self):
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

    def avanza(self):
        pos = self.norte.GetPosition()
        self.norte.SetPosition((pos[0], pos[1]-20))


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
        # end wxGlade

# end of class MyFrame


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)

    frame.mundoGUI.avanza()

    frame.Show(True)
    app.MainLoop()

