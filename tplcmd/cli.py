import os

import click
from rich.console import Console
from tplcmd.commands.scripts_cmd import scripts


def init_cli():

    console = Console()

    @click.group()
    def cli():
        """
        Command line tool
        """

    @click.command()
    def version():
        """Actual version"""
        from services.utils import get_version

        ver = get_version("__version__.py")
        console.print(f"[bold magenta]{ver}[/bold magenta]")

    cli.add_command(version)
    cli.add_command(scripts)
    return cli


cli = init_cli()

if __name__ == "__main__":

    cli()
