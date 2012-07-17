import wx
class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        panel = wx.Panel(self)
        self.quote = wx.StaticText(panel, label="Your quote: bvyegfyueu", pos=(20, 30))
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    ExampleFrame(None)
    app.MainLoop()
