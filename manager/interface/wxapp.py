import wx

from ..system.manager import ModManager, ModManagerConfiguration

from .generated import MainFrame


class ObjectList:
    def __init__(self, element, columns, column_labels=None):
        self.element = element
        self.columns = columns
        if column_labels:
            self.column_labels = column_labels
        else:
            self.column_labels = columns

        self.element.ClearAll()
        for index, label in enumerate(self.column_labels):
            self.element.InsertColumn(index, label)
        self.resize_columns()
        self.element.Bind(wx.EVT_SIZE, lambda event: self.resize_columns())

    def OnSize(self, event):
        width, height = self.GetClientSize()
        colwidth = (width - 100) / 20
        self.grid.SetColSize(0, colwidth * 4)
        self.grid.SetColSize(1, colwidth * 10)
        self.grid.SetColSize(2, colwidth * 3)
        self.grid.SetColSize(3, colwidth * 3)

    def refresh_list(self, new_objects):
        self.element.DeleteAllItems()
        for row, entry in enumerate(new_objects):
            self.element.InsertItem(row, getattr(entry, self.columns[0], ""))
            for i in range(1, len(self.columns)):
                item = wx.ListItem()
                item.SetId(row)
                item.SetColumn(i)
                item.SetText(str(getattr(entry, self.columns[i], "")))
                self.element.SetItem(item)

    def resize_columns(self):
        width, height = self.element.GetClientSize()
        column_width = int(float(width) / len(self.column_labels))
        for index in range(len(self.column_labels)):
            self.element.SetColumnWidth(index, column_width)


class TestMod:
    def __init__(self, name, author, description, version, downloads):
        self.name = name
        self.author = author
        self.description = description
        self.version = version
        self.downloads = downloads


class Application:
    def __init__(self):
        self.app = wx.App(0)
        self.main_frame = MainFrame(None)
        self.remote_mod_list = ObjectList(
            element=self.main_frame.mod_list_list,
            columns=("name", "author", "description", "version", "downloads"),
        )
        configuration = ModManagerConfiguration(
            thunderstore_url="https://thunderstore.io/",
            mod_cache_path="mod-cache/",
            mod_install_path="risk-of-rain-2/mods/",
            risk_of_rain_path="risk-of-rain-2/",
        )
        self.manager = ModManager(configuration)

    def launch(self):
        self.main_frame.Show()
        self.remote_mod_list.refresh_list(
            [
                TestMod(
                    name="Test",
                    author="AnotherTest",
                    description="Not a description",
                    version="1.0.3",
                    downloads=5,
                ),
                TestMod(
                    name="SomeMod",
                    author="SomeAuthor",
                    description="This is not a real mod",
                    version="0.0.1",
                    downloads=3289,
                ),
            ]
        )
        self.app.MainLoop()
