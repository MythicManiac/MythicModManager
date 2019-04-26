import wx
import wx.grid
import sys
from pathlib import Path
import inspect
import threading


class GridFrame(wx.Frame):
    def __init__(self, parent):

        # This code still needs cleaning and isn't finished yet

        # wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE)
        self.SetSize(wx.DLG_UNIT(self, wx.Size(300, 260)))

        self.itemset = set([])
        self.cellection = []

        listA = wx.ListBox(choices=[], name='LeftList', parent=self, style=0)

        listB = wx.ListBox(choices=[], name='RightList', parent=self, style=0)

        sizer_0 = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        sizer_bar = wx.BoxSizer(wx.HORIZONTAL)
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)

        sizer_0.Add(sizer_bar, 1, wx.EXPAND)
        sizer_0.Add(sizer_buttons, 0, wx.EXPAND)
        sizer_0.Add(sizer_1, 3, wx.EXPAND)

        sizer_1.Add(listA, 1, wx.EXPAND)
        sizer_1.Add(sizer_2, 0, wx.CENTER)
        sizer_1.Add(listB, 1, wx.EXPAND)

        image = wx.Image("icon.png").Scale(180, 180)
        print(image)
        self.bmp = wx.StaticBitmap(self, bitmap=wx.Bitmap(image, wx.IMAGE_QUALITY_HIGH))

        infoscreen = wx.TextCtrl(self, value="Mod info")

        sizer_bar.Add(self.bmp, 1, wx.CENTER)
        sizer_bar.Add(infoscreen, 2, wx.EXPAND)

        button_bepis = wx.Button(self, wx.ID_ANY, "Update Bepis")
        button_bepis.Bind(wx.EVT_BUTTON, self.OnClicked)
        button_refresh = wx.Button(self, wx.ID_ANY, "Refresh")
        button_refresh.Bind(wx.EVT_BUTTON, self.OnClicked)
        button_view = wx.Button(self, wx.ID_ANY, "View on Thunderstore")
        button_view.Bind(wx.EVT_BUTTON, self.OnClicked)
        button_export = wx.Button(self, wx.ID_ANY, "Export")
        button_export.Bind(wx.EVT_BUTTON, self.OnClicked)
        button_import = wx.Button(self, wx.ID_ANY, "Import")
        button_import.Bind(wx.EVT_BUTTON, self.OnClicked)

        sizer_buttons.Add(button_bepis, 11, wx.EXPAND)
        sizer_buttons.Add(button_refresh, 7, wx.EXPAND)
        sizer_buttons.Add(button_view, 15, wx.EXPAND)
        sizer_buttons.Add(button_export, 6, wx.EXPAND)
        sizer_buttons.Add(button_import, 6, wx.EXPAND)

        button_left = wx.Button(self, wx.ID_ANY, "<", size=(50,30))
        button_left.Bind(wx.EVT_BUTTON, self.OnClicked)

        button_right = wx.Button(self, wx.ID_ANY, ">", size=(50,30))
        button_right.Bind(wx.EVT_BUTTON, self.OnClicked)

        listA.Bind(wx.EVT_LISTBOX, self.onSingleSelect)
        listB.Bind(wx.EVT_LISTBOX, self.onSingleSelect)

        listA.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleCLick)
        listB.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleCLick)

        sizer_2.Add(button_right, 0, wx.CENTER)
        sizer_2.Add(button_left, 0, wx.CENTER)

        self.leftlist = listA
        self.rightlist = listB
        self.SetSizer(sizer_0)
        self.Layout()
        self.Show()

    def OnDoubleCLick(self, event):
        print("Doubleclick!")
        print(event)
        event.Skip()

    def OnClicked(self, event):
        btn = event.GetEventObject().GetLabel()

        if btn == ">":
            msg = wx.MessageDialog(self,"JKHasd.", "About", wx.OK | wx.ICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()

    def onSingleSelect(self, event):
        """
        Get the selection of a single cell by clicking or
        moving the selection with the arrow keys
        """
        object = event.GetEventObject()

        if object == self.leftlist:
            self.rightlist.SetSelection(-1)
        elif object == self.rightlist:
            self.leftlist.SetSelection(-1)
        print("Singleclick!")
        print(event)
        event.Skip()


if __name__ == '__main__':

    app = wx.App(0)
    frame = GridFrame(None)
    app.MainLoop()
