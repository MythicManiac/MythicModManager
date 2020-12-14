import requests_async

from urllib import parse

from .containers import Packages


class ThunderstoreAPI:
    def __init__(self, repository_url):
        self.repository_url = repository_url
        self.api_url = parse.urljoin(repository_url, "api/v1/")
        self.package_url = parse.urljoin(self.api_url, "package/")
        self.packages = Packages()

    async def async_update_packages(self):
        data = await requests_async.get(self.package_url)
        data = data.json()
        self.update_packages_with_data(data)

    def update_packages_with_data(self, data):
        self.packages.update(data)

    def get_package_download_url(self, reference):
        if not reference.version:
            raise AttributeError("Unable to get package download URL without a version")
        return parse.urljoin(
            self.repository_url,
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
