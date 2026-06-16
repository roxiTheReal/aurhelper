import click

from aur.client import search
from build.cacheclean import clean_cache
from build.installer import install
from common.config import open_config
from ui.output import Colors


@click.group()
def cli():
    """calico - a minimal aur helper"""
    pass


@cli.command()
@click.argument("pkgnames", nargs=-1, required=True)
def install_cmd(pkgnames):
    """install one or more packages"""
    install(list(pkgnames))


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


@cli.command()
@click.argument("pkgname", required=False)
def clean_cmd(pkgname):
    """clean calico's cache for one or all packages"""
    clean_cache(pkgname)


@cli.command()
def config():
    """open calico's config file"""
    open_config()


if __name__ == "__main__":
    cli()
