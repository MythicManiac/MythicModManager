# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.3 on Sun Apr 28 17:10:15 2019
#

import wx
import wx.adv

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((937, 647))
        self.main_content_notebook = wx.Notebook(self, wx.ID_ANY)
        self.manager_tab = wx.Panel(self.main_content_notebook, wx.ID_ANY)
        self.installed_mods_uninstall_button = wx.Button(
            self.manager_tab, wx.ID_ANY, "Uninstall"
        )
        self.installed_mods_update_button = wx.Button(
            self.manager_tab, wx.ID_ANY, "Update installed mods"
        )
        self.installed_mods_export_button = wx.Button(
            self.manager_tab, wx.ID_ANY, "Export"
        )
        self.installed_mods_import_button = wx.Button(
            self.manager_tab, wx.ID_ANY, "Import"
        )
        self.installed_mods_list = wx.ListCtrl(
            self.manager_tab,
            wx.ID_ANY,
            style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES,
        )
        self.downloaded_mods_install_button = wx.Button(
            self.manager_tab, wx.ID_ANY, "Install"
        )
        self.downloaded_mods_delete_button = wx.Button(
            self.manager_tab, wx.ID_ANY, "Delete"
        )
        self.downloaded_mods_group_version_checkbox = wx.CheckBox(
            self.manager_tab, wx.ID_ANY, "Group by version"
        )
        self.downloaded_mods_list = wx.ListCtrl(
            self.manager_tab,
            wx.ID_ANY,
            style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES,
        )
        self.mod_list_tab = wx.Panel(self.main_content_notebook, wx.ID_ANY)
        self.mod_list_refresh_button = wx.Button(
            self.mod_list_tab, wx.ID_ANY, "Refresh"
        )
        self.mod_list_install_button = wx.Button(
            self.mod_list_tab, wx.ID_ANY, "Install Selected"
        )
        self.mod_list_search = wx.SearchCtrl(self.mod_list_tab, wx.ID_ANY, "")
        self.mod_list_list = wx.ListCtrl(
            self.mod_list_tab,
            wx.ID_ANY,
            style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES,
        )
        self.job_queue_tab = wx.Panel(self.main_content_notebook, wx.ID_ANY)
        self.job_queue_list = wx.ListCtrl(
            self.job_queue_tab,
            wx.ID_ANY,
            style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES,
        )
        self.settings_tab = wx.Panel(self.main_content_notebook, wx.ID_ANY)
        self.about_tab = wx.Panel(self.main_content_notebook, wx.ID_ANY)
        self.about_github_link = wx.adv.HyperlinkCtrl(
            self.about_tab,
            wx.ID_ANY,
            "MythicModManager on GitHub",
            "https://github.com/MythicManiac/MythicModManager/",
        )
        self.selection_icon_bitmap = wx.StaticBitmap(
            self,
            wx.ID_ANY,
            wx.Bitmap("resources\\icon-unknown.png", wx.BITMAP_TYPE_ANY),
        )
        self.selection_info_panel = wx.Panel(self, wx.ID_ANY)
        self.selection_title = wx.StaticText(
            self.selection_info_panel,
            wx.ID_ANY,
            "Placeholder Mod Name That Is Very Long And Could Break The UI",
        )
        self.selection_description = wx.StaticText(
            self.selection_info_panel,
            wx.ID_ANY,
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in",
        )
        self.selection_version = wx.StaticText(
            self.selection_info_panel, wx.ID_ANY, "Latest Version: v1.0.3"
        )
        self.selection_download_count = wx.StaticText(
            self.selection_info_panel, wx.ID_ANY, "Total downloads: 68309"
        )
        self.selection_thunderstore_button = wx.Button(self, wx.ID_ANY, "More Details")
        self.launch_game_button = wx.Button(self, wx.ID_ANY, "Launch Game")
        self.progress_bar_big = wx.Gauge(self, wx.ID_ANY, 1000)
        self.progress_bar_small = wx.Gauge(self, wx.ID_ANY, 1000)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("MythicModManager")
        self.installed_mods_list.AppendColumn(
            "Name", format=wx.LIST_FORMAT_LEFT, width=133
        )
        self.installed_mods_list.AppendColumn(
            "Author", format=wx.LIST_FORMAT_LEFT, width=136
        )
        self.installed_mods_list.AppendColumn(
            "Description", format=wx.LIST_FORMAT_LEFT, width=290
        )
        self.installed_mods_list.AppendColumn(
            "Version", format=wx.LIST_FORMAT_LEFT, width=79
        )
        self.downloaded_mods_group_version_checkbox.SetValue(1)
        self.downloaded_mods_list.AppendColumn(
            "Name", format=wx.LIST_FORMAT_LEFT, width=132
        )
        self.downloaded_mods_list.AppendColumn(
            "Author", format=wx.LIST_FORMAT_LEFT, width=138
        )
        self.downloaded_mods_list.AppendColumn(
            "Description", format=wx.LIST_FORMAT_LEFT, width=288
        )
        self.downloaded_mods_list.AppendColumn(
            "Version", format=wx.LIST_FORMAT_LEFT, width=-1
        )
        self.mod_list_search.ShowCancelButton(True)
        self.mod_list_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=115)
        self.mod_list_list.AppendColumn("Author", format=wx.LIST_FORMAT_LEFT, width=102)
        self.mod_list_list.AppendColumn(
            "Description", format=wx.LIST_FORMAT_LEFT, width=194
        )
        self.mod_list_list.AppendColumn("Version", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.mod_list_list.AppendColumn(
            "Downloads", format=wx.LIST_FORMAT_LEFT, width=-1
        )
        self.job_queue_list.AppendColumn(
            "Action", format=wx.LIST_FORMAT_LEFT, width=342
        )
        self.job_queue_list.AppendColumn(
            "Parameter", format=wx.LIST_FORMAT_LEFT, width=315
        )
        self.selection_title.SetFont(
            wx.Font(
                14,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        self.selection_title.Wrap(160)
        self.selection_description.Wrap(240)
        self.selection_version.Wrap(240)
        self.selection_download_count.Wrap(240)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        progress_bars_sizer = wx.BoxSizer(wx.VERTICAL)
        main_content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        selection_info_sizer = wx.BoxSizer(wx.VERTICAL)
        selection_info_content_sizer = wx.BoxSizer(wx.VERTICAL)
        selection_info_buttons_sizer = wx.BoxSizer(wx.VERTICAL)
        selection_info_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        about_sizer = wx.BoxSizer(wx.HORIZONTAL)
        job_queue_sizer = wx.BoxSizer(wx.VERTICAL)
        mod_list_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        manager_sizer = wx.BoxSizer(wx.VERTICAL)
        downloaded_mods_sizer = wx.BoxSizer(wx.VERTICAL)
        downloaded_mods_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        installed_mods_sizer = wx.BoxSizer(wx.VERTICAL)
        installed_mods_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        installed_mods_title = wx.StaticText(
            self.manager_tab, wx.ID_ANY, "Installed mods"
        )
        installed_mods_title.SetFont(
            wx.Font(
                14,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        installed_mods_sizer.Add(installed_mods_title, 0, 0, 0)
        installed_mods_buttons_sizer.Add(
            self.installed_mods_uninstall_button, 1, wx.EXPAND, 0
        )
        installed_mods_buttons_sizer.Add(
            self.installed_mods_update_button, 1, wx.EXPAND, 0
        )
        installed_mods_buttons_sizer.Add(
            self.installed_mods_export_button, 1, wx.EXPAND, 0
        )
        installed_mods_buttons_sizer.Add(
            self.installed_mods_import_button, 1, wx.EXPAND, 0
        )
        installed_mods_sizer.Add(installed_mods_buttons_sizer, 0, wx.EXPAND, 0)
        installed_mods_sizer.Add(self.installed_mods_list, 1, wx.EXPAND, 0)
        manager_sizer.Add(installed_mods_sizer, 1, wx.EXPAND, 0)
        downloaded_mods_title = wx.StaticText(
            self.manager_tab, wx.ID_ANY, "Downloaded mods"
        )
        downloaded_mods_title.SetFont(
            wx.Font(
                14,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        downloaded_mods_sizer.Add(downloaded_mods_title, 0, 0, 0)
        downloaded_mods_buttons_sizer.Add(self.downloaded_mods_install_button, 1, 0, 0)
        downloaded_mods_buttons_sizer.Add(self.downloaded_mods_delete_button, 1, 0, 0)
        downloaded_mods_buttons_sizer.Add(
            self.downloaded_mods_group_version_checkbox, 0, wx.ALIGN_CENTER | wx.ALL, 4
        )
        downloaded_mods_sizer.Add(downloaded_mods_buttons_sizer, 0, wx.EXPAND, 0)
        downloaded_mods_sizer.Add(self.downloaded_mods_list, 1, wx.EXPAND, 0)
        manager_sizer.Add(downloaded_mods_sizer, 1, wx.EXPAND, 0)
        self.manager_tab.SetSizer(manager_sizer)
        sizer_1.Add(self.mod_list_refresh_button, 1, wx.EXPAND, 0)
        sizer_1.Add(self.mod_list_install_button, 1, wx.EXPAND, 0)
        mod_list_sizer.Add(sizer_1, 0, wx.EXPAND, 0)
        mod_list_sizer.Add(self.mod_list_search, 0, wx.EXPAND, 0)
        mod_list_sizer.Add(self.mod_list_list, 1, wx.EXPAND, 0)
        self.mod_list_tab.SetSizer(mod_list_sizer)
        job_queue_sizer.Add(self.job_queue_list, 1, wx.EXPAND, 0)
        self.job_queue_tab.SetSizer(job_queue_sizer)
        about_sizer.Add(self.about_github_link, 0, wx.ALIGN_CENTER, 0)
        self.about_tab.SetSizer(about_sizer)
        self.main_content_notebook.AddPage(self.manager_tab, "Manager")
        self.main_content_notebook.AddPage(self.mod_list_tab, "Mod list")
        self.main_content_notebook.AddPage(self.job_queue_tab, "Job queue")
        self.main_content_notebook.AddPage(self.settings_tab, "Settings")
        self.main_content_notebook.AddPage(self.about_tab, "About")
        main_content_sizer.Add(self.main_content_notebook, 1, wx.EXPAND, 0)
        selection_info_sizer.Add(self.selection_icon_bitmap, 0, wx.EXPAND, 0)
        selection_info_panel_sizer.Add(self.selection_title, 50, 0, 0)
        selection_info_panel_sizer.Add(self.selection_description, 60, 0, 0)
        selection_info_panel_separator = wx.StaticLine(
            self.selection_info_panel, wx.ID_ANY
        )
        selection_info_panel_sizer.Add(selection_info_panel_separator, 1, wx.EXPAND, 0)
        selection_info_panel_sizer.Add(self.selection_version, 10, 0, 0)
        selection_info_panel_sizer.Add(self.selection_download_count, 10, wx.ALL, 0)
        self.selection_info_panel.SetSizer(selection_info_panel_sizer)
        selection_info_content_sizer.Add(self.selection_info_panel, 1, wx.EXPAND, 0)
        selection_info_buttons_sizer.Add(
            self.selection_thunderstore_button, 1, wx.EXPAND, 0
        )
        selection_info_buttons_sizer.Add(self.launch_game_button, 0, wx.EXPAND, 0)
        selection_info_content_sizer.Add(selection_info_buttons_sizer, 0, wx.EXPAND, 0)
        selection_info_sizer.Add(selection_info_content_sizer, 1, wx.EXPAND, 0)
        main_content_sizer.Add(selection_info_sizer, 0, wx.EXPAND, 0)
        root_sizer.Add(main_content_sizer, 95, wx.EXPAND, 0)
        progress_bars_sizer.Add(self.progress_bar_big, 1, wx.EXPAND, 0)
        progress_bars_sizer.Add(self.progress_bar_small, 0, wx.EXPAND, 0)
        root_sizer.Add(progress_bars_sizer, 8, wx.EXPAND, 0)
        self.SetSizer(root_sizer)
        self.Layout()
        # end wxGlade


# end of class MainFrame
