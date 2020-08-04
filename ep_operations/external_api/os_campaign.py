import json
import requests

from typing import List
from ep_operations.auth import external_login as login
from ep_operations.auth import external_logout as logout
from ep_operations.common import get_authorized_headers

GET_OSCAMP_V1_API = "{}/api/v1/management/os/campaigns"
List_string = List[str]


def get_os_campaigns(uri: str, user: str, password: str, campaign_id: str = None):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    endpoint = GET_OSCAMP_V1_API.format(uri)

    if campaign_id:
        endpoint += "/{}".format(campaign_id)

    get_oscamp_api_request = requests.get(endpoint.format(uri), headers=headers)
    campaigns_dict = get_oscamp_api_request.json()

    if campaign_id:
        logout(uri, token)
        campaign = campaigns_dict.get("data")
        if campaign:
            return print(json.dumps(__clean_campaign()))
        else:
            return ""

    campaigns = []
    for campaign in campaigns_dict.get('rows', []):
        campaigns.append(__clean_campaign(campaign))

    logout(uri, token)
    return print(json.dumps(campaigns, indent=4))


def add_campaign(uri: str, user: str, password: str, name: str, os_id: int, tags: List_string, timeout: int = 0,
                 rollout_rate: int = 0):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)
    endpoint = GET_OSCAMP_V1_API.format(uri)
    body = {
        "name": name,
        "timeout": timeout,
        "rollout_rate": rollout_rate,
        "os_id": os_id,
        "tags": tags
    }

    add_oscamp_api_request = requests.post(endpoint.format(uri), headers=headers, params = body)
    response = add_oscamp_api_request.json()

    logout(uri, token)
    print(json.dumps(response))


def start_cancel(uri: str, user: str, password: str, campaign_id: str, cancel: bool = False):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)
    operation = "cancel" if cancel else "start"

    endpoint = (GET_OSCAMP_V1_API+"/{}/" + operation).format(uri, campaign_id)

    interact_oscamp_api_request = requests.post(endpoint.format(uri), headers=headers)
    response = interact_oscamp_api_request.json()

    logout(uri, token)
    print(json.dumps(response))


def __clean_campaign(campaign: dict):
    out = {
        "id": campaign.get("id"),
        "job_id": campaign.get("job_id"),
        "name": campaign.get("name"),
        "status": campaign.get("status"),
        "tags": campaign.get("tags"),
        "started_at": campaign.get("started_at"),
        "completed_at": campaign.get("completed_at"),
        "numbers": campaign.get("numbers"),
        "gateways": [],
        "operating_system": campaign.get("operating_system")
    }

    gateways = campaign.get("gateways")
    for gateway in gateways:
        out["gateways"].append({
            "id": gateway.get("id"),
            "status": gateway.get("status"),
            "thing_name": gateway.get("thing_name"),
            "device_sn": gateway.get("device_sn"),
            "gateway_sn": gateway.get("gateway_sn"),
            "version": gateway.get("version"),
            "error": gateway.get("error"),
            "stdout": gateway.get("stdout"),
            "date": gateway.get("date"),
        })
    return out
