import os
import subprocess

from aur.client import fetch_info
from common.types import PacmanInfo
from ui.output import (
    print_ask,
    print_aur_summary,
    print_err,
    print_pacman_summary,
    print_success,
)


def search_in_pacman(pkgname: str) -> bool:
    result = subprocess.run(["pacman", "-Si", pkgname], capture_output=True)
    return result.returncode == 0


def fetch_pacman_info(query: str) -> PacmanInfo:
    result = subprocess.run(["pacman", "-Si", query], capture_output=True, text=True)
    lines = result.stdout.split("\n")

    name = ""
    version = ""
    depends = []
    opt_depends = []

    in_opt_depends = False

    for line in lines:
        if line.startswith(" ") and in_opt_depends:
            pkg_name = line.strip().split(":")[0].strip()
            opt_depends.append(pkg_name)
            continue

        in_opt_depends = False
        parts = line.split(" : ", 1)
        if len(parts) != 2:
            continue
        key = parts[0].strip()
        value = parts[1].strip()

        if key.lower() == "name":
            name = value
        elif key.lower() == "version":
            version = value
        elif key.lower() == "depends on":
            depends = value.split()
        elif key.lower() == "optional deps":
            in_opt_depends = True
            pkg_name = value.split(":")[0].strip()
            opt_depends.append(pkg_name)

    return PacmanInfo(
        name=name,
        version=version,
        depends=depends,
        opt_depends=opt_depends,
    )


def clone_or_pull(pkgname: str, pkg_dir: str) -> None:
    repo_url = f"https://aur.archlinux.org/{pkgname}.git"

    if not os.path.exists(pkg_dir) or not os.listdir(pkg_dir):
        result = subprocess.run(["git", "clone", repo_url, pkg_dir])
        if result.returncode != 0:
            raise Exception(f"failed to clone {pkgname} from aur")
    else:
        result = subprocess.run(["git", "-C", pkg_dir, "pull"])
        if result.returncode != 0:
            raise Exception(f"failed to pull {pkgname} from aur")


def show_pkgbuild(pkg_dir: str) -> None:
    pkgbuild_path = os.path.join(pkg_dir, "PKGBUILD")
    with open(pkgbuild_path, "r") as f:
        content = f.read()

    subprocess.run(["less"], input=content, text=True)


def install(pkgname: str) -> None:
    if search_in_pacman(pkgname):
        info = fetch_pacman_info(pkgname)
        print_pacman_summary(info)
        answer = input().strip().lower()
        if answer not in ("y", ""):
            print_err("installation aborted")
            return

        result = subprocess.run(
            ["sudo", "pacman", "-S", "--needed", "--noconfirm", pkgname]
        )
        if result.returncode == 0:
            print_success(f"installation of {pkgname} succeeded :3")
        else:
            print_err(f"{pkgname} could not be installed")
    else:
        info = fetch_info(pkgname)
        print_aur_summary(info)

        answer = input().strip().lower()
        if answer not in ("y", ""):
            print_err("installation aborted")
            return

        cache_dir = os.path.join(os.path.expanduser("~/.cache"), "calico", pkgname)
        os.makedirs(cache_dir, exist_ok=True)

        try:
            clone_or_pull(pkgname, cache_dir)
            show_pkgbuild(cache_dir)
            print_ask("proceed with build?", default_yes=False)
            answer = input().strip().lower()
            if answer != "y":
                print_err("build aborted")
                return

            result = subprocess.run(["makepkg", "-si"], cwd=cache_dir)
            if result.returncode == 0:
                print_success(f"installation of {pkgname} succeeded :3")
            else:
                print_err(f"{pkgname} could not be built")
        except Exception as e:
            print_err(f"failed to build {pkgname}", e)
