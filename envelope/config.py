import os
from pathlib import Path
from typing import Any, List, MutableMapping

import click
import toml


class Config:
    def __init__(self) -> None:
        self.config = self._load_config()

    @property
    def debug_mode(self) -> bool:
        return self.config["settings"]["debug_mode"]

    @property
    def database_name(self) -> str:
        return self.config["settings"]["db_name"]

    @property
    def database_path(self) -> Path:
        return Path(self.folder) / self.database_name

    @property
    def folder(self) -> Any:
        return self.config["settings"]["folder"]

    @property
    def snapshot_name(self) -> Any:
        return self.config["settings"]["snapshot_name"]

    @property
    def accounts(self) -> Any:
        return self.config["accounts"]

    @property
    def accounts_names(self) -> List[str]:
        return [
            account["friendly_name"] for _, account in self.config["accounts"].items()
        ]

    def _load_config(self) -> MutableMapping[str, Any]:
        config_path = self._get_config_path()
        with config_path.open() as f:
            return toml.load(f)

    def _get_config_path(self) -> Path:
        if os.environ.get("ENVELOPE_ENV") == "dev":
            return Path(__file__).parent.parent / "config.toml"
        return Path(click.get_app_dir("envelope", force_posix=True)) / "config.toml"
