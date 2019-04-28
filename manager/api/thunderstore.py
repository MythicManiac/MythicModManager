import requests
import requests_async

from urllib import parse

from .containers import Packages


class ThunderstoreAPI:
    def __init__(self, thunderstore_url):
        self.thunderstore_url = thunderstore_url
        self.api_url = parse.urljoin(thunderstore_url, "api/v1/")
        self.package_url = parse.urljoin(self.api_url, "package/")
        self.packages = Packages()

    def update_packages(self):
        data = requests.get(self.package_url).json()
        self.update_packages_with_data(data)

    async def async_update_packages(self):
        data = await requests_async.get(self.package_url)
        data = data.json()
        self.update_packages_with_data(data)

    def update_packages_with_data(self, data):
        self.packages.update(data)

    # TODO: Deprecate
    def get_package_names(self):
        return [str(x) for x in self.packages.keys()]

    def get_package_download_url(self, reference):
        if not reference.version:
            raise AttributeError("Unable to get package download URL without a version")
        return parse.urljoin(
            self.thunderstore_url,
            "/".join(
                (
                    "package",
                    "download",
                    reference.namespace,
                    reference.name,
                    reference.version_str,
                )
            ),
        )
