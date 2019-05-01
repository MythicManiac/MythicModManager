import toml
import json
from pathlib import Path


def read_config_json():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        return config
    except Exception:
        return {}


def read_config_toml():
    json_config = read_config_json()
    default_path = json_config.get("risk_of_rain_path", "")

    try:
        config_path = Path("config.toml")
        if config_path.is_file():
            config = toml.load(config_path)
        else:
            config = {"risk_of_rain_2_path": default_path}
            with open(config_path, "w") as file:
                toml.dump(config, file)
        return config["risk_of_rain_2_path"]
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


def find_install_path():
    return find_windows_install_path()


def verify_install_path(location):
    return (location / "Risk of Rain 2.exe").is_file()


def get_install_path():
    path = Path(read_config_toml())
    if path and verify_install_path(path):
        return path

    try:
        path = find_install_path()
        if verify_install_path(path):
            return path
    except Exception:
        return None
