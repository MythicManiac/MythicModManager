import webbrowser
from pathlib import Path

from manager.games.game import Game


class RiskOfRain2(Game):
    GAME_ID = "riskofrain2"

    def verify_install_path(self, location):
        return (location / "Risk of Rain 2.exe").is_file()

    def autodiscover_game_path(self):
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

    def get_managed_mods_path(self):
        return self.game_path / "BepInEx" / "plugins"

    def launch_game(self):
        webbrowser.open_new("steam://run/632360")
