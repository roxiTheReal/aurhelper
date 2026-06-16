import os
import shutil
import subprocess

from ui.output import print_ask, print_err, print_success


def get_cache_dir() -> str:
    return os.path.join(os.path.expanduser("~/.cache"), "calico")


def clean_pacman_cache() -> None:
    print_ask("also clean pacman's package cache?", default_yes=False)
    answer = input().strip().lower()
    if answer != "y":
        return

    result = subprocess.run(["sudo", "pacman", "-Scc", "--noconfirm"])
    if result.returncode == 0:
        print_success("pacman cache cleaned :3")
    else:
        print_err("failed to clean pacman cache")


def clean_cache(pkgname: str | None) -> None:
    cache_dir = get_cache_dir()

    if not os.path.exists(cache_dir):
        print_err("nothing to clean, cache is empty")
        return

    if not pkgname:
        print_ask("remove ALL packages in calico's cache?", default_yes=False)
        answer = input().strip().lower()
        if answer != "y":
            print_err("clean aborted")
            return

        shutil.rmtree(cache_dir)
        print_success("cache cleaned :3")
        clean_pacman_cache()

    else:
        pkg_dir = os.path.join(cache_dir, pkgname)
        if not os.path.exists(pkg_dir):
            print_err(f"no cache found for {pkgname}")
            return

        print_ask(f"remove calico cache for package {pkgname}", default_yes=True)
        answer = input().strip().lower()
        if answer not in ("y", ""):
            print_err("clean aborted")
            return

        shutil.rmtree(pkg_dir)
        print_success(f"cache for package {pkgname} cleaned :3")
