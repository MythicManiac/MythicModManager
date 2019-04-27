import requests
from urllib import parse

from .containers import Packages


class ThunderstoreAPI:
    def __init__(self, api_url):
        self.api_url = api_url
        self.packages = Packages()

    def update_packages(self):
        url = parse.urljoin(self.api_url, "package/")
        data = requests.get(url).json()
        self.update_packages_with_data(data)

    def update_packages_with_data(self, data):
        self.packages.update(data)

    def get_package_names(self):
        return [str(x) for x in self.packages.keys()]
