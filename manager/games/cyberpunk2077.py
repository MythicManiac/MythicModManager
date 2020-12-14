import subprocess
import webbrowser

from pathlib import Path

from manager.games.game import Game


class Cyberpunk2077(Game):
    GAME_ID = "cyberpunk2077"
    STEAM_ID = "1091500"

    def find_gog_install_path(self):
        try:
            import winreg
        except ImportError:
            return None

        try:
            aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            aKey = winreg.OpenKey(
                aReg, "SOFTWARE\\WOW6432Node\\GOG.com\\Games\\1423049311"
            )

            path = Path(winreg.QueryValueEx(aKey, "path")[0])
            winreg.CloseKey(aReg)
            winreg.CloseKey(aKey)

            return path
        except Exception:
            return None

    def find_steam_install_path(self):
        try:
            import winreg
        except ImportError:
            return None

        try:
            aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            aKey = winreg.OpenKey(
                aReg,
                f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Steam App {self.STEAM_ID}\\InstallLocation",
            )

            path = Path(winreg.QueryValueEx(aKey, "SteamPath")[0])
            winreg.CloseKey(aReg)
            winreg.CloseKey(aKey)

            return path
        except Exception:
            return None

    def verify_install_path(self, location):
        return (location / "bin" / "x64" / "Cyberpunk2077.exe").is_file()

    def autodiscover_game_path(self):
        path = self.find_gog_install_path()
        if path:
            return path
        path = self.find_steam_install_path()
        if path:
            return path
        return None

    def launch_game(self):
        if self.find_steam_install_path():
            webbrowser.open_new(f"steam://run/{self.STEAM_ID}")
        else:
            subprocess.Popen(
                [str((self.game_path / "bin" / "x64" / "Cyberpunk2077.exe").resolve())]
            )
