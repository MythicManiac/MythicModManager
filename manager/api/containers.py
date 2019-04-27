from .types import PackageReference


class PackageContainer:
    """ Container for storing an index of packages """

    def __init__(self):
        self.packages = {}

    def __len__(self):
        return len(self.packages)

    @staticmethod
    def _handle_key(key) -> PackageReference:
        if isinstance(key, str):
            key = PackageReference.parse(key)
        if hasattr(key, "package_reference"):
            key = key.package_reference
        if not isinstance(key, PackageReference):
            raise KeyError("Key must be a valid package reference")
        return key

    def __getitem__(self, key):
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

    @property
    def package_cls(self):
        from .models import BasePackage

        return BasePackage

    def items(self):
        return self.packages.items()

    def keys(self):
        return self.packages.keys()

    def values(self):
        return self.packages.values()

    def add_package(self, package):
        self.packages[package.package_reference] = package

    def update(self, data):
        for entry in data:
            package = self.package_cls(entry)
            self.add_package(package)

    @classmethod
    def with_data(cls, data):
        packages = cls()
        packages.update(data)
        return packages


class Packages(PackageContainer):
    @property
    def package_cls(self):
        from .models import Package

        return Package

    def add_package(self, package):
        if package.package_reference.version is not None:
            raise ValueError(
                "Attempting to add a versioned package to a Packages container"
            )
        self.packages[package.package_reference] = package

    def __getitem__(self, key):
        key = self._handle_key(key)
        if key.version:
            return self.packages[key.without_version].versions[key]
        return self.packages[key]


class PackageVersions(PackageContainer):
    def add_package(self, package):
        if package.package_reference.version is None:
            raise ValueError(
                "Attempting to add a versionless package to a PackageVersions container"
            )
        self.packages[package.package_reference] = package

    @property
    def package_cls(self):
        from .models import PackageVersion

        return PackageVersion
