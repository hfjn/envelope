from typing import Any, MutableMapping

import click
import pendulum


def pretty_dict(
    d: MutableMapping[str, Any], *, level: int = 0, break_after_key: bool = False
) -> None:
    max_col_length = max([len(key) for key in d.keys()])

    for key, value in d.items():
        output = "".ljust(2 * level)
        output += f"{key}:".ljust(max_col_length + 1)
        if isinstance(value, dict):
            click.echo(output)
            pretty_dict(value, level=level + 1, break_after_key=break_after_key)
            continue

        if break_after_key:
            click.echo(output)
            output = "".ljust(2 * level + 2)

        if type(value) in OUTPUT_MAPPING:
            value = OUTPUT_MAPPING[type(value)](value)

        output += value

        click.echo(f"{output}")


def format_pendulum(value: pendulum.DateTime) -> str:
    return f"{value.date().isoformat()}"


def format_float(value: float) -> str:
    return f"{value:0.2f} €".rjust(10)


OUTPUT_MAPPING = {pendulum.DateTime: format_pendulum, float: format_float}
