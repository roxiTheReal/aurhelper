# types_.py
from dataclasses import dataclass


@dataclass
class Package:
    name: str
    description: str
    version: str
    num_votes: int
    out_of_date: int | None


@dataclass
class PackageInfo:
    package: Package
    depends: list[str]
    make_depends: list[str] | None
    opt_depends: list[str] | None


@dataclass
class PacmanInfo:
    name: str
    version: str
    depends: list[str]
    opt_depends: list[str]
