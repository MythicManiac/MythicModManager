import os
import requests_async
import shutil
import json

from pathlib import Path
from io import BytesIO

from zipfile import ZipFile

from ..api.types import PackageReference
from ..api.thunderstore import ThunderstoreAPI
from ..utils.log import log_exception

from .jobs import DownloadAndInstallPackage


class ModManagerConfiguration:
    def __init__(
        self, risk_of_rain_path, mod_install_path=None, thunderstore_url="https://thunderstore.io/", mod_cache_path="mod-cache/"
    ):
        self.thunderstore_url = thunderstore_url
        self.mod_cache_path = Path(mod_cache_path).resolve()
        self.mod_install_path = Path(mod_install_path if mod_install_path else risk_of_rain_path / "BepInEx" / "plugins").resolve()
        self.risk_of_rain_path = Path(risk_of_rain_path).resolve()


class PackageMetadata:
    def __init__(
        self,
        namespace,
        name,
        version,
        description,
        downloads,
        dependencies,
        icon_url=None,
        icon_data=None,
        thunderstore_url=None,
    ):
        self.namespace = namespace
        self.name = name
        self.version = version
        self.description = description
        self.downloads = downloads
        self.icon_url = icon_url
        self.icon_data = icon_data
        self.dependencies = dependencies
        self.thunderstore_url = thunderstore_url

    @property
    def package_reference(self):
        return PackageReference(
            namespace=self.namespace, name=self.name, version=self.version
        )

    @classmethod
    def from_package(cls, package, thunderstore_url):
        if hasattr(package, "versions"):
            package = package.versions.latest
        return cls(
            namespace=package.package_reference.namespace,
            name=package.package_reference.name,
            version=package.package_reference.version_str,
            description=package.description,
            icon_url=package.icon,
            downloads=package.downloads,
            dependencies=package.dependencies,
            thunderstore_url=thunderstore_url,
        )

    @classmethod
    def empty(cls):
        return cls(
            namespace="None",
            name="No package selected",
            version="0.0.0",
            description="",
            icon_url="",  # TODO: Add unknown icon,
            downloads="",
            dependencies=[],
        )

    async def get_icon_bytes(self):
        if self.icon_data:
            return self.icon_data

        if not self.icon_url:
            return None

        try:
            # TODO: Add caching
            response = await requests_async.get(self.icon_url)
            return BytesIO(response.content)
        except Exception as e:
            log_exception(e)
            return None

    def __eq__(self, other):
        if isinstance(other, PackageMetadata):
            return self.package_reference == other.package_reference
        return super().__eq__(other)


class ModManager:
    def __init__(self, configuration, job_manager):
        self.api = ThunderstoreAPI(configuration.thunderstore_url)
        self.mod_cache_path = configuration.mod_cache_path
        self.mod_install_path = configuration.mod_install_path
        self.risk_of_rain_path = configuration.risk_of_rain_path
        self.job_manager = job_manager
        self.on_uninstall_callbacks = []
        self.on_install_callbacks = []
        self.on_delete_callbacks = []
        self.on_download_callbacks = []

    def bind_on_uninstall(self, callback):
        self.on_uninstall_callbacks.append(callback)

    def bind_on_install(self, callback):
        self.on_install_callbacks.append(callback)

    def bind_on_delete(self, callback):
        self.on_delete_callbacks.append(callback)

    def bind_on_download(self, callback):
        self.on_download_callbacks.append(callback)

    @property
    def installed_packages(self):
        result = []
        for entry in self.mod_install_path.glob("*"):
            if entry.is_dir() and (entry / "manifest.json").exists():
                try:
                    result.append(PackageReference.parse(entry.name))
                except Exception:
                    pass
        return result

    @property
    def cached_packages(self):
        return [
            PackageReference.parse(x.stem) for x in self.mod_cache_path.glob("*.zip")
        ]

    def get_installed_package_metadata(self, reference):
        managed_path = self.get_managed_package_path(reference)
        manifest_path = managed_path / "manifest.json"
        icon_path = managed_path / "icon.png"
        with open(manifest_path, "rb") as f:
            data = json.loads(f.read().decode("utf-8-sig"))
        with open(icon_path, "rb") as f:
            icon_data = BytesIO(f.read())
        return PackageMetadata(
            namespace=reference.namespace,
            name=reference.name,
            version=reference.version_str,
            description=data.get("description", ""),
            downloads="Unknown",
            icon_data=icon_data,
            dependencies=[
                PackageReference.parse(x) for x in data.get("dependencies", [])
            ],
        )

    def get_cached_package_metadata(self, reference):
        zip_path = self.get_package_cache_path(reference)

        try:
            with ZipFile(zip_path) as unzip:
                data = json.loads(unzip.read("manifest.json").decode("utf-8-sig"))
                icon_data = BytesIO(unzip.read("icon.png"))
        except Exception:
            return PackageMetadata(
                namespace=reference.namespace,
                name=reference.name,
                version=reference.version_str,
                description="",
                downloads="Unknown",
                dependencies=[],
            )

        return PackageMetadata(
            namespace=reference.namespace,
            name=reference.name,
            version=reference.version_str,
            description=data.get("description", ""),
            downloads="Unknown",
            icon_data=icon_data,
            dependencies=[
                PackageReference.parse(x) for x in data.get("dependencies", [])
            ],
        )

    async def migrate_mmm_prefixes(self):
        for entry in self.mod_install_path.glob("mmm-*"):
            try:
                reference = PackageReference.parse(entry.name[4:])
                await self.job_manager.put(DownloadAndInstallPackage(self, reference))
            except Exception as e:
                log_exception(e)
            shutil.rmtree(entry)

    async def validate_cache(self):
        for package in self.cached_packages:
            await self.validate_zip_or_delete(package)

    async def validate_zip_or_delete(self, reference):
        zip_path = self.get_package_cache_path(reference)

        try:
            with ZipFile(zip_path) as unzip:
                if unzip.testzip():
                    raise RuntimeError("Invalid zip")
        except Exception:
            await self.delete_package(reference)

    def get_newest_from(self, package, references):
        # TODO: Refactor and use a package container
        newest = None
        for version in references:
            if not version.is_same_package(package):
                continue
            if newest is None or version > newest:
                newest = version
        return newest

    def get_newest_cached(self, reference):
        return self.get_newest_from(reference, self.cached_packages)

    def get_newest_installed(self, reference):
        return self.get_newest_from(reference, self.installed_packages)

    def resolve_package_metadata(self, reference):
        """
        :param package: The package to resolve metadata for
        :type package: PackageReference or Package or str
        """
        if hasattr(reference, "package_reference"):
            reference = reference.package_reference
        if not isinstance(reference, PackageReference):
            reference = PackageReference.parse(reference)
        if reference in self.api.packages:
            url = self.api.packages[reference.without_version].package_url
            return PackageMetadata.from_package(self.api.packages[reference], url)

        if not reference.version:
            version = self.get_newest_installed(reference)
            if version:
                return self.get_installed_package_metadata(version)

        if reference in self.installed_packages:
            return self.get_installed_package_metadata(reference)

        if not reference.version:
            version = self.get_newest_cached(reference)
            if version:
                return self.get_cached_package_metadata(version)

        if reference in self.cached_packages:
            return self.get_cached_package_metadata(reference)
        return PackageMetadata.empty()

    def get_package_cache_path(self, reference):
        return self.mod_cache_path / f"{reference}.zip"

    def get_managed_package_path(self, reference):
        return self.mod_install_path / f"{reference}"

    async def download_package(self, reference, progress):
        download_url = self.api.get_package_download_url(reference)
        print(f"Downloading {reference}... ", end="")

        target_dir = self.get_package_cache_path(reference)
        if not self.mod_cache_path.exists():
            os.makedirs(self.mod_cache_path)

        response = await requests_async.get(download_url, stream=True)
        response.raise_for_status()
        try:
            total_length = float(response.headers["Content-length"])
        except Exception:
            total_length = None
        current_length = 0
        with open(target_dir, "wb") as f:
            async for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                current_length += len(chunk)
                if total_length is not None:
                    progress.SetValue(current_length / total_length * 1000)

        await self.validate_zip_or_delete(reference)

        print("Done!")
        for callback in self.on_download_callbacks:
            callback()

    async def delete_package(self, reference):
        if reference.version:
            print(f"Deleting {reference}... ", end="")
            package_path = self.get_package_cache_path(reference)
            if package_path.exists():
                os.remove(package_path)
            print("Done!")
            for callback in self.on_delete_callbacks:
                callback()
        else:
            for package in self.cached_packages:
                if package.is_same_package(reference):
                    await self.delete_package(package)

    def install_extract_package(self, reference):
        pass  # TODO: Implement

    def install_managed_package(self, reference):
        print(f"Installing {reference}... ", end="")
        package_path = self.get_package_cache_path(reference)
        target_dir = self.get_managed_package_path(reference)

        if not target_dir.is_dir():
            os.makedirs(target_dir)

        if not package_path.exists():
            print("Could not install, package was not found")
            return

        with ZipFile(package_path) as unzip:
            if unzip.testzip():
                # TODO: Handle better
                raise RuntimeError("Corrupted zip file")
            unzip.extractall(target_dir)
        print("Done!")

    async def install_package(self, reference, progress):
        if not reference.version:
            print("Skipping install, no version specified")
            return

        installed_packages = self.installed_packages
        if reference in installed_packages:
            print(f"Skipping install, {reference} already installed")
            return

        for installed_package in installed_packages:
            if installed_package.is_same_package(reference):
                if installed_package.version > reference.version:
                    print(
                        f"Skipping install of {reference}, {installed_package} already present"
                    )
                    return
                else:
                    await self.uninstall_package(installed_package)

        # TODO: Add checking for managed vs. extract package install
        self.install_managed_package(reference)

        # TODO: Resolve dependencies in a safer way
        meta = self.resolve_package_metadata(reference)
        for dependency in meta.dependencies:
            await self.download_and_install_package(dependency, progress)
        for callback in self.on_install_callbacks:
            callback()

    async def uninstall_package(self, reference):
        # TODO: Also uninstall dependants
        if reference.version:
            print(f"Uninstalling {reference}... ", end="")
            package_path = self.get_managed_package_path(reference)
            if package_path.exists():
                shutil.rmtree(package_path)
            print("Done!")
            for callback in self.on_uninstall_callbacks:
                callback()
            return True
        else:
            for package in self.installed_packages:
                if package.is_same_package(reference):
                    if not await self.uninstall_package(package):
                        print(f"Unable to uninstall {reference}")

    async def download_and_install_package(self, reference, progress):

        if not reference.version:
            if reference in self.api.packages:
                reference = self.api.packages[
                    reference
                ].versions.latest.package_reference
            else:
                print(
                    f"Could not find version information for {reference}, skipping install"
                )
                print(f"Try refreshing the package list first")

        if reference not in self.cached_packages:
            await self.download_package(reference, progress)

        await self.install_package(reference, progress)
