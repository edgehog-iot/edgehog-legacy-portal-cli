import json
import requests

from typing import List
from ep_operations.auth import external_login as login
from ep_operations.auth import external_logout as logout
from ep_operations.common import get_authorized_headers
from ep_operations.external_api.campaigns import get_campaigns, add_campaign, start_cancel_campaign

GET_OSCAMP_V1_API = "{}/api/v1/management/applications/campaigns"
List_string = List[str]


def get_app_campaigns(uri: str, user: str, password: str, campaign_id: str = None):
    get_campaigns(uri, user, password, GET_OSCAMP_V1_API, __clean_campaign, campaign_id)


def add(uri: str, user: str, password: str, name: str, app_id: int, tags: List_string, operation: str,
        timeout: int = 30, rollout_rate: int = 5):
    body = {
        "name": name,
        "timeout": timeout,
        "operation":operation,
        "rollout_rate": rollout_rate,
        "application_id": app_id,
        "tags": tags
    }

    add_campaign(uri, user, password, GET_OSCAMP_V1_API, body)


def start_cancel(uri: str, user: str, password: str, campaign_id: str, cancel: bool = False):
    start_cancel_campaign(uri, user, password, GET_OSCAMP_V1_API, campaign_id, cancel)


def __clean_campaign(campaign: dict):
    out = {
        "id": campaign.get("id"),
        "name": campaign.get("name"),
        "status": campaign.get("status"),
        "job_id": campaign.get("job_id"),
        "operation": campaign.get("operation"),
        "tags": campaign.get("tags"),
        "started_at": campaign.get("started_at"),
        "completed_at": campaign.get("completed_at"),
        "numbers": campaign.get("numbers"),
        "gateways": [],
        "application": campaign.get("application")
    }

    gateways = campaign.get("gateways")
    for gateway in gateways:
        out["gateways"].append({
            "id": gateway.get("id"),
            "status": gateway.get("status"),
            "thing_name": gateway.get("thing_name"),
            "device_sn": gateway.get("device_sn"),
            "gateway_sn": gateway.get("gateway_sn"),
            "error": gateway.get("error"),
            "stdout": gateway.get("stdout"),
            "date": gateway.get("date"),
        })

    return out
