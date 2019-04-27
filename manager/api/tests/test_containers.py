import pytest
import random

from uuid import uuid4
from distutils.version import StrictVersion

from ..types import PackageReference
from ..containers import PackageContainer


def create_package_data(variation):
    reference = PackageReference(namespace="SomeUser", name=f"SomePackage-{variation}")
    package_data = {"full_name": str(reference), "uuid": str(uuid4())}
    version_numbers = [f"1.0.{x}" for x in range(random.randint(2, 5))]
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
    packages = [create_package_data(i) for i in range(package_count)]
    container = PackageContainer.with_data(packages)
    assert len(container) == package_count
