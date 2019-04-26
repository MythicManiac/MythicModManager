import json
import webbrowser
import PySimpleGUI as sg

from ..system.manager import ModManager
from ..api.thunderstore import ThunderstoreAPI
from ..utils.install_finder import get_install_path


class Application:
    def __init__(self):
        self.api = ThunderstoreAPI()
        self.mod_manager = ModManager(
            api=self.api,
            mod_cache_path="mod-cache/",
            risk_of_rain_path=get_install_path(),
        )
        self.build_window()
        if self.can_run:
            self.refresh_installed_mods()
        self.last_values = None
        self.last_event = None
        self.last_selection = None
        self.last_selection_latest_version = None

    def build_window(self):
        self.selection_title = sg.Text(f"", font=("Helvetica", 20), size=(30, 1))
        self.selection_description = sg.Multiline(
            f"", font=("Helvetica", 10), size=(60, 5)
        )
        self.selection_author = sg.Text(f"", font=("Helvetica", 12), size=(26, 1))
        self.selection_version = sg.Text(f"", font=("Helvetica", 12), size=(26, 1))
        self.slection_total_downloads = sg.Text(
            f"", font=("Helvetica", 12), size=(26, 1)
        )
        self.selection_url = None

        self.available_packages_list = sg.Listbox(
            values=self.api.get_package_names(),
            size=(38, 16),
            select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        )
        self.installed_packages_list = sg.Listbox(
            values=[], size=(38, 16), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED
        )
        self.progress_bar = sg.ProgressBar(
            max_value=1000,
            orientation="h",
            size=(100, 40),
            auto_size_text=None,
            bar_color=(None, None),
            style=None,
            border_width=None,
            relief=None,
            key="progress",
            pad=None,
            visible=True,
        )

        self.layout = [
            [
                sg.Text(
                    (
                        "Find the source from https://github.com/MythicManiac/MythicModManager "
                        + "and please make a better tool than this abomination"
                    ),
                    font=("Helvetica", 14),
                )
            ],
            [
                sg.Button("Update BepInEx"),
                sg.Button("Refresh list"),
                sg.Button("Export"),
                sg.Button("Import"),
            ],
            [
                sg.Column(
                    [
                        [sg.Text("Available mods", font=("Helvetica", 14))],
                        [self.available_packages_list],
                        [sg.Button("Install")],
                    ]
                ),
                sg.Column(
                    [
                        [sg.Text("Installed mods", font=("Helvetica", 14))],
                        [self.installed_packages_list],
                        [sg.Button("Uninstall")],
                    ]
                ),
                sg.Column(
                    [
                        [self.selection_title],
                        [self.selection_description],
                        [self.selection_author],
                        [self.selection_version],
                        [self.slection_total_downloads],
                        [sg.RealtimeButton("View on Thunderstore")],
                    ]
                ),
            ],
            [self.progress_bar],
        ]

        if not self.mod_manager.risk_of_rain_path.exists():
            self.can_run = False
            sg.Popup(
                (
                    "Could not find your risk of rain installation path. "
                    + "Please add it in the config.json file"
                )
            )
        else:
            self.window = sg.Window("Mythic Mod Manager").Layout(self.layout).Finalize()
            self.can_run = True

            if not self.mod_manager.verify_bepinex():
                sg.Popup(
                    (
                        "It seems you don't have BepInex installed. "
                        + "Please install it by clicking the 'Update BepInEx' button"
                    )
                )

    def refresh_installed_mods(self):
        installed_packages = self.mod_manager.get_installed_packages()
        package_list = [package[0] for package in installed_packages]
        available_package_list = [
            entry for entry in self.api.get_package_names() if entry not in package_list
        ]
        self.installed_packages_list.Update(package_list)
        self.available_packages_list.Update(available_package_list)

    def navigate_to_thunderstore(self):
        if self.selection_url:
            webbrowser.open(self.selection_url)

    def update_selection(self, selection):
        entry = self.api.packages[selection]
        version = self.api.get_latest_version(entry)
        total_downloads = sum(
            [int(version["downloads"]) for version in entry["versions"]]
        )
        self.last_selection = entry
        self.last_selection_latest_version = version
        self.selection_title.Update(version["name"].replace("_", " "))
        self.selection_description.Update(version["description"])
        self.selection_author.Update(f"Author: {entry['owner']}")
        self.selection_version.Update(f"Version: v{version['version_number']}")
        self.slection_total_downloads.Update(f"Total downloads: {total_downloads}")
        self.selection_url = entry["package_url"]

    def install_mod(self, mod_name):
        mod_entry = self.api.packages.get(mod_name, None)
        if mod_entry:
            last_version = self.api.get_latest_version(mod_entry)
            for dependency in last_version["dependencies"]:
                if not dependency.startswith("bbepis-BepInExPack"):
                    self.install_mod(dependency[:-6])

            self.mod_manager.download_and_install(
                owner=mod_entry["owner"],
                name=mod_entry["name"],
                version=last_version["version_number"],
            )

    def full_refresh(self):
        self.api.update_package_index()
        self.refresh_installed_mods()

    def update(self, event, values):
        if not self.last_values:
            self.last_values = values
            return

        last_available_selections = self.last_values[0]
        new_available_selections = values[0]
        available_selection_change = None

        if last_available_selections != new_available_selections:
            for selection in new_available_selections:
                if selection not in last_available_selections:
                    available_selection_change = selection
                    break

        last_installed_selections = self.last_values[1]
        new_installed_selections = values[1]
        isntalled_selection_change = None

        if last_installed_selections != new_installed_selections:
            for selection in new_installed_selections:
                if selection not in last_installed_selections:
                    isntalled_selection_change = selection
                    break

        if available_selection_change:
            self.update_selection(available_selection_change)

        if isntalled_selection_change:
            if selection in self.api.packages:
                self.update_selection(selection)

        thunderstore_event = "View on Thunderstore"
        if event == thunderstore_event and self.last_event != thunderstore_event:
            self.navigate_to_thunderstore()

        install_event = "Install"
        if event == install_event and self.last_event != install_event:
            self.progress_bar.UpdateBar(0, 1000)
            for index, mod_name in enumerate(values[0]):
                self.install_mod(mod_name)
                self.progress_bar.UpdateBar(float(index) / len(values[0]) * 1000, 1000)
            self.progress_bar.UpdateBar(1000, 1000)
            self.refresh_installed_mods()

        uninstall_event = "Uninstall"
        if event == uninstall_event and self.last_event != uninstall_event:
            self.progress_bar.UpdateBar(0, 1000)
            for index, mod_name in enumerate(values[1]):
                self.mod_manager.uninstall_package(mod_name)
                self.progress_bar.UpdateBar(float(index) / len(values[1]) * 1000, 1000)
            self.progress_bar.UpdateBar(1000, 1000)
            self.refresh_installed_mods()

        refresh_event = "Refresh list"
        if event == refresh_event and self.last_event != refresh_event:
            self.progress_bar.UpdateBar(0, 1000)
            self.full_refresh()
            self.progress_bar.UpdateBar(1000, 1000)

        bepinex_install_event = "Update BepInEx"
        if event == bepinex_install_event and self.last_event != bepinex_install_event:
            self.progress_bar.UpdateBar(0, 1000)
            self.mod_manager.update_bepinex()
            self.progress_bar.UpdateBar(1000, 1000)

        export_event = "Export"
        if event == export_event and self.last_event != export_event:
            sg.PopupScrolled(self.mod_manager.export_json())

        import_event = "Import"
        if event == import_event and self.last_event != import_event:
            data = sg.PopupGetText("Import mod configuration")
            self.handle_import(data)
            self.refresh_installed_mods()

        self.last_event = event
        self.last_values = values

    def handle_import(self, data):
        if not data:
            return
        try:
            mods_to_install = json.loads(data)
        except Exception:
            sg.Popup("Invalid mod configuration supplied")
            return

        self.progress_bar.UpdateBar(0, 1000)
        for index, entry in enumerate(mods_to_install):
            mod_info = self.mod_manager.split_full_version_name(entry)
            self.mod_manager.download_and_install(*mod_info)
            self.progress_bar.UpdateBar(
                float(index) / len(mods_to_install) * 1000, 1000
            )
        self.progress_bar.UpdateBar(1000, 1000)

    def launch(self):
        while self.can_run:
            event, values = self.window.Read(timeout=100)
            if values is None:
                break
            else:
                self.update(event, values)
