import os
import subprocess

from aur.client import fetch_info
from build.cacheclean import get_cache_dir
from common.types import PacmanInfo
from ui.output import (
    print_ask,
    print_aur_summary,
    print_combined_summary,
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


def install(pkgnames: list[str]) -> None:
    pacman_pkgs = []
    aur_pkgs = []

    for pkgname in pkgnames:
        if search_in_pacman(pkgname):
            pacman_pkgs.append(pkgname)
        else:
            aur_pkgs.append(pkgname)

    all_depends = []
    all_opt_depends = []
    all_make_depends = []

    for pkg in pacman_pkgs:
        info = fetch_pacman_info(pkg)
        all_depends.extend(info.depends)
        all_opt_depends.extend(info.opt_depends)

    for pkg in aur_pkgs:
        info = fetch_info(pkg)
        all_depends.extend(info.depends)
        all_opt_depends.extend(info.opt_depends or [])
        all_make_depends.extend(info.make_depends or [])

    all_depends = list(set(all_depends))
    all_opt_depends = list(set(all_opt_depends))
    all_make_depends = list(set(all_make_depends))

    print_combined_summary(
        pacman_pkgs, aur_pkgs, all_depends, all_opt_depends, all_make_depends
    )
    answer = input().strip().lower()
    if answer not in ("y", ""):
        print_err("installation aborted")
        return

    if pacman_pkgs:
        result_pacman = subprocess.run(
            ["sudo", "pacman", "-S", "--needed"] + pacman_pkgs
        )
        if result_pacman.returncode != 0:
            print_err("pacman installation failed")
            return
        else:
            print_success(f"installed: {', '.join(pacman_pkgs)} :3")

    base_dir = os.path.join(os.path.expanduser("~/.cache"), "calico")

    for pkg in aur_pkgs:
        pkg_dir = os.path.join(base_dir, pkg)
        os.makedirs(pkg_dir, exist_ok=True)
        try:
            clone_or_pull(pkg, pkg_dir)
            show_pkgbuild(pkg_dir)
            print_ask("proceed with build?", default_yes=False)
            answer = input().strip().lower()
            if answer != "y":
                print_err(f"build of {pkg} aborted")
                continue

            result_aur = subprocess.run(["makepkg", "-si"], cwd=pkg_dir)
            if result_aur.returncode != 0:
                print_err(f"{pkg} could not be built, skipping")
                continue
            else:
                print_success(f"installation of {pkg} succeeded :3")
        except Exception as e:
            print_err(f"failed to build {pkg}", e)
            continue
