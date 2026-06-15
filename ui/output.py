from common.types import PackageInfo, PacmanInfo


class Colors:
    RESET = "\033[0m"
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    YELLOW = "\033[33m"


def print_err(err: str, *args) -> None:
    """
    Internal helper to print a properly formatted error message.
    @param err: The error to print.
    @param args: Optional arguments to include in the output.
    """
    c = Colors
    output = f"{c.RED}[ERROR] {c.RESET}:: {err}"
    if args:
        output += f": {args[0]}"
    print(output)


def print_warn(warn: str, *args) -> None:
    """
    Internal helper to print a properly formatted warning message.
    @param warn: The warning to print.
    @param args: Optional arguments to include in the output.
    """
    c = Colors
    output = f"{c.YELLOW}[WARN] {c.RESET}:: {warn}"
    if args:
        output += f": {args[0]}"
    print(output)


def print_info(info: str, *args) -> None:
    """
    Internal helper to print a properly formatted info message.
    @param info: The info to print.
    @param args: Optional arguments to include in the output.
    """
    c = Colors
    output = f"{c.BLUE}==> {c.RESET}{c.BOLD}{info}{c.RESET}"
    if args:
        output += f": {args[0]}"
    print(output)


def print_ask(ask: str, default_yes: bool = True) -> None:
    """
    Internal helper to print a properly formatted ask message.
    @param ask: The ask to print.
    @param default_yes: Whether the default answer is yes or no.
    """
    c = Colors
    if default_yes:
        indicator = f"[{c.GREEN}Y{c.RESET}/{c.RED}n{c.RESET}]"
    else:
        indicator = f"[{c.GREEN}y{c.RESET}/{c.RED}N{c.RESET}]"
    print(f"{c.BLUE}[?] {c.RESET}:: {ask} {indicator} ", end="")


def print_success(scs: str, *args) -> None:
    """
    Internal helper to print a properly formatted ask message.
    @param succ: The success message to print.
    @param args: Optional arguments to include in the output.
    """
    c = Colors
    output = f"{c.GREEN}[SUCC] {c.RESET}:: {scs}"
    if args:
        output += f": {args[0]}"
    print(output)


def print_aur_summary(pkg: PackageInfo) -> None:
    c = Colors
    print(
        f"{c.CYAN}{c.BOLD}aur explicit (1){c.RESET}: {pkg.package.name}-{pkg.package.version}"
    )

    if pkg.depends:
        deps = ", ".join(pkg.depends)
        print(f"{c.CYAN}{c.BOLD}dependencies ({len(pkg.depends)}){c.RESET}: {deps}")

    opt_depends = pkg.opt_depends or []
    if opt_depends:
        opt_deps = ", ".join(opt_depends)
        print(
            f"{c.CYAN}{c.BOLD}optional dependencies ({len(opt_depends)}){c.RESET}: {opt_deps}"
        )

    make_depends = pkg.make_depends or []
    if make_depends:
        make_deps = ", ".join(make_depends)
        print(
            f"{c.CYAN}{c.BOLD}make dependencies ({len(make_depends)}){c.RESET}: {make_deps}"
        )

    print_ask("proceed with installation?")


def print_pacman_summary(pkg: PacmanInfo) -> None:
    c = Colors
    sync_expl: str = (
        f"{c.CYAN}{c.BOLD}sync explicit (1){c.RESET}: {pkg.name}-{pkg.version}"
    )
    print(sync_expl)
    if pkg.depends:
        deps = ", ".join(pkg.depends)
        print(f"{c.CYAN}{c.BOLD}dependencies ({len(pkg.depends)}){c.RESET}: {deps}")

    opt_depends = pkg.opt_depends or []
    if opt_depends:
        opt_deps = ", ".join(opt_depends)
        print(
            f"{c.CYAN}{c.BOLD}optional dependencies ({len(opt_depends)}){c.RESET}: {opt_deps}"
        )

    print_ask("proceed with installation?")
