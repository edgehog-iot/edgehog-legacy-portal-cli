#!/usr/bin/env python3

import sys
import requests
import pprint

from datetime import datetime
from ep_operations.auth import login, logout
from ep_operations.common import get_authorized_headers

OS_API_V1 = "{}/iapi/v1/operating-systems"
RELEASES_API_V1 = "{}/iapi/v1/operating-systems/{}/releases"


def get_oses(uri: str, user: str, password: str, code_id: str):
    pprint.pprint(get_oses_request(uri, user, password, code_id), indent=4)


def get_oses_request(uri: str, user: str, password: str, code_id: str):
    token = login(uri, user, password)
    params = {}
    if len(token) == 0:
        return

    if code_id is not None:
        params = {
            '$filter': "{ \"filters\": [ {\"field\": \"code_id\", \"operator\": \"eq\", \"value\": \"" + code_id +
                       "\"}],\"logic\": \"and\"}"
        }

    headers = get_authorized_headers(token)
    get_oses_api_request = requests.get(OS_API_V1.format(uri), headers=headers, params=params)
    oses_dict = get_oses_api_request.json()

    oses = []

    for os in oses_dict.get("rows", []):
        oses.append({
            "id": os.get("id"),
            "code_id": os.get("code_id"),
            "name": os.get("name"),
            "description": os.get("description"),
            "repository_url": os.get("repository_url")
        })

    logout(uri, token)
    return oses


def create_os(uri: str, user: str, password: str, name: str, description: str, repository_url: str, code_id: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    body = {
        "name": name,
        "code_id": code_id,
        "description": description,
        "repository_url": repository_url,
        "releases": []
    }

    create_oss_request = requests.post(OS_API_V1.format(uri), headers=headers, params=body)
    result = create_oss_request.json()

    pprint.pprint(result, indent=4)
    logout(uri, token)


def get_releases(uri: str, user: str, password: str, os_id: str, code_id: str):
    token = login(uri, user, password)
    params = {}
    if len(token) == 0:
        return

    if code_id is not None:
        oses = get_oses_request(uri, user, password, code_id)
        if oses.__len__() != 1:
            print("{{ \"success\": false,"
                  "\"message\":\"Error in code_id filter: expected 1 OS, {} found\"}}".format(oses.__len__()))
            return
        else:
            os_id = oses[0].get('id')

    headers = get_authorized_headers(token)
    get_releases_request = requests.get(RELEASES_API_V1.format(uri, os_id), headers=headers, params=params)
    releases_dict = get_releases_request.json()

    releases = []
    for release in releases_dict.get("rows"):
        releases.append({
            "id": release.get("id"),
            "version": release.get("version"),
            "changelog": release.get("changelog"),
            "delta_size": release.get("delta_size"),
            "release_date": release.get("release_date")
        })

    pprint.pprint(releases, indent=4)
    logout(uri, token)


def create_releases(uri: str, user: str, password: str, os_id: str, code_id: str, version: str, changelog: str,
                    delta_size: int, release_date: str, dryrun: bool = False):
    if not release_date:
        release_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    token = login(uri, user, password)
    if len(token) == 0:
        return

    if code_id is not None:
        oses = get_oses_request(uri, user, password, code_id)
        if oses.__len__() != 1:
            print("{{ 'success': false,"
                  "'message':'Error in code_id filter: expected 1 OS, {} found'}}".format(oses.__len__()))
            sys.exit(1)
        else:
            os_id = oses[0].get('id')
    elif os_id is None:
        print("{ \"success\": false,"
              "\"message\":\"No OS identifier found\"}")
        sys.exit(1)

    headers = get_authorized_headers(token)
    body = {
        "version": version,
        "changelog": changelog,
        "delta_size": delta_size,
        "release_date": release_date
    }

    create_release_request = requests.post(RELEASES_API_V1.format(uri, os_id), headers=headers, params=body)
    result = create_release_request.json()

    if dryrun and result.get('success', False):
        release_id = result.get('data', {id: None}).get('id')
        if release_id:
            delete_release_request = requests.delete((RELEASES_API_V1+"/{}").format(uri, os_id, release_id), headers=headers)
            delete_result = delete_release_request.json()
            result['dryrun_success'] = delete_result.get('success', False)

    pprint.pprint(result, indent=4)
    logout(uri, token)
