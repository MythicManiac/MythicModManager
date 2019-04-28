import wx

from ..system.manager import ModManager, ModManagerConfiguration
from ..utils.log import log_exception

from .generated import MainFrame


class ObjectList:
    def __init__(self, element, columns, column_labels=None):
        self.element = element
        self.columns = columns
        if column_labels:
            self.column_labels = column_labels
        else:
            self.column_labels = [x.capitalize().replace("_", " ") for x in columns]

        self.element.ClearAll()
        for index, label in enumerate(self.column_labels):
            self.element.InsertColumn(index, label)
        self.resize_columns()
        self.element.Bind(wx.EVT_SIZE, lambda event: self.resize_columns())

    def update(self, new_objects):
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
            columns=(
                "name",
                "owner",
                "description",
                "latest_version",
                "total_downloads",
            ),
        )
        self.installed_mod_list = ObjectList(
            element=self.main_frame.installed_mods_list,
            columns=("name", "namespace", "description", "version"),
        )
        self.downloaded_mod_list = ObjectList(
            element=self.main_frame.downloaded_mods_list,
            columns=("name", "namespace", "description", "version"),
        )
        self.configuration = ModManagerConfiguration(
            thunderstore_url="https://thunderstore.io/",
            mod_cache_path="mod-cache/",
            mod_install_path="risk-of-rain-2/mods/",
            risk_of_rain_path="risk-of-rain-2/",
            log_path="logs/",
        )
        self.manager = ModManager(self.configuration)
        self.bind_events()

    def bind_events(self):
        self.main_frame.mod_list_refresh_button.Bind(
            wx.EVT_BUTTON, self.refresh_remote_mod_list
        )

    def refresh_remote_mod_list(self, event):
        try:
            self.manager.api.update_packages()
            self.remote_mod_list.update(self.manager.api.packages.values())
        except Exception as e:
            log_exception(self.configuration.log_path, e)
            wx.MessageBox(
                "Failed to pull remote package data. Server could be offline.",
                "Error",
                wx.OK | wx.ICON_ERROR,
            )

    def refresh_manager_mod_lists(self):
        self.installed_mod_list.update(self.manager.installed_packages)
        self.downloaded_mod_list.update(self.manager.cached_packages)

    def launch(self):
        self.main_frame.Show()
        self.refresh_manager_mod_lists()
        self.app.MainLoop()
