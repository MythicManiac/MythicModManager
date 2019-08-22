import wx
from enum import Enum, auto

from aenum import NamedConstant


class Tabs(Enum):
    """
        To add a new Tab, just add a new enum. The value will be the name of the tab.
    """

    def _generate_next_value_(name, start, count, last_values):
        return name.title().replace("_", " ")

    MANAGER = auto()
    MOD_LIST = auto()
    JOB_QUEUE = auto()
    SETTINGS = auto()
    ABOUT = auto()


class Buttons(Enum):
    # These are the strings used inside of buttons used Globally, put in one place for easy updating
    UNINSTALL = "uninstall"
    UPDATE = "update installed mods"
    EXPORT = "export"
    IMPORT = "import"
    INSTALL = "install"
    DELETE = "delete"
    REFRESH = "refresh"
    INSTALL_SELECTED = "install selected"
    DETAILS = "more metails"
    LAUNCH = "launch game"


def make_list_ctrl_enum_value(title, width=None, format_enum=wx.LIST_FORMAT_LEFT):
    return {"heading": title.title(), "width": width, "format": format_enum}


class ColumnEnums(Enum):
    # These column enums exist to be put inside of enums that represent each ListCtrl and the column names that correlate to them.
    def _generate_next_value_(name, start, count, last_values):
        return name.title().replace("_", " ")

    NAME = auto()
    OWNER = auto()
    DESCRIPTION = auto()
    LATEST_VERSION = auto()
    DOWNLOADS = auto()
    NAMESPACE = "Author"
    VERSION = auto()
    PARAMETERS_STR = "Parameters"


# The NamedConstant class must be used to allow unique lists with the same column names
class ListCtrlEnums(NamedConstant):
    MODS = [
        ColumnEnums.NAME,
        ColumnEnums.OWNER,
        ColumnEnums.DESCRIPTION,
        ColumnEnums.LATEST_VERSION,
        ColumnEnums.DOWNLOADS,
    ]
    DOWNLOADED = [ColumnEnums.NAME, ColumnEnums.NAMESPACE, ColumnEnums.VERSION]
    INSTALLED = [ColumnEnums.NAME, ColumnEnums.NAMESPACE, ColumnEnums.VERSION]
    JOBS = [ColumnEnums.NAME, ColumnEnums.PARAMETERS_STR]


def make_mod_list_value(TabEnum=None, ListCtrlEnum=None):
    return tuple([TabEnum, ListCtrlEnum, ListCtrlEnum._name_])


class ModLists(Enum):
    REMOTE_MODS = make_mod_list_value(Tabs.MOD_LIST, ListCtrlEnums.MODS)
    INSTALLED_MODS = make_mod_list_value(Tabs.MANAGER, ListCtrlEnums.INSTALLED)
    DOWNLOADED_MODS = make_mod_list_value(Tabs.MANAGER, ListCtrlEnums.DOWNLOADED)
    JOB_QUEUE = make_mod_list_value(Tabs.JOB_QUEUE, ListCtrlEnums.JOBS)
