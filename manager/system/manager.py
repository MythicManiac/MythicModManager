import json
import os
import requests
import shutil

from pathlib import Path

from zipfile import ZipFile


class ModManager:
    def __init__(self, api, mod_cache_path, risk_of_rain_path):
        self.api = api
        self.mod_cache_path = Path(mod_cache_path)
        self.risk_of_rain_path = risk_of_rain_path
        self.mod_install_path = risk_of_rain_path / "BepInex/plugins"

    def verify_bepinex(self):
        return (self.risk_of_rain_path / "doorstop_config.ini").is_file()

    def download_mod(self, owner, name, version):
        full_name = self.get_package_full_name(owner, name, version)
        download_url = (
            f"https://thunderstore.io/package/download/{owner}/{name}/{version}/"
        )
        print(f"Downloading {full_name}")

        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(self.mod_cache_path.resolve() / f"{full_name}.zip", "wb") as f:
                for chunk in (x for x in r.iter_content(chunk_size=8192) if x):
                    f.write(chunk)

    def install_bepinmod_package(self, mod_full_name):
        package_path = self.mod_cache_path / f"{mod_full_name}.zip"
        assert package_path.is_file()
        print(f"Installing {mod_full_name}")

        target_dir = self.mod_install_path / f"mmm-{mod_full_name}"

        with ZipFile(package_path) as unzip:
            if unzip.testzip():
                raise RuntimeError("Corrupted zip file")
                return
            for file in unzip.namelist():
                if file.endswith(".mm.dll"):
                    continue
                if file.endswith(".dll"):
                    unzip.extract(file, target_dir)

    def get_package_full_name(self, owner, name, version=None):
        return f"{owner}-{name}{f'-{version}' if version else ''}"

    def get_downloaded_packages(self):
        return [x.stem for x in self.mod_cache_path.glob("*.zip")]

    def get_installed_packages(self):
        return [
            (x.name[4:-6], x.name[-5:]) for x in self.mod_install_path.glob("mmm-*")
        ]

    def export_json(self):
        installed_packages = self.get_installed_packages()
        installed_full_versions = [f"{e[0]}-{e[1]}" for e in installed_packages]
        return json.dumps(installed_full_versions)

    def uninstall_package(self, name, version=None):
        if version:
            print(f"Uninstalling {name}-{version}")
            package_path = self.mod_install_path / f"mmm-{name}-{version}"
            shutil.rmtree(package_path)
        else:
            installed_packages = self.get_installed_packages()
            for installed_package in installed_packages:
                if installed_package[0] == name:
                    self.uninstall_package(*installed_package)

    def install_bepinex(self, mod_full_name):
        # TODO: re-implement makedirs
        package_path = self.mod_cache_path / f"{mod_full_name}.zip"
        assert package_path.is_file()
        if not self.risk_of_rain_path.exists():
            self.risk_of_rain_path.mkdir(parents=True, exist_ok=True)

        with ZipFile(package_path) as unzip:
            if unzip.testzip():
                raise RuntimeError("Corrupted zip file")
                return

            prefix = "BepInExPack/"
            for entry in unzip.namelist():
                if not entry.startswith(prefix) or not os.path.basename(entry):
                    continue

                file_target = self.risk_of_rain_path / entry[len(prefix) :]
                if not file_target.parent.exists():
                    file_target.parent.mkdir(parents=True, exist_ok=True)

                source = unzip.open(entry)
                target = file_target.open("wb")
                with source, target:
                    shutil.copyfileobj(source, target)

    def update_bepinex(self):
        bepinex_package = self.api.bepinex
        latest = self.api.get_latest_version(bepinex_package)

        owner = bepinex_package.owner
        name = bepinex_package.name
        version = latest.version_number
        self.download_mod(owner, name, version)
        self.install_bepinex(self.get_package_full_name(owner, name, version))

    def split_full_version_name(self, full):
        version = full[-5:]
        full = full[:-6]
        name = full.split("-")[-1]
        owner = "-".join(full.split("-")[:-1])
        return owner, name, version

    def download_and_install(self, owner, name, version):
        already_downloaded = self.get_downloaded_packages()
        version_full_name = self.get_package_full_name(owner, name, version)
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
