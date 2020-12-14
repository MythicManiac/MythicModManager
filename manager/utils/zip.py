import os
import os.path
import shutil
from zipfile import ZipInfo


def extractall_starting_from(archive, start_from, destination, pwd=None):
    for zipinfo in archive.namelist():
        _extract_member_starting_from(archive, zipinfo, start_from, destination, pwd)


def extract_starting_from(archive, member, start_from, destination, pwd=None):
    return _extract_member_starting_from(archive, member, start_from, destination, pwd)


def _extract_member_starting_from(archive, member, start_from, targetpath, pwd):
    """Extract the ZipInfo object 'member' to a physical
       file on the path targetpath.
    """
    if not isinstance(member, ZipInfo):
        member = archive.getinfo(member)

    # build the destination pathname, replacing
    # forward slashes to platform specific separators.
    arcname = member.filename.replace("/", os.path.sep)
    start_from_path = start_from.replace("/", os.path.sep)

    if os.path.altsep:
        arcname = arcname.replace(os.path.altsep, os.path.sep)
    # interpret absolute pathname as relative, remove drive letter or
    # UNC path, redundant separators, "." and ".." components.
    arcname = os.path.splitdrive(arcname)[1]
    invalid_path_parts = ("", os.path.curdir, os.path.pardir)
    arcname = os.path.sep.join(
        x for x in arcname.split(os.path.sep) if x not in invalid_path_parts
    )

    split_arcname = arcname.split(os.path.sep)
    split_start_from = start_from_path.split(os.path.sep)
    if split_start_from and not split_start_from[-1]:
        split_start_from = split_start_from[:-1]

    for index, piece in enumerate(split_start_from):
        if index >= len(split_arcname) or split_arcname[index] != piece:
            return None
    arcname = os.path.sep.join(split_arcname[len(split_start_from) :])
    if not arcname:
        return None

    if os.path.sep == "\\":
        # filter illegal characters on Windows
        arcname = archive._sanitize_windows_name(arcname, os.path.sep)

    targetpath = os.path.join(targetpath, arcname)
    targetpath = os.path.normpath(targetpath)

    # Create all upper directories if necessary.
    upperdirs = os.path.dirname(targetpath)
    if upperdirs and not os.path.exists(upperdirs):
        os.makedirs(upperdirs)

    if member.is_dir():
        if not os.path.isdir(targetpath):
            os.mkdir(targetpath)
        return targetpath

    with archive.open(member, pwd=pwd) as source, open(targetpath, "wb") as target:
        shutil.copyfileobj(source, target)

    return targetpath
