import os
import requests
import shutil

from pathlib import Path

from manager.api.types import PackageReference
from manager.api.thunderstore import ThunderstoreAPI

from zipfile import ZipFile


class ModManagerConfiguration:
    def __init__(
        self,
        thunderstore_url,
        mod_cache_path,
        risk_of_rain_path,
        mod_install_path,
        log_path,
    ):
        self.thunderstore_url = thunderstore_url
        self.mod_cache_path = Path(mod_cache_path).resolve()
        self.mod_install_path = Path(mod_install_path).resolve()
        self.risk_of_rain_path = Path(risk_of_rain_path).resolve()
        self.log_path = Path(log_path).resolve()


class ModManager:
    def __init__(self, configuration):
        self.api = ThunderstoreAPI(configuration.thunderstore_url)
        self.mod_cache_path = configuration.mod_cache_path
        self.mod_install_path = configuration.mod_install_path
        self.risk_of_rain_path = configuration.risk_of_rain_path

    @property
    def installed_packages(self):
        return [
            PackageReference.parse(x.name)
            for x in self.mod_install_path.glob("*")
            if x.is_dir() and (x / "manifest.json").exists()
        ]

    @property
    def cached_packages(self):
        return [
            PackageReference.parse(x.stem) for x in self.mod_cache_path.glob("*.zip")
        ]

    def get_package_cache_path(self, reference):
        return self.mod_cache_path / f"{reference}.zip"

    def get_managed_package_path(self, reference):
        return self.mod_install_path / f"{reference}"

    def download_package(self, reference):
        download_url = self.api.get_package_download_url(reference)
        print(f"Downloading {reference}... ", end="")

        target_dir = self.get_package_cache_path(reference)
        if not self.mod_cache_path.exists():
            os.makedirs(self.mod_cache_path)

        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(target_dir, "wb") as f:
                for chunk in (x for x in r.iter_content(chunk_size=8192) if x):
                    f.write(chunk)
        print("Done!")

    def install_extract_package(self, reference):
        pass  # TODO: Implement

    def install_managed_package(self, reference):
        print(f"Installing {reference}... ", end="")
        package_path = self.get_package_cache_path(reference)
        target_dir = self.get_managed_package_path(reference)

        if not target_dir.is_dir():
            os.makedirs(target_dir)

        with ZipFile(package_path) as unzip:
            if unzip.testzip():
                raise RuntimeError("Corrupted zip file")
            unzip.extractall(target_dir)
        print("Done!")

    def install_package(self, reference):
        # TODO: Add checking for managed vs. extract package install
        self.install_managed_package(reference)

    def uninstall_package(self, reference):
        if reference.version:
            print(f"Uninstalling {reference}... ", end="")
            package_path = self.get_managed_package_path(reference)
            shutil.rmtree(package_path)
            print("Done!")
        else:
            for package in self.installed_packages:
                if package.is_same_package(reference):
                    self.uninstall_package(package)

    def download_and_install_package(self, reference, use_cache=True):
        installed_packages = self.installed_packages
        if reference in installed_packages:
            return

        if reference not in self.cached_packages or not use_cache:
            self.download_package(reference)

        for installed_package in self.installed_packages:
            if installed_package.is_same_package(reference):
                self.uninstall_package(installed_package)

        self.install_package(reference)
