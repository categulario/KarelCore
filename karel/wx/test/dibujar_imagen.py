import wx

def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result

class KarelPanel(wx.Panel):
    def __init__(self, parent, path):
        super(KarelPanel, self).__init__(parent, -1)
        bitmap = wx.Bitmap(path)
        bitmap = scale_bitmap(bitmap, 20, 20)
        for i in xrange(20):
            for j in xrange(20):
                control = wx.StaticBitmap(self, -1, bitmap)
                control.SetPosition((i*20, j*20))


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1, 'Scaled Image', size=(400, 400))
    panel = KarelPanel(frame, '../default/bkarel.png')
    frame.Show()
    app.MainLoop()
