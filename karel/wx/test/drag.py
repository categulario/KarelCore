#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sin título.py
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
class TextDropTarget(wx.TextDropTarget):
   """ This object implements Drop Target functionality for Text """
   def __init__(self, obj):
      """ Initialize the Drop Target, passing in the Object Reference to
          indicate what should receive the dropped text """
      # Initialize the wx.TextDropTarget Object
      wx.TextDropTarget.__init__(self)
      # Store the Object Reference for dropped text
      self.obj = obj

   def OnDropText(self, x, y, data):
      """ Implement Text Drop """
      # When text is dropped, write it into the object specified
      self.obj.WriteText(data + '\n\n')

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(450, 350))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(self, -1)
        txtbox = wx.TextCtrl(self)
        dt1 = TextDropTarget(txtbox)
        # Link the Drop Target Object to the Text Control
        txtbox.SetDropTarget(dt1)

        self.tree = wx.TreeCtrl(panel1, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        root = self.tree.AddRoot('Programmer')
        os = self.tree.AppendItem(root, 'Operating Systems')
        pl = self.tree.AppendItem(root, 'Programming Languages')
        tk = self.tree.AppendItem(root, 'Toolkits')
        self.tree.AppendItem(os, 'Linux')
        self.tree.AppendItem(os, 'FreeBSD')
        self.tree.AppendItem(os, 'OpenBSD')
        self.tree.AppendItem(os, 'NetBSD')
        self.tree.AppendItem(os, 'Solaris')
        self.tree.AppendItem(pl, 'Java')
        self.tree.AppendItem(pl, 'C++')
        self.tree.AppendItem(pl, 'C')
        self.tree.AppendItem(pl, 'Pascal')
        self.tree.AppendItem(pl, 'Python')
        self.tree.AppendItem(pl, 'Ruby')
        self.tree.AppendItem(pl, 'Tcl')
        self.tree.AppendItem(pl, 'PHP')
        self.tree.AppendItem(tk, 'Qt')
        self.tree.AppendItem(tk, 'MFC')
        self.tree.AppendItem(tk, 'wxPython')
        self.tree.AppendItem(tk, 'GTK+')
        self.tree.AppendItem(tk, 'Swing')
        self.display = wx.StaticText(txtbox, -1, '',(10,10), style=wx.ALIGN_CENTRE)
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(panel1, 1, wx.EXPAND)
        hbox.Add(txtbox, 1, wx.EXPAND)
        panel1.SetSizer(vbox)
        self.SetSizer(hbox)
        self.Centre()
        self.tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
        self.tree.Bind(wx.EVT_TREE_END_DRAG, self.OnEndDrag)


    def OnBeginDrag(self, event):
        '''Allow drag-and-drop for leaf nodes.'''
        """ Begin a Drag Operation """
        # Create a Text Data Object, which holds the text that is to be dragged
        tdo = wx.PyTextDataObject(self.tree.GetItemText(event.GetItem()))
        # Create a Drop Source Object, which enables the Drag operation
        tds = wx.DropSource(self.tree)
        # Associate the Data to be dragged with the Drop Source Object
        tds.SetData(tdo)
        # Initiate the Drag Operation
        tds.DoDragDrop(True)

        print("OnBeginDrag")
        if self.tree.GetChildrenCount(event.GetItem()) == 0:
            event.Allow()
            self.dragItem = event.GetItem()
        else:
            print("Cant drag a node that has children")


    def OnEndDrag(self, event):
        '''Do the re-organization if possible'''

        print("OnEndDrag")
       #If we dropped somewhere that isn't on top of an item, ignore the event
        if not event.GetItem().IsOk():
            return

        # Make sure this memeber exists.
        try:
            old = self.dragItem
        except:
            return

        # Get the other IDs that are involved
        new = event.GetItem()
        parent = self.tree.GetItemParent(new)
        if not parent.IsOk():
            return

        # Move 'em
        text = self.tree.GetItemText(old)
        self.tree.Delete(old)
        self.tree.InsertItem(parent, new, text)





class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'treectrl.py')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()

