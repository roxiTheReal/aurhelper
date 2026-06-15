import click

from aur.client import search
from build.installer import install
from ui.output import Colors


@click.group()
def cli():
    """calico - a minimal aur helper"""
    pass


@cli.command()
@click.argument("pkgname")
def install_cmd(pkgname):
    """install a package"""
    install(pkgname)


@cli.command()
@click.argument("query")
def search_cmd(query):
    """search for a package"""
    c = Colors
    results = search(query)
    for result in results:
        print(
            f"{c.BOLD}{c.PURPLE}aur{c.RESET}/{c.BOLD}{result.name}{c.RESET} {c.CYAN}{result.version}{c.RESET}"
        )
        print(f"    {result.description}")


if __name__ == "__main__":
    cli()
