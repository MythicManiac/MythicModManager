from __future__ import annotations

import dateutil.parser

from datetime import datetime
from distutils.version import StrictVersion
from typing import List
from uuid import UUID

from cached_property import cached_property

from .types import PackageReference
from .containers import PackageVersions


class BasePackage:
    def __init__(self, data):
        self.data = data

    @cached_property
    def full_name(self) -> PackageReference:
        """ The package reference to this package """
        return PackageReference.parse(self.data["full_name"])

    @property
    def package_reference(self) -> PackageReference:
        """ The package reference to this package """
        return self.full_name

    @cached_property
    def uuid4(self) -> UUID:
        """ UUID4 of this package """
        return UUID(self.data["uuid4"])

    def __str__(self) -> str:
        return str(self.package_reference)

    def __repr__(self) -> str:
        return f"<Package: {str(self)}>"


class PackageVersion(BasePackage):
    @property
    def name(self) -> str:
        """ Name of this package version """
        return self.data["name"]

    @property
    def description(self) -> str:
        """ Description of this package version """
        return self.data["description"]

    @property
    def icon(self) -> str:
        """ Icon URL of this package version """
        return self.data["icon"]

    @cached_property
    def version_number(self) -> StrictVersion:
        """ Version number of this package version """
        return StrictVersion(self.data["version_number"])

    @cached_property
    def dependencies(self) -> List[PackageReference]:
        """ List of other package references this package version depends on """
        return [PackageReference.parse(entry) for entry in self.data["dependencies"]]

    @property
    def download_url(self) -> str:
        """ Download URL of this package version """
        return self.data["download_url"]

    @cached_property
    def downloads(self) -> int:
        """ Amount of times this package version has been downloaded """
        return int(self.data["downloads"])

    @cached_property
    def date_created(self) -> datetime:
        """ Datetime when this package version was created """
        return dateutil.parser.parse(self.data["date_created"])

    @property
    def website_url(self) -> str:
        """ This package versions unvalidated website URL """
        return self.data["website_url"]

    @cached_property
    def is_active(self) -> bool:
        """ Whether or not this package version is active/enabled """
        return bool(self.data["is_active"])


class Package(BasePackage):
    @property
    def name(self) -> str:
        """ Name of this package """
        return self.data["name"]

    @property
    def owner(self) -> str:
        """ The owner of this package """
        return self.data["owner"]

    @property
    def package_url(self) -> str:
        """ The URL of this package's page """
        return self.data["package_url"]

    @property
    def maintainers(self) -> List[str]:
        """ List of this package's maintainers """
        return self.data["maintainers"]

    @cached_property
    def date_created(self) -> datetime:
        """ Datetime was created """
        return dateutil.parser.parse(self.data["date_created"])

    @cached_property
    def date_updated(self) -> datetime:
        """ Datetime when this package was last updated """
        return dateutil.parser.parse(self.data["date_updated"])

    @cached_property
    def is_pinned(self) -> bool:
        """ Is this package pinned on the mod list or not """
        return bool(self.data["is_pinned"])

    @cached_property
    def versions(self) -> List[PackageVersion]:
        """ List of PackageVersion objects for this package """
        return PackageVersions.with_data(self.data["versions"])

    @cached_property
    def downloads(self) -> int:
        """ The total amount of times this package has been downloaded """
        return sum(version.downloads for version in self.versions)

    @cached_property
    def description(self) -> str:
        """ The description of the latest version """
        return self.versions.latest.description

    @cached_property
    def icon(self) -> str:
        """ The icon URL of the latest version """
        return self.versions.latest.icon

    @cached_property
    def latest_version(self) -> StrictVersion:
        """ The version of the latest version """
        return self.versions.latest.version_number
