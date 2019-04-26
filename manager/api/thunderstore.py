import requests

from .packages import Packages


class ThunderstoreAPI:
    API_URL = "https://thunderstore.io/api/v1/package/"

    def __init__(self):
        self.package_index = Packages()

    def update_package_index(self):
        package_data = requests.get(self.API_URL).json()
        self.package_index.update(package_data)
