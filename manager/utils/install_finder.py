import toml
from pathlib import Path


def read_install_config():
    try:
        config_path = Path("config.toml")
        if config_path.is_file():
            dict = toml.load(config_path)
        else:
            dict = {"Steam_path": ""}
            with open(config_path, "w") as file:
                toml.dump(dict, file)
        return dict["Steam_path"]
    except Exception:
        raise ValueError("Config file is corrupt. Please repair or remove the file")


def find_windows_install_path():
    try:
        import winreg
    except ImportError:
        return None

    aReg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    aKey = winreg.OpenKey(aReg, r"Software\Valve\Steam")

    path = Path(winreg.QueryValueEx(aKey, "SteamPath")[0])
    winreg.CloseKey(aReg)
    winreg.CloseKey(aKey)

    return path / "steamapps/common/Risk of Rain 2/"


def find_steam_location():
    return find_windows_install_path()


def verify_steam_location(location):
    return (location / "Risk of Rain 2.exe").is_file()


def get_install_path():
    path = Path(read_install_config())
    if path and verify_steam_location(path):
        return path
    try:
        path = find_steam_location()
        if verify_steam_location(path):
            return path
    except Exception:
        raise FileNotFoundError(
            "Could not find your Steam folder. Please set path manually"
        )


# Todo: fix for custom steam installations
# # def extract config
#
# path = path / "config" / "config.vdf"
#
# with open(path) as file:
#     print("\n".join(file.readlines()).replace(r"\t", ""))
#     #json.load(json_file)
