import pytest
import random
import json

from uuid import uuid4
from distutils.version import StrictVersion

from ..types import PackageReference
from ..containers import PackageContainer, Packages
from ..models import Package


def create_package_data(namespace, name, version_numbers):
    reference = PackageReference(namespace, name)
    package_data = {"full_name": str(reference), "uuid": str(uuid4())}
    versions = []

    for version_number in version_numbers:
        version_reference = PackageReference(
            namespace=reference.namespace,
            name=reference.name,
            version=StrictVersion(version_number),
        )
        versions.append({"full_name": str(version_reference), "uuid": str(uuid4())})

    package_data["versions"] = versions
    return package_data


@pytest.mark.parametrize("package_count", [2, 3, 0, 48, 7, 1])
def test_len(package_count):
    versions = [f"1.0.{x}" for x in range(random.randint(2, 5))]
    packages = [
        create_package_data("SomeUser", f"package-{i}", versions)
        for i in range(package_count)
    ]
    container = PackageContainer.with_data(packages)
    assert len(container) == package_count


def test_accessing():
    data = [create_package_data("SomeUser", "somePackage", ["1.0.1", "1.0.2"])]
    packages = PackageContainer.with_data(data)
    assert "SomeUser-somePackage" in packages
    assert "SomeUser-somePackage-1.0.0" not in packages
    assert "AnotherUser-somePackage" not in packages
    reference = PackageReference("SomeUser", "somePackage")
    assert reference in packages
    package = Package(data[0])
    assert package in packages

    data = [create_package_data("another", "somePackage", ["1.0.1", "1.0.2"])]
    packages.update(data)
    assert "another-somePackage" in packages

    with pytest.raises(KeyError):
        54 in packages
    with pytest.raises(ValueError):
        "not a package reference" in packages


@pytest.mark.parametrize("package_count", [2, 3, 0, 48, 7, 1])
def test_iterating(package_count):
    data = [
        create_package_data("SomeUser", f"package-{i}", ["1.0.1", "1.0.2"])
        for i in range(package_count)
    ]
    all_references = set([PackageReference.parse(x["full_name"]) for x in data])
    packages = PackageContainer.with_data(data)
    for package in packages:
        # Raises an error if it doesn't exist
        all_references.remove(package.package_reference)


def test_items():
    data = [
        create_package_data("SomeUser", "somePackage", ["1.0.1", "1.0.2"]),
        create_package_data("another", "package", ["1.0.1", "1.0.2"]),
    ]
    keys = [PackageReference.parse(x["full_name"]) for x in data]
    # We use json because dict isn't hashable
    values = [json.dumps(x) for x in data]
    packages = PackageContainer.with_data(data)

    keys_set = set(keys)
    values_set = set(values)
    for key, value in packages.items():
        keys_set.remove(key)
        values_set.remove(json.dumps(value.data))

    keys_set = set(keys)
    for key in packages.keys():
        keys_set.remove(key)

    values_set = set(values)
    for value in packages.values():
        values_set.remove(json.dumps(value.data))


def test_update():
    data = [
        create_package_data("SomeUser", "somePackage", ["1.0.1", "1.0.2"]),
        create_package_data("another", "package", ["1.0.1", "1.0.2"]),
    ]
    packages = Packages()
    assert len(packages) == 0

    packages.update(data)
    assert len(packages) == 2
    assert len(packages["SomeUser-somePackage"].versions) == 2
    assert len(packages["another-package"].versions) == 2

    data = [create_package_data("SomeUser", "somePackage", ["1.0.1"])]
    packages.update(data)
    assert len(packages) == 2
    assert len(packages["SomeUser-somePackage"].versions) == 1
    assert len(packages["another-package"].versions) == 2


def test_versions_access():
    data = [
        create_package_data("SomeUser", "somePackage", ["1.0.1", "1.0.2"]),
        create_package_data("another", "package", ["1.0.1", "1.0.2"]),
    ]
    packages = Packages.with_data(data)

    package = PackageReference.parse("SomeUser-somePackage")
    version = package.with_version("1.0.1")

    assert package in packages
    package = packages[package]
    assert package.package_reference == package.package_reference
    assert version in packages
    version = packages[version]
    assert version.package_reference == version.package_reference

    assert "SomeUser-somePackage-1.0.1" in packages
    assert "SomeUser-somePackage-1.0.2" in packages
    assert "another-package-1.0.1" in packages
    assert "another-package-1.0.2" in packages


def test_adding_version_to_packages_fail():
    data = [create_package_data("SomeUser", "somePackage", ["1.0.1", "1.0.2"])]
    packages = Packages.with_data(data)
    with pytest.raises(ValueError):
        packages.add_package(packages["SomeUser-somePackage-1.0.1"])


def test_adding_package_to_versions_fail():
    data = [create_package_data("SomeUser", "somePackage", ["1.0.1", "1.0.2"])]
    packages = Packages.with_data(data)
    with pytest.raises(ValueError):
        package = packages["SomeUser-somePackage"]
        package.versions.add_package(package)
