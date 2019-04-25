import requests

from .index import PackageIndex


class ThunderstoreAPI:
    API_URL = "https://thunderstore.io/api/v1/package/"

    def __init__(self):
        self.package_index = PackageIndex()

    def update_package_index(self):
        package_data = requests.get(self.API_URL).json()
        self.package_index.update(package_data)
