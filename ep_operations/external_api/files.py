import json
import os
from io import TextIOWrapper

import requests

from ep_operations.auth import external_login as login
from ep_operations.auth import external_logout as logout
from ep_operations.common import get_authorized_headers
from typing import List
from base64 import standard_b64encode
from requests_toolbelt.multipart.encoder import MultipartEncoder

List_int = List[int]
List_string = List[str]

GET_FILES_V1_API = "{}/api/v1/production/files"


def get_files(uri: str, user: str, password: str, file_id: str = None):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    endpoint = GET_FILES_V1_API.format(uri)

    if file_id:
        endpoint = endpoint + "/{}".format(file_id)

    get_file_request = requests.get(endpoint.format(uri), headers=headers)
    files_dict = get_file_request.json()

    if file_id:
        logout(uri, token)
        return print(json.dumps(__clean_file(files_dict.get("data")), indent=4))

    files = []
    for file in files_dict.get("rows"):
        files.append(__clean_file(file))

    logout(uri, token)
    print(json.dumps(files, indent=4))


def get_file_verions(uri: str, user: str, password: str, file_id: str, version_id: str = None):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    endpoint = (GET_FILES_V1_API + "/{}/versions").format(uri, file_id)

    if version_id:
        endpoint = endpoint + "/{}".format(version_id)

    get_file_request = requests.get(endpoint.format(uri), headers=headers)
    files_dict = get_file_request.json()

    if version_id:
        logout(uri, token)
        return print(json.dumps(__clean_version(files_dict.get("data")), indent=4))

    files = []
    for file in files_dict.get("rows"):
        files.append(__clean_version(file))

    logout(uri, token)
    print(json.dumps(files, indent=4))


def add_file(uri: str, user: str, password: str, name: str, description: str, file: TextIOWrapper,
             file_description: str, remote_path: str, tags: List_string, inflate: bool = False, ack: bool = False):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    uri = GET_FILES_V1_API.format(uri)

    filename = os.path.basename(file.name)
    fields = [
        ("name", name),
        ("description", description),
        ("file[file]", (filename, file)),
        ("file[description]", file_description),
        ("file[inflate]", "1" if inflate else "0"),
        ("ack", "1" if ack else "0"),
        ("remote_path", remote_path),
    ]

    for tag in tags:
        fields.append(("tags[]", tag))

    mp_encoder = MultipartEncoder(
        fields=fields
    )

    headers = get_authorized_headers(token, content_type=mp_encoder.content_type)

    add_file_request = requests.post(uri, headers=headers, data=mp_encoder)
    response = add_file_request.json()

    print(json.dumps(response))


def add_version(uri: str, user: str, password: str, file_id: str, file: TextIOWrapper, file_description: str,
                inflate: bool = False):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    uri = (GET_FILES_V1_API + "/{}/versions").format(uri, file_id)

    filename = os.path.basename(file.name)
    fields = [
        ("file", (filename, file)),
        ("description", file_description),
        ("inflate", "1" if inflate else "0"),
    ]

    mp_encoder = MultipartEncoder(
        fields=fields
    )

    headers = get_authorized_headers(token, content_type=mp_encoder.content_type)

    add_file_request = requests.post(uri, headers=headers, data=mp_encoder)
    response = add_file_request.json()

    print(json.dumps(response))


def __clean_file(file: dict):
    out = {
        "id": file.get("id"),
        "name": file.get("name"),
        "description": file.get("description"),
        "remote_path": file.get("remote_path"),
        "ack": file.get("ack"),
        "tags": file.get("tags"),
        "versions": []
    }

    versions = file.get("versions")

    for version in versions:
        out["versions"].append(__clean_version(version))

    return out


def __clean_version(version: dict):
    return {
        "id": version.get("id"),
        "description": version.get("description"),
        "file": version.get("file"),
        "md5": version.get("md5"),
        "file_name": version.get("file_name"),
        "version": version.get("version"),
        "inflate": version.get("inflate")
    }
