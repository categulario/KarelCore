#frame.py
import wx
from wx import stc #Developingo 2012-07-23

class my_frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200, 100))
        self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE) #Developingo 2012-07-23
        self.Show(True)

if __name__ == "__main__":
    app = wx.App(False)
    frame = my_frame(None, 'Small editor')
    app.MainLoop()
