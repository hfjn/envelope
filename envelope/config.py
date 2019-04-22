import os
from pathlib import Path
from typing import Any, MutableMapping

import click
import toml


class Config:
    def __init__(self) -> None:
        self.config = self._load_config()

    @property
    def folder(self) -> Any:
        return self.config["settings"]["folder"]

    @property
    def snapshot_name(self) -> Any:
        return self.config["settings"]["snapshot_name"]

    def _load_config(self) -> MutableMapping[str, Any]:
        config_path = self._get_config_path()
        with config_path.open() as f:
            return toml.load(f)

    def _get_config_path(self) -> Path:
        if os.environ.get("ENVELOPE_ENV") == "dev":
            return Path(__file__).parent.parent / "config.toml"
        return Path(click.get_app_dir("envelope", force_posix=True)) / "config.toml"
