import requests

from distutils.version import StrictVersion

class ThunderstoreAPI():
    API_URL = "https://thunderstore.io/api/v1/package/"

    def __init__(self):
        self.update_package_index()

    def update_package_index(self):
        self.packages, self.bepinex = self.build_package_index()

    def build_package_index(self):
        all_packages = sorted(requests.get(self.API_URL).json(), key=lambda i: "-".join(reversed(i["full_name"].lower().split("-"))))
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
