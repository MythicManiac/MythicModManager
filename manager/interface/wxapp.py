import wx
import wx.grid
import sys
from pathlib import Path
import inspect
import threading


class GridFrame(wx.Frame):
    def __init__(self, parent):
        # wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        # self.SetSize(wx.DLG_UNIT(self, wx.Size(325, 200)))
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE)

        self.itemset = set([])
        self.cellection = []

        listA = wx.ListBox(choices=[], name='LeftList', parent=self, style=0)

        listB = wx.ListBox(choices=[], name='RightList', parent=self, style=0)

        sizer_0 = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        sizer_bar = wx.BoxSizer(wx.HORIZONTAL)

        sizer_0.Add(sizer_1, 1, wx.EXPAND)
        sizer_0.Add(sizer_bar, 1)

        button_lefta = wx.Button(self, wx.ID_ANY, "<", size=(50,30))

        sizer_bar.Add(button_lefta)

        sizer_1.Add(listA, 1, wx.EXPAND)
        sizer_1.Add(sizer_2, 0)
        sizer_1.Add(listB, 1, wx.EXPAND)

        button_left = wx.Button(self, wx.ID_ANY, "<", size=(50,30))
        button_right = wx.Button(self, wx.ID_ANY, ">", size=(50,30))

        button_left.Bind(wx.EVT_BUTTON, self.OnClicked)
        button_right.Bind(wx.EVT_BUTTON, self.OnClicked)

        listA.Bind(wx.EVT_LISTBOX, self.onSingleSelect)
        listB.Bind(wx.EVT_LISTBOX, self.onSingleSelect)

        listA.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleCLick)
        listB.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleCLick)

        sizer_2.Add(button_left, 0, wx.CENTER)
        sizer_2.Add(button_right, 0, wx.CENTER)

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
