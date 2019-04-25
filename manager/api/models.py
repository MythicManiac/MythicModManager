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
        return self.data["name"]

    @cached_property
    def full_name(self) -> PackageReference:
        return PackageReference.parse(self.data["full_name"])

    @property
    def description(self) -> str:
        return self.data["description"]

    @cached_property
    def icon(self) -> ParseResult:
        return urlparse(self.data["icon"])

    @cached_property
    def version_number(self) -> StrictVersion:
        return StrictVersion(self.data["version_number"])

    @cached_property
    def dependencies(self) -> List[PackageReference]:
        return [PackageReference.parse(entry) for entry in self.data["dependencies"]]

    @cached_property
    def download_url(self) -> ParseResult:
        return urlparse(self.data["download_url"])

    @cached_property
    def downloads(self) -> int:
        return int(self.data["downloads"])

    @cached_property
    def date_created(self) -> datetime:
        return dateutil.parser.parse(self.data["date_created"])

    @property
    def website_url(self) -> str:
        return self.data["website_url"]

    @cached_property
    def is_active(self) -> bool:
        return bool(self.data["is_active"])

    @cached_property
    def uuid4(self) -> UUID:
        return UUID(self.data["uuid4"])


class Package:
    def __init__(self, data):
        self.data = data

    @property
    def name(self) -> str:
        return self.data["name"]

    @cached_property
    def full_name(self) -> PackageReference:
        return PackageReference.parse(self.data["full_name"])

    @property
    def owner(self) -> str:
        return self.data["owner"]

    @cached_property
    def package_url(self) -> ParseResult:
        return urlparse(self.data["package_url"])

    @property
    def maintainers(self) -> List[str]:
        return self.data["maintainers"]

    @cached_property
    def date_created(self) -> datetime:
        return dateutil.parser.parse(self.data["date_created"])

    @cached_property
    def date_updated(self) -> datetime:
        return dateutil.parser.parse(self.data["date_updated"])

    @cached_property
    def uuid4(self) -> UUID:
        return UUID(self.data["uuid4"])

    @cached_property
    def is_pinned(self) -> bool:
        return bool(self.data["is_pinned"])

    @cached_property
    def versions(self) -> List[PackageVersion]:
        return [PackageVersion(entry) for entry in self.data["versions"]]
