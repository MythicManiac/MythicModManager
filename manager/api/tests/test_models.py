import json

import dateutil.parser
from distutils.version import StrictVersion
from uuid import UUID

from ..models import Package, PackageVersion
from ..types import PackageReference


TEST_PACKAGE_JSON = """
{
    "name": "MythicModManager",
    "full_name": "MythicManiac-MythicModManager",
    "owner": "MythicManiac",
    "package_url": "https://thunderstore.io/package/MythicManiac/MythicModManager/",
    "maintainers": [],
    "date_created": "2019-04-22T20:58:48.580581Z",
    "date_updated": "2019-04-22T21:27:16.567749Z",
    "uuid4": "01a37972-5a4f-4419-8725-f54a29c862d3",
    "is_pinned": true,
    "versions": [
        {
            "name": "MythicModManager",
            "full_name": "MythicManiac-MythicModManager-1.0.1",
            "description": "Download, Install, Enable, and Disable mods automatically. Includes BepInEx",
            "icon": "https://storage.googleapis.com/thunderstore/live/MythicManiac-MythicModManager-1.0.1.png",
            "version_number": "1.0.1",
            "dependencies": ["TestUser-TestMod-0.1.0"],
            "download_url": "https://thunderstore.io/package/download/MythicManiac/MythicModManager/1.0.1/",
            "downloads": 2670,
            "date_created": "2019-04-22T21:27:15.413861Z",
            "website_url": "https://github.com/MythicManiac/MythicModManager",
            "is_active": true,
            "uuid4": "c5eaa105-a522-49aa-bae6-8c423ec06310"
        },
        {
            "name": "MythicModManager",
            "full_name": "MythicManiac-MythicModManager-1.0.0",
            "description": "Download, Install, Enable, and Disable mods automatically.",
            "icon": "https://storage.googleapis.com/thunderstore/live/MythicManiac-MythicModManager-1.0.0.png",
            "version_number": "1.0.0",
            "dependencies": [],
            "download_url": "https://thunderstore.io/package/download/MythicManiac/MythicModManager/1.0.0/",
            "downloads": 62,
            "date_created": "2019-04-22T20:58:49.124986Z",
            "website_url": "https://github.com/MythicManiac/MythicModManager",
            "is_active": true,
            "uuid4": "407b1c2a-04d0-41e4-93a2-4ea02f2227bd"
        }
    ]
}
"""


def test_package_model():
    data = json.loads(TEST_PACKAGE_JSON)
    package = Package(data)

    assert package.name == "MythicModManager"
    assert package.full_name == PackageReference.parse("MythicManiac-MythicModManager")
    assert package.owner == "MythicManiac"
    assert package.package_url == (
        "https://thunderstore.io/package/MythicManiac/MythicModManager/"
    )
    assert package.maintainers == []
    assert package.date_created == dateutil.parser.parse("2019-04-22T20:58:48.580581Z")
    assert package.date_created.year == 2019
    assert package.date_created.month == 4
    assert package.date_created.day == 22
    assert package.date_created.hour == 20
    assert package.date_created.minute == 58
    assert package.date_created.second == 48
    assert package.date_created.microsecond == 580581
    assert package.date_updated == dateutil.parser.parse("2019-04-22T21:27:16.567749Z")
    assert package.uuid4 == UUID("01a37972-5a4f-4419-8725-f54a29c862d3")
    assert package.is_pinned is True
    assert str(package) == "MythicManiac-MythicModManager"
    assert repr(package) == "<Package: MythicManiac-MythicModManager>"

    assert len(package.versions) == 2
    for version in package.versions:
        assert isinstance(version, PackageVersion)

    version = package.versions["MythicManiac-MythicModManager-1.0.1"]
    assert version.name == "MythicModManager"
    assert version.full_name == PackageReference.parse(
        "MythicManiac-MythicModManager-1.0.1"
    )
    assert (
        version.description
        == "Download, Install, Enable, and Disable mods automatically. Includes BepInEx"
    )
    assert version.icon == (
        "https://storage.googleapis.com/thunderstore/live/MythicManiac-MythicModManager-1.0.1.png"
    )
    assert version.version_number == StrictVersion("1.0.1")
    assert len(version.dependencies) == 1
    assert version.dependencies[0] == PackageReference.parse("TestUser-TestMod-0.1.0")

    download_url = (
        "https://thunderstore.io/package/download/MythicManiac/MythicModManager/1.0.1/"
    )
    assert version.download_url == download_url

    assert version.downloads == 2670
    assert version.date_created == dateutil.parser.parse("2019-04-22T21:27:15.413861Z")
    assert version.website_url == "https://github.com/MythicManiac/MythicModManager"
    assert version.is_active is True
    assert version.uuid4 == UUID("c5eaa105-a522-49aa-bae6-8c423ec06310")
    assert str(version) == "MythicManiac-MythicModManager-1.0.1"
    assert repr(version) == "<Package: MythicManiac-MythicModManager-1.0.1>"

    assert package.downloads == 2670 + 62
