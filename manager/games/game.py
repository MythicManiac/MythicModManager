from pathlib import Path
from typing import Optional

from manager.config import Configuration
from manager.exceptions import GamePathNotFound


class Game:
    GAME_ID: Optional[str] = None

    def __init__(self, config: Configuration):
        self.config = config
        self.game_path = self.find_install_path()

    def get_game_id(self):
        if not self.GAME_ID:
            raise NotImplementedError("GAME_ID must be defined")
        return self.GAME_ID

    def get_config(self, name):
        return self.config.get_game_config(self.get_game_id(), name)

    def set_config(self, name, value):
        return self.config.set_game_config(self.get_game_id(), name, value)

    def validate_paths(self):
        if not self.game_path:
            raise GamePathNotFound()

    def get_install_path(self):
        if not self.game_path:
            raise GamePathNotFound()
        return self.game_path

    def find_install_path(self) -> Optional[Path]:
        path: Optional[Path] = Path(self.get_config("install_path"))
        if path and self.verify_install_path(path):
            return path

        try:
            path = self.autodiscover_game_path()
            if path and self.verify_install_path(path):
                self.set_config("install_path", str(path.resolve()))
                return path
        except Exception:
            pass
        return None

    def autodiscover_game_path(self) -> Optional[Path]:
        raise NotImplementedError()

    def verify_install_path(self, path: Path):
        raise NotImplementedError()

    def launch_game(self):
        raise NotImplementedError()

    def get_repository_url(self) -> str:
        return self.get_config("repository_url")

    def get_mod_cache_path(self) -> Path:
        return self.get_install_path() / "modding" / "mods" / "cache"

    def get_managed_mods_path(self) -> Path:
        return self.get_install_path() / "modding" / "mods" / "managed"

    def get_extracted_log_path(self) -> Path:
        return self.get_install_path() / "modding" / "mods" / "extracted"
