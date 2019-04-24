import json
import winreg
from pathlib import Path


def find_steam_location():
    aReg = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
    aKey = winreg.OpenKey(aReg, r"Software\Valve\Steam")

    path = Path(winreg.QueryValueEx(aKey, "SteamPath")[0])
    winreg.CloseKey(aReg)
    winreg.CloseKey(aKey)

    return path / "steamapps/common/Risk of Rain 2/"



# Todo: fix for custom steam installations
# # def extract config
#
# path = path / "config" / "config.vdf"
#
# with open(path) as file:
#     print("\n".join(file.readlines()).replace(r"\t", ""))
#     #json.load(json_file)
