import wx
import wx.grid
import sys
from pathlib import Path
import inspect
import threading


class GridFrame(wx.Frame):
    def __init__(self, parent):

        ####################################################################
        #                     ###                                          #
        #                     ###                                          #
        #                     ###            infoscreen                    #
        #      portrait       ###                                          #
        #                     ###                                          #
        #                     ##############################################
        #                     ###      update      ###           view      #
        ####################################################################
        # refresh   #    bepis     #   parse   #    export    #    import  #
        ####################################################################
        #                             ########                             #
        #                             ########                             #
        #                             ########                             #
        #                             ##right#                             #
        #           listA             ##left##           listB             #
        #                             ########                             #
        #                             ########                             #
        #                             ########                             #
        #                             ########                             #
        ####################################################################

        ####################################################################
        # Instantiate frame
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE)
        self.SetSize(wx.DLG_UNIT(self, wx.Size(300, 260)))

        ####################################################################
        # Instantiate element winddows

        self.i_listA = wx.ListBox(choices=[], name='listA',
                                  parent=self, style=0)
        self.i_listA.Bind(wx.EVT_LISTBOX, self.onSingleSelect)
        self.i_listA.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleCLick)

        self.i_listB = wx.ListBox(choices=[], name='listB',
                                  parent=self, style=0)
        self.i_listB.Bind(wx.EVT_LISTBOX, self.onSingleSelect)
        self.i_listB.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleCLick)

        self.unknown_bmp = wx.Bitmap(wx.Image("unknown.png").Scale(180, 180),
                                     wx.IMAGE_QUALITY_HIGH)
        self.i_portrait = wx.StaticBitmap(self, bitmap=self.unknown_bmp)
        self.i_infoscreen = wx.TextCtrl(self, value="Mod info")

        self.i_refresh = wx.Button(self, wx.ID_ANY, "Refresh")
        self.i_refresh.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.i_bepis = wx.Button(self, wx.ID_ANY, "Update Bepis")
        self.i_bepis.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.i_parse = wx.Button(self, wx.ID_ANY, "Parse Download")
        self.i_parse.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.i_export = wx.Button(self, wx.ID_ANY, "Export")
        self.i_export.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.i_import = wx.Button(self, wx.ID_ANY, "Import")
        self.i_import.Bind(wx.EVT_BUTTON, self.OnClicked)

        self.i_left = wx.Button(self, wx.ID_ANY, "<", size=(50, 30))
        self.i_left.Bind(wx.EVT_BUTTON, self.OnClicked)

        self.i_right = wx.Button(self, wx.ID_ANY, ">", size=(50, 30))
        self.i_right.Bind(wx.EVT_BUTTON, self.OnClicked)

        self.i_update = wx.Button(self, wx.ID_ANY, "Update package")
        self.i_update.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.i_view = wx.Button(self, wx.ID_ANY, "View on Thunderstore")
        self.i_view.Bind(wx.EVT_BUTTON, self.OnClicked)

        ####################################################################
        # Instantiate sizers

        is_A = wx.BoxSizer(wx.VERTICAL)  # Main vertical sizer
        is_B = wx.BoxSizer(wx.HORIZONTAL)  # Top horizontal sizer
        is_C = wx.BoxSizer(wx.HORIZONTAL)  # Button row horiz. sizer
        is_D = wx.BoxSizer(wx.HORIZONTAL)  # Bottom horizontal sizer
        is_E = wx.BoxSizer(wx.VERTICAL)  # Buttons between lists vert. sizer
        is_F = wx.BoxSizer(wx.VERTICAL)  # Buttons under infoscreen v sizer
        is_G = wx.BoxSizer(wx.HORIZONTAL)  # Buttons under infoscreen h sizer

        is_A.Add(is_B, 1, wx.EXPAND)
        is_A.AddSpacer(4)
        is_A.Add(is_C, 0, wx.EXPAND)
        is_A.Add(is_D, 3, wx.EXPAND)

        is_B.Add(self.i_portrait, 1, wx.CENTER)
        is_B.Add(is_F, 2, wx.EXPAND)

        is_C.Add(self.i_refresh, 7, wx.EXPAND)
        is_C.Add(self.i_bepis, 11, wx.EXPAND)
        is_C.Add(self.i_parse, 15, wx.EXPAND)
        is_C.Add(self.i_export, 6, wx.EXPAND)
        is_C.Add(self.i_import, 6, wx.EXPAND)

        is_D.Add(self.i_listA, 1, wx.EXPAND)
        is_D.Add(is_E, 0, wx.CENTER)
        is_D.Add(self.i_listB, 1, wx.EXPAND)

        is_E.Add(self.i_right, 0, wx.CENTER)
        is_E.Add(self.i_left, 0, wx.CENTER)

        is_F.Add(self.i_infoscreen, 2, wx.EXPAND)
        is_F.Add(is_G, 0, wx.EXPAND)

        is_G.Add(self.i_update, 14, wx.EXPAND)
        is_G.Add(self.i_view, 20, wx.EXPAND)
        ####################################################################
        # Show

        self.SetSizer(is_A)
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

        if object == self.i_listB:
            self.i_listA.SetSelection(-1)
        elif object == self.i_listA:
            self.i_listB.SetSelection(-1)
        print("Singleclick!")
        print(event)
        event.Skip()


if __name__ == '__main__':

    app = wx.App(0)
    frame = GridFrame(None)
    app.MainLoop()
