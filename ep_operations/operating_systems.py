import requests
import pprint

from datetime import datetime
from ep_operations.auth import login, logout
from ep_operations.common import get_authorized_headers

OS_API_V1 = "{}/iapi/v1/operating-systems"
RELEASES_API_V1 = "{}/iapi/v1/operating-systems/{}/releases"


def get_oses(uri: str, user: str, password: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)
    get_oses_request = requests.get(OS_API_V1.format(uri), headers=headers)
    oses_dict = get_oses_request.json()

    oses = []

    for os in oses_dict.get("rows", []):
        oses.append({
            "id": os.get("id"),
            "name": os.get("name"),
            "description": os.get("description"),
            "repository_url": os.get("repository_url")
        })
    pprint.pprint(oses, indent=4)
    logout(uri, token)


def create_os(uri: str, user: str, password: str, name: str, description: str, repository_url: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    body = {
        "name": name,
        "description": description,
        "repository_url": repository_url,
        "releases": []
    }

    create_oss_request = requests.post(OS_API_V1.format(uri), headers=headers, params=body)
    result = create_oss_request.json()

    pprint.pprint(result, indent=4)
    logout(uri, token)


def get_releases(uri: str, user: str, password: str, os_id: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)
    get_releases_request = requests.get(RELEASES_API_V1.format(uri, os_id), headers=headers)
    releases_dict = get_releases_request.json()

    releases = []
    for release in releases_dict.get("rows"):
        releases.append({
            "id": release.get["id"],
            "version": release.get["release"],
            "changelog": release.get["changelog"],
            "delta_size": release.get["delta_size"],
            "release_date": release.get["release_date"]
        })

    pprint.pprint(releases, indent=4)
    logout(uri, token)


def create_releases(uri: str, user: str, password: str, os_id: str, version: str, changelog: str, delta_size: int,
                    release_date: str):
    if not release_date:
        release_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)
    body = {
        "version": version,
        "changelog": changelog,
        "delta_size": delta_size,
        "release_date": release_date
    }

    create_release_request = requests.post(RELEASES_API_V1.format(uri, os_id), headers=headers, params=body)
    result = create_release_request.json()

    pprint.pprint(result, indent=4)
    logout(uri, token)
