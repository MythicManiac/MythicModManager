import wx
import wx.grid


class TabOne(wx.Panel):
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
        wx.Panel.__init__(self, parent)

        ####################################################################
        # Instantiate element winddows

        self.i_listA = wx.ListBox(choices=[], name="listA", parent=self, style=0)
        self.i_listA.Bind(wx.EVT_LISTBOX, self.on_single_select)
        self.i_listA.Bind(wx.EVT_LISTBOX_DCLICK, self.on_double_click)

        self.i_listB = wx.ListBox(choices=[], name="listB", parent=self, style=0)
        self.i_listB.Bind(wx.EVT_LISTBOX, self.on_single_select)
        self.i_listB.Bind(wx.EVT_LISTBOX_DCLICK, self.on_double_click)

        self.unknown_bmp = wx.Bitmap(
            wx.Image("resources/icon-unknown.png").Scale(180, 180),
            wx.IMAGE_QUALITY_HIGH,
        )
        self.i_portrait = wx.StaticBitmap(self, bitmap=self.unknown_bmp)
        self.i_infoscreen = wx.TextCtrl(self, value="Mod info")

        self.i_refresh = wx.Button(self, wx.ID_ANY, "Refresh")
        self.i_refresh.Bind(wx.EVT_BUTTON, self.on_click)
        self.i_bepis = wx.Button(self, wx.ID_ANY, "Update Bepis")
        self.i_bepis.Bind(wx.EVT_BUTTON, self.on_click)
        self.i_parse = wx.Button(self, wx.ID_ANY, "Parse Download")
        self.i_parse.Bind(wx.EVT_BUTTON, self.on_click)
        self.i_export = wx.Button(self, wx.ID_ANY, "Export")
        self.i_export.Bind(wx.EVT_BUTTON, self.on_click)
        self.i_import = wx.Button(self, wx.ID_ANY, "Import")
        self.i_import.Bind(wx.EVT_BUTTON, self.on_click)

        self.i_left = wx.Button(self, wx.ID_ANY, "<", size=(50, 30))
        self.i_left.Bind(wx.EVT_BUTTON, self.on_click)

        self.i_right = wx.Button(self, wx.ID_ANY, ">", size=(50, 30))
        self.i_right.Bind(wx.EVT_BUTTON, self.on_click)

        self.i_update = wx.Button(self, wx.ID_ANY, "Update package")
        self.i_update.Bind(wx.EVT_BUTTON, self.on_click)
        self.i_view = wx.Button(self, wx.ID_ANY, "View on Thunderstore")
        self.i_view.Bind(wx.EVT_BUTTON, self.on_click)

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

    def on_double_click(self, event):
        print("Doubleclick!")
        print(event)
        event.Skip()

    def on_click(self, event):
        btn = event.GetEventObject().GetLabel()

        if btn == ">":
            msg = wx.MessageDialog(self, ">", "Button", wx.OK | wx.ICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()

        elif btn == "<":
            msg = wx.MessageDialog(self, "<", "Button", wx.OK | wx.ICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()

        elif btn == "Refresh":
            msg = wx.MessageDialog(
                self, "Refresh", "Button", wx.OK | wx.ICON_INFORMATION
            )
            msg.ShowModal()
            msg.Destroy()

        elif btn == "Update Bepis":
            msg = wx.MessageDialog(
                self, "Update Bepis", "Button", wx.OK | wx.ICON_INFORMATION
            )
            msg.ShowModal()
            msg.Destroy()

    def on_single_select(self, event):
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


class TabTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # self.i_downloadlist = wx.ListBox(choices=["Mod A", "b", "c", "d"], name='listA',
        #                           parent=self, style=0)
        self.grid = wx.grid.Grid(self, -1)
        self.grid.CreateGrid(100, 4)
        self.grid.EnableEditing(False)

        self.grid.SetColLabelValue(0, "Name")
        self.grid.SetColLabelValue(1, "Description")
        self.grid.SetColLabelValue(2, "Version")
        self.grid.SetColLabelValue(3, "Local")

        sizer = wx.BoxSizer()
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.grid.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetSizer(sizer)

    def OnSize(self, event):
        width, height = self.GetClientSize()
        colwidth = (width - 100) / 20
        self.grid.SetColSize(0, colwidth * 4)
        self.grid.SetColSize(1, colwidth * 10)
        self.grid.SetColSize(2, colwidth * 3)
        self.grid.SetColSize(3, colwidth * 3)


class GridFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE)
        self.SetSize(wx.DLG_UNIT(self, wx.Size(300, 260)))
        p = wx.Panel(self)
        nb = wx.Notebook(p)
        tab1 = TabOne(nb)
        tab2 = TabTwo(nb)
        nb.AddPage(tab1, "Manage")
        nb.AddPage(tab2, "Download")
        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
        self.Layout()
        self.Show()


def main():
    app = wx.App(0)
    GridFrame(None)
    app.MainLoop()


if __name__ == "__main__":
    main()
