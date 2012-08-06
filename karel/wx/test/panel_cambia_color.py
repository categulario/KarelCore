import wx

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.panel = wx.Panel(self)
        self.panel.BackgroundColour = wx.RED
        self.panel.Bind(wx.EVT_LEFT_UP, self.onClick)

    def onClick(self, event):
        self.panel.BackgroundColour = wx.GREEN

app = wx.App()
frame = MyFrame()
frame.Show(True)
app.MainLoop()
