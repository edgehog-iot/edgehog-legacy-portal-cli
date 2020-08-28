import json

import requests

from ep_operations.auth import external_login as login
from ep_operations.auth import external_logout as logout
from ep_operations.common import get_authorized_headers

GET_MODELS_V1_API = "{}/api/v1/management/os"


def get_oses(uri: str, user: str, password: str, os_id: str = None):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    endpoint = GET_MODELS_V1_API.format(uri)

    if os_id:
        endpoint += "/{}".format(os_id)

    get_models_api_request = requests.get(endpoint.format(uri), headers=headers)
    models_dict = get_models_api_request.json()

    if os_id:
        logout(uri, token)
        return print(json.dumps(__clean_os(models_dict.get("data")), indent=4))

    models = []
    for model in models_dict.get('rows', []):
        models.append(__clean_os(model))

    logout(uri, token)
    print(json.dumps(models, indent=4))


def __clean_os(os: dict):
    if not os:
        return {}

    out = {
      "id": os.get("id"),
      "name": os.get("name"),
      "description": os.get("description"),
      "repository_url": os.get("repository_url"),
      "releases": []
    }

    releases = os.get("releases")
    for release in releases:
        out["releases"].append({
          "id": release.get("id"),
          "version": release.get("version"),
          "changelog": release.get("changelog"),
          "delta_size": release.get("delta_size"),
          "release_date": release.get("release_date")
        })

    return out
