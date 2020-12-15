from pathlib import Path
from typing import Any

import toml


DEFAULT_CONFIG = {
    "games": {
        "riskofrain2": {
            "install_path": "",
            "repository_url": "https://thunderstore.io/",
        },
        "cyberpunk2077": {
            "install_path": "",
            "repository_url": "https://cybermods.net/",
        },
    }
}


class Configuration:
    def __init__(self, filepath: str, data: Any):
        self.data = data
        self.filepath = filepath

    @property
    def games(self):
        return self.data.get("games", {})

    def save(self):
        with open(self.filepath, "w") as file:
            toml.dump(self.data, file)

    def get_game_config(self, game, name, default=None):
        return self.games.get(game, {}).get(name, default)

    def set_game_config(self, game, name, value):
        self.data["game"] = self.games.get(game, {}).update({name: value})
        self.save()

    @classmethod
    def load_or_create(cls, filepath) -> "Configuration":
        try:
            config_path = Path(filepath)
            if config_path.is_file():
                config = toml.load(config_path)
                return Configuration(filepath, config)
            else:
                config = Configuration(filepath, DEFAULT_CONFIG)
                config.save()
                return config
        except Exception:
            raise ValueError("Config file is corrupt. Please repair or remove the file")
