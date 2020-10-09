import json
import requests

from typing import List
from ep_operations.auth import external_login as login
from ep_operations.auth import external_logout as logout
from ep_operations.common import get_authorized_headers

List_string = List[str]


def get_campaigns(uri: str, user: str, password: str, api_url: str, __clean_campaign, campaign_id: str = None):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    endpoint = api_url.format(uri)

    if campaign_id:
        endpoint += "/{}".format(campaign_id)

    get_oscamp_api_request = requests.get(endpoint.format(uri), headers=headers)
    campaigns_dict = get_oscamp_api_request.json()

    if campaign_id:
        logout(uri, token)
        campaign = campaigns_dict.get("data")
        if campaign:
            return print(json.dumps(__clean_campaign(campaign), indent=4))
        else:
            return ""

    campaigns = []
    for campaign in campaigns_dict.get('rows', []):
        campaigns.append(__clean_campaign(campaign))

    logout(uri, token)
    return print(json.dumps(campaigns, indent=4))


def add_campaign(uri: str, user: str, password: str, api_url: str, body: dict):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)
    endpoint = api_url.format(uri)

    add_oscamp_api_request = requests.post(endpoint.format(uri), headers=headers, json=body)
    res = add_oscamp_api_request.json()
    response = res
    if res.data:
        response = res.get("data")
        response["success"] = res.get("success")

    logout(uri, token)
    print(json.dumps(response, indent=4))


def start_cancel_campaign(uri: str, user: str, password: str, api_url: str, campaign_id: str, cancel: bool = False):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)
    operation = "cancel" if cancel else "start"

    endpoint = (api_url + "/{}/" + operation).format(uri, campaign_id)

    interact_oscamp_api_request = requests.post(endpoint.format(uri), headers=headers)
    response = interact_oscamp_api_request.json()

    logout(uri, token)
    print(json.dumps(response, indent=4))
