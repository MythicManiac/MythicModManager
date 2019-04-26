from __future__ import annotations

import dateutil.parser

from datetime import datetime
from distutils.version import StrictVersion
from typing import List
from urllib.parse import urlparse, ParseResult
from uuid import UUID

from cached_property import cached_property

from .types import PackageReference


class PackageVersion:
    def __init__(self, data):
        self.data = data

    @property
    def name(self) -> str:
        """ Name of this package version """
        return self.data["name"]

    @cached_property
    def full_name(self) -> PackageReference:
        """ The package reference to this package version """
        return PackageReference.parse(self.data["full_name"])

    @property
    def description(self) -> str:
        """ Description of this package version """
        return self.data["description"]

    @cached_property
    def icon(self) -> ParseResult:
        """ Icon URL of this package version """
        return urlparse(self.data["icon"])

    @cached_property
    def version_number(self) -> StrictVersion:
        """ Version number of this package version """
        return StrictVersion(self.data["version_number"])

    @cached_property
    def dependencies(self) -> List[PackageReference]:
        """ List of other package references this package version depends on """
        return [PackageReference.parse(entry) for entry in self.data["dependencies"]]

    @cached_property
    def download_url(self) -> ParseResult:
        """ Download URL of this package version """
        return urlparse(self.data["download_url"])

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

    @cached_property
    def uuid4(self) -> UUID:
        """ UUID4 of this package version """
        return UUID(self.data["uuid4"])


class Package:
    def __init__(self, data):
        self.data = data

    @property
    def name(self) -> str:
        """ Name of this package """
        return self.data["name"]

    @cached_property
    def full_name(self) -> PackageReference:
        """ The package reference object to this package """
        return PackageReference.parse(self.data["full_name"])

    @property
    def owner(self) -> str:
        """ The owner of this package """
        return self.data["owner"]

    @cached_property
    def package_url(self) -> ParseResult:
        """ The URL of this package's page """
        return urlparse(self.data["package_url"])

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
    def uuid4(self) -> UUID:
        """ UUID4 of this package """
        return UUID(self.data["uuid4"])

    @cached_property
    def is_pinned(self) -> bool:
        """ Is this package pinned on the mod list or not """
        return bool(self.data["is_pinned"])

    @cached_property
    def versions(self) -> List[PackageVersion]:
        """ List of PackageVersion objects for this package """
        return [PackageVersion(entry) for entry in self.data["versions"]]