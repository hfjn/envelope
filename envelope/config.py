import os
from pathlib import Path
from typing import Any, MutableMapping

import click
import toml


def get_config() -> MutableMapping[str, Any]:
    config_path = get_config_path()
    with config_path.open() as f:
        return toml.load(f)


def get_config_path() -> Path:
    click.echo(os.environ.get("ENVELOPE_ENV"))
    if os.environ.get("ENVELOPE_ENV") == "dev":
        click.echo("Loading Dev Config")
        return Path(__file__).parent.parent / "config.toml"
    return Path(click.get_app_dir("envelope", force_posix=True)) / "config.toml"
