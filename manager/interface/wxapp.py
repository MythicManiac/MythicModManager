import wx

from .generated import MainFrame


class Application:
    def __init__(self):
        self.app = wx.App(0)
        self.main_frame = MainFrame(None)

    def launch(self):
        self.main_frame.Show()
        self.app.MainLoop()
