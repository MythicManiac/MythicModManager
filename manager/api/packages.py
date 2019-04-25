from .models import Package
from .types import PackageReference


class Packages:
    """ Container for storing an index of packages """

    def __init__(self):
        self.packages = {}

    def __len__(self):
        return len(self.packages)

    @staticmethod
    def _handle_key(key) -> PackageReference:
        if isinstance(key, str):
            key = PackageReference.parse(key)
        if not isinstance(key, PackageReference):
            raise KeyError("Key must be a valid package reference")
        return key

    def __getitem__(self, key) -> Package:
        key = self._handle_key(key)
        return self.packages[key]

    def __delitem__(self, key):
        key = self._handle_key(key)
        del self.packages[key]

    def __iter__(self):
        return iter(self.packages.values())

    def __contains__(self, item) -> bool:
        item = self._handle_key(item)
        return item in self.packages

    def items(self):
        return self.packages.items()

    def keys(self):
        return self.packages.keys()

    def values(self):
        return self.packages.values()

    def update(self, data):
        for entry in data:
            package = Package(data)
            self.packages[package.full_name] = package

    @classmethod
    def with_data(cls, data):
        packages = Packages()
        packages.update(data)
        return packages
