import json
from io import TextIOWrapper

import requests

from ep_operations.auth import external_login as login
from ep_operations.auth import external_logout as logout
from ep_operations.common import get_authorized_headers
from typing import List
from base64 import standard_b64encode

List_int = List[int]
List_string = List[str]

GET_APPS_V1_API = "{}/api/v1/production/applications"


def get_apps(uri: str, user: str, password: str, app_id: str = None):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    endpoint = GET_APPS_V1_API.format(uri)

    if app_id:
        endpoint = endpoint + "/{}".format(app_id)

    get_app_request = requests.get(endpoint.format(uri), headers=headers)
    apps_dict = get_app_request.json()

    if app_id:
        logout(uri, token)
        return print(json.dumps(__clean_app(apps_dict.get("data")), indent=4))

    apps = []
    for app in apps_dict.get("rows"):
        apps.append(__clean_app(app))

    logout(uri, token)
    print(json.dumps(apps, indent=4))


def add_app(uri: str, user: str, password: str, name: str, description: str, file: TextIOWrapper,
            gateway_model_ids: List_int, tags: List_string, start_on_install: bool = False):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    uri = GET_APPS_V1_API.format(uri)
    headers = get_authorized_headers(token)
    body = {
        "name": name,
        "description": description,
        "configuration_file": "data:text/yaml;base64," + standard_b64encode(file.read()).decode('utf-8'),
        "start_on_install": start_on_install,
        "gateway_models": [],
        "tags": tags
    }

    for gw_model_id in gateway_model_ids:
        body["gateway_models"].append({"id": gw_model_id})

    add_app_request = requests.post(uri, headers=headers, data=json.dumps(body))
    response = add_app_request.json()

    print(json.dumps(response))


def update_app(uri: str, user: str, password: str, name: str, description: str, file: TextIOWrapper,
               tags: List_string, app_id: str, start_on_install: bool = False):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    uri = (GET_APPS_V1_API + "/{}").format(uri, app_id)
    headers = get_authorized_headers(token)
    body = {
        "name": name,
        "description": description,
        "configuration_file": "data:text/yaml;base64," + standard_b64encode(file.read()).decode('utf-8'),
        "start_on_install": start_on_install,
        "tags": tags
    }

    add_app_request = requests.put(uri, headers=headers, data=json.dumps(body))
    response = add_app_request.json()

    print(json.dumps(response))


def __clean_app(app: dict):
    out = {
        "id": app.get("id"),
        "name": app.get("name"),
        "description": app.get("description"),
        "configuration_file": app.get("configuration_file"),
        "start_on_install": app.get("start_on_install") == 1,
        "tags": app.get("tags"),
        "gateway_models": []
    }

    models = app.get("gateway_models")

    for model in models:
        out["gateway_models"].append({
            "id": model.get("id"),
            "name": model.get("name"),
            "vendor": model.get("vendor")
        })

    return out
