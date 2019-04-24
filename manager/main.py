import os
import glob
import requests
import PySimpleGUI as sg
import webbrowser
import shutil
import json

from zipfile import ZipFile


from distutils.version import StrictVersion


class ThunderstoreAPI():
    API_URL = "https://thunderstore.io/api/v1/package/"

    def __init__(self):
        self.update_package_index()

    def update_package_index(self):
        self.packages, self.bepinex = self.build_package_index()

    def build_package_index(self):
        all_packages = sorted(requests.get(self.API_URL).json(), key=lambda i: i["full_name"].lower())
        packages_by_full_name = {
            entry["full_name"]: entry
            for entry in all_packages
        }
        bepinex = packages_by_full_name["bbepis-BepInExPack"]
        bepinex_packages = {
            entry["full_name"]: entry
            for entry in all_packages
            if self.is_bepis_package(entry)
        }
        return (bepinex_packages, bepinex)

    def get_latest_version(self, package):
        ordered = sorted(
            package["versions"],
            key=lambda version: StrictVersion(version["version_number"])
        )
        return ordered[-1]

    def is_bepis_package(self, entry):
        latest = self.get_latest_version(entry)
        for dependency in latest["dependencies"]:
            if dependency.startswith("bbepis-BepInExPack"):
                return True
        return False

    def get_package_names(self):
        return tuple(self.packages.keys())


class ModManager():

    def __init__(self, api, mod_cache_path, risk_of_rain_path):
        self.mod_cache_path = os.path.abspath(mod_cache_path)
        self.risk_of_rain_path = os.path.abspath(risk_of_rain_path)
        self.mod_install_path = os.path.join(
            self.risk_of_rain_path,
            "BepInex",
            "plugins",
        )
        self.api = api

    def verify_bepinex(self):
        doorstop_config = os.path.join(self.risk_of_rain_path, "doorstop_config.ini")
        if os.path.exists(doorstop_config):
            return True
        else:
            return False

    def download_mod(self, owner, name, version):
        full_name = self.get_version_full_name(owner, name, version)
        download_url = f"https://thunderstore.io/package/download/{owner}/{name}/{version}/"
        target_name = f"{full_name}.zip"
        print(f"Downloading {full_name}")

        target_path = os.path.join(self.mod_cache_path, target_name)
        target_dir = os.path.dirname(target_path)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(target_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

    def install_bepinmod_package(self, mod_full_name):
        package_path = os.path.join(self.mod_cache_path, f"{mod_full_name}.zip")
        assert os.path.exists(package_path)
        print(f"Installing {mod_full_name}")

        target_dir = os.path.join(self.mod_install_path, f"mmm-{mod_full_name}")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with ZipFile(package_path) as unzip:
            if unzip.testzip():
                raise RuntimeError("Corrupted zip file")
                return
            for file in unzip.namelist():
                if file.endswith(".mm.dll"):
                    continue
                if file.endswith(".dll"):
                    unzip.extract(file, target_dir)

    def get_package_full_name(self, owner, name):
        return f"{owner}-{name}"

    def get_version_full_name(self, owner, name, version):
        return f"{self.get_package_full_name(owner, name)}-{version}"

    def get_downloaded_packages(self):
        glob_path = os.path.join(self.mod_cache_path + f"{os.sep}*.zip")
        return [
            os.path.splitext(os.path.basename(entry))[:-1][0]
            for entry in glob.glob(glob_path)
        ]

    def get_installed_packages(self):
        glob_path = os.path.join(self.mod_install_path + f"{os.sep}mmm-*")
        return [
            (os.path.basename(entry)[4:-6], os.path.basename(entry)[-5:])
            for entry in glob.glob(glob_path)
        ]

    def export_json(self):
        installed_packages = self.get_installed_packages()
        installed_full_versions = [
            f"{e[0]}-{e[1]}" for e in installed_packages
        ]
        return json.dumps(installed_full_versions)

    def uninstall_package(self, name, version=None):
        if version:
            print(f"Uninstalling {name}-{version}")
            package_path = os.path.join(self.mod_install_path, f"mmm-{name}-{version}")
            shutil.rmtree(package_path)
        else:
            installed_packages = self.get_installed_packages()
            for installed_package in installed_packages:
                if installed_package[0] == name:
                    self.uninstall_package(*installed_package)

    def install_bepinex(self, mod_full_name):
        package_path = os.path.join(self.mod_cache_path, f"{mod_full_name}.zip")
        assert os.path.exists(package_path)

        target_dir = self.risk_of_rain_path
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with ZipFile(package_path) as unzip:
            if unzip.testzip():
                raise RuntimeError("Corrupted zip file")
                return

            prefix = "BepInExPack/"
            for entry in unzip.namelist():
                if not entry.startswith(prefix):
                    continue

                filename = os.path.basename(entry)
                if not filename:
                    continue

                file_target = os.path.join(target_dir, entry[len(prefix):])
                file_target_dir = os.path.dirname(file_target)

                if not os.path.exists(file_target_dir):
                    os.makedirs(file_target_dir)

                source = unzip.open(entry)
                target = open(file_target, "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

    def update_bepinex(self):
        bepinex_package = self.api.bepinex
        latest = self.api.get_latest_version(bepinex_package)

        owner = bepinex_package["owner"]
        name = bepinex_package["name"]
        version = latest["version_number"]
        self.download_mod(owner, name, version)
        self.install_bepinex(self.get_version_full_name(owner, name, version))

    def split_full_version_name(self, full):
        version = full[-5:]
        full = full[:-6]
        name = full.split("-")[-1]
        owner = "-".join(full.split("-")[:-1])
        return owner, name, version

    def download_and_install(self, owner, name, version):
        already_downloaded = self.get_downloaded_packages()
        version_full_name = self.get_version_full_name(owner, name, version)
        package_full_name = self.get_package_full_name(owner, name)

        if version_full_name not in already_downloaded:
            self.download_mod(owner, name, version)

        installed_packages = self.get_installed_packages()
        for installed_package, installed_version in installed_packages:
            if installed_package == package_full_name:
                if installed_version == version:
                    return
                else:
                    self.uninstall_package(installed_package, installed_version)

        self.install_bepinmod_package(version_full_name)


class Application():

    def __init__(self):
        self.api = ThunderstoreAPI()
        config = {
            "risk_of_rain_path": "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Risk of Rain 2"
        }
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config.update(json.load(f))
        self.mod_manager = ModManager(
            api=self.api,
            mod_cache_path="mod-cache/",
            risk_of_rain_path=config["risk_of_rain_path"],
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
        self.selection_description = sg.Multiline(f"", font=("Helvetica", 10), size=(60, 5))
        self.selection_author = sg.Text(f"", font=("Helvetica", 12), size=(26, 1))
        self.selection_version = sg.Text(f"", font=("Helvetica", 12), size=(26, 1))
        self.slection_total_downloads = sg.Text(f"", font=("Helvetica", 12), size=(26, 1))
        self.selection_url = None

        self.available_packages_list = sg.Listbox(
            values=self.api.get_package_names(),
            size=(38, 16),
            select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        )
        self.installed_packages_list = sg.Listbox(
            values=[],
            size=(38, 16),
            select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
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
            visible=True
        )

        self.layout = [
            [
                sg.Text(
                    (
                        "Find the source from https://github.com/MythicManiac/MythicModManager " +
                        "and please make a better tool than this abomination"
                    ),
                    font=("Helvetica", 14),
                )
            ],
            [
                sg.Button("Update BepInEx"), sg.Button("Refresh list"), sg.Button("Export"), sg.Button("Import"),
            ],
            [
                sg.Column([
                    [sg.Text("Available mods", font=("Helvetica", 14))],
                    [self.available_packages_list],
                    [sg.Button("Install")],
                ]),
                sg.Column([
                    [sg.Text("Installed mods", font=("Helvetica", 14))],
                    [self.installed_packages_list],
                    [sg.Button("Uninstall")],
                ]),
                sg.Column([
                    [self.selection_title],
                    [self.selection_description],
                    [self.selection_author],
                    [self.selection_version],
                    [self.slection_total_downloads],
                    [sg.RealtimeButton("View on Thunderstore")],
                ]),
            ],
            [self.progress_bar],
        ]

        if not os.path.exists(self.mod_manager.risk_of_rain_path):
            self.can_run = False
            sg.Popup((
                "Could not find your risk of rain installation path. " +
                "Please add it in the config.json file"
            ))
        else:
            self.window = (
                sg.Window("Mythic Mod Manager")
                .Layout(self.layout)
                .Finalize()
            )
            self.can_run = True

            if not self.mod_manager.verify_bepinex():
                sg.Popup((
                    "It seems you don't have BepInex installed. " +
                    "Please install it by clicking the 'Update BepInEx' button"
                ))

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
        total_downloads = sum([int(version["downloads"]) for version in entry["versions"]])
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
            self.progress_bar.UpdateBar(float(index) / len(mods_to_install) * 1000, 1000)
        self.progress_bar.UpdateBar(1000, 1000)

    def launch(self):
        while self.can_run:
            event, values = self.window.Read(timeout=100)
            if values is None:
                break
            else:
                self.update(event, values)


def main():
    application = Application()
    application.launch()


if __name__ == "__main__":
    main()
