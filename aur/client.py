from typing import Any
from urllib.parse import quote as q

import requests

from common.types import Package, PackageInfo


class AURError(Exception):
    pass


def search(query: str) -> list[Package]:
    url: str = "https://aur.archlinux.org/rpc/v5/search/" + q(query)
    response: requests.Response = requests.get(url)
    try:
        data: dict[str, Any] = response.json()
    except requests.exceptions.JSONDecodeError as e:
        raise AURError(f"invalid response from aur: {e}")

    if data["type"] == "error":
        raise AURError(data["error"])

    packages: list[Package] = []
    for result in data["results"]:
        packages.append(
            Package(
                name=result["Name"],
                description=result["Description"],
                version=result["Version"],
                num_votes=result["NumVotes"],
                out_of_date=result["OutOfDate"],
            )
        )

    return packages


def fetch_info(query: str) -> PackageInfo:
    url = "https://aur.archlinux.org/rpc/v5/info?arg[]=" + q(query)
    response: requests.Response = requests.get(url)
    try:
        data: dict[str, Any] = response.json()
    except requests.exceptions.JSONDecodeError as e:
        raise AURError(f"invalid response from aur: {e}")
    if data["type"] == "error":
        raise AURError(data["error"])
    elif len(data["results"]) == 0:
        raise AURError("no results found")
    result: Package = Package(
        name=data["results"][0].get("Name", []),
        description=data["results"][0].get("Description", []),
        version=data["results"][0].get("Version", []),
        num_votes=data["results"][0].get("NumVotes", []),
        out_of_date=data["results"][0].get("OutOfDate", []),
    )
    return PackageInfo(
        package=result,
        depends=data["results"][0].get("Depends", []),
        make_depends=data["results"][0].get("MakeDepends", []),
        opt_depends=data["results"][0].get("OptDepends", []),
    )


if __name__ == "__main__":
    print(search("intellij-idea-community-edition"))
