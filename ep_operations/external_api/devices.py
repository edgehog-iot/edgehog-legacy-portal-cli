import json
from typing import List

import requests

from ep_operations.auth import external_login as login
from ep_operations.auth import external_logout as logout
from ep_operations.common import get_authorized_headers
from ep_operations.external_api import gateways

GET_GW_V1_API = "{}/api/v1/management/devices"
List_string = List[str]


def get_devices(uri: str, user: str, password: str, device_id: str = None, hardware_id: str = None,
                tags: List_string = None):
    if tags is None:
        tags = []
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    endpoint = GET_GW_V1_API.format(uri)

    if device_id:
        endpoint += "/{}".format(device_id)

    params = {}

    if tags or hardware_id:
        filters = []
        if hardware_id:
            filters.append({
                "field": "gateway.hardware_id",
                "operator": "contains",
                "value": hardware_id
            })
        for tag in tags:
            filters.append({
                "field": "tags",
                "operator": "eq",
                "value": tag
            })
        if len(filters) > 0:
            params = {
                '$filter': '{"filters": ' + json.dumps(filters) + ', "logic": "and"}'
            }

    get_devices_api_request = requests.get(endpoint.format(uri), headers=headers, params=params)
    devices_dict = get_devices_api_request.json()

    if device_id:
        logout(uri, token)
        device = devices_dict.get("data")
        if device:
            return print(json.dumps(__clean_device(device)))
        else:
            return ""

    devices = []
    for device in devices_dict.get('rows', []):
        devices.append(__clean_device(device))

    logout(uri, token)
    return print(json.dumps(devices, indent=4))


def add_device(uri: str, user: str, password: str, gateway_id: int, model_id: int, serial_number: str, name: str,
               notes: str = None):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    body = {
        "gateway_id": gateway_id,
        "model_id": model_id,
        "serial_number": serial_number,
        "name": name,
        "notes": notes
    }

    req = requests.post(GET_GW_V1_API.format(uri), headers=headers, params=body)
    response = req.json()

    logout(uri, token)
    print(json.dumps(response))


def provision(uri: str, user: str, password: str, device_id: str, gateway_serial_number: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    url = GET_GW_V1_API + "/{}/provision".format(uri, device_id)
    headers = get_authorized_headers(token)
    body = {
        "device_serial_number": gateway_serial_number
    }

    req = requests.post(url=url, headers=headers, params=body)
    response = req.json()

    logout(uri, token)
    print(json.dumps(response))


def get_geolocation(uri: str, user: str, password: str, device_id: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    url = (GET_GW_V1_API + "/{}/geolocations?$orderby=created_at DESC&$top=1").format(uri, device_id)
    headers = get_authorized_headers(token)

    req = requests.get(url=url, headers=headers)
    response = req.json()

    if response.get('success') and response.get('rows') and len(response.get('rows')) > 0:
        ret = response.get('rows')[0]
        del ret['id']
        ret['success'] = True
    else:
        ret = response

    logout(uri, token)
    print(json.dumps(ret, indent=4))


def decommission(uri: str, user: str, password: str, device_id: str, device_serial_number: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    url = GET_GW_V1_API + "/{}/decommission".format(uri, device_id)
    headers = get_authorized_headers(token)
    body = {
        "serial_number": device_serial_number
    }

    req = requests.post(url=url, headers=headers, params=body)
    response = req.json()

    logout(uri, token)
    print(json.dumps(response))


def reinstall_os(uri: str, user: str, password: str, device_id: str, device_serial_number: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    url = GET_GW_V1_API + "/{}/reinstall-os".format(uri, device_id)
    headers = get_authorized_headers(token)
    body = {
        "serial_number": device_serial_number
    }

    req = requests.post(url=url, headers=headers, params=body)
    response = req.json()

    logout(uri, token)
    print(json.dumps(response))


def replace_gw(uri: str, user: str, password: str, device_id: str, device_serial_number: str, new_gw_id: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    url = GET_GW_V1_API + "/{}/replace-gateway".format(uri, device_id)
    headers = get_authorized_headers(token)
    body = {
        "serial_number": device_serial_number,
        "new:gateway_id": new_gw_id
    }

    req = requests.post(url=url, headers=headers, params=body)
    response = req.json()

    logout(uri, token)
    print(json.dumps(response))


def __clean_device(device: dict):
    dev = {
        "id": device.get("id"),
        "name": device.get("name"),
        "serial_number": device.get("serial_number"),
        "status": device.get("status"),
        "notes": device.get("notes"),
        "features": [],
        "tags": []
    }

    gateway = device.get("gateway")
    if gateway:
        dev["gateway"] = gateways.__clean_gateway(gateway)

    model = device.get("model")
    if model:
        dev["model"] = {
            "id": model.get("id"),
            "name": model.get("name"),
            "image": model.get("image")
        }

    features = device.get("features")
    for feature in features:
        dev["features"].append(feature)

    tags = device.get("tags")
    for tag in tags:
        dev["tags"].append(tag)

    return dev
