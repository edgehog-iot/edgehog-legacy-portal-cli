import json

import requests

from ep_operations.auth import external_login as login
from ep_operations.auth import external_logout as logout
from ep_operations.common import get_authorized_headers

GET_GW_V1_API = "{}/api/v1/production/gateways"


def get_gateways(uri: str, user: str, password: str, unassociated: bool):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    endpoint = GET_GW_V1_API.format(uri)

    if unassociated:
        endpoint += "/unassociated"

    get_gateways_api_request = requests.get(endpoint.format(uri), headers=headers)
    gateways_dict = get_gateways_api_request.json()

    gateways = []
    for gateway in gateways_dict.get('rows', []):
        gateways.append(__clean_gateway(gateway))

    logout(uri, token)
    return print(json.dumps(gateways, indent=4))


def ssh_connect(uri: str, user: str, password: str, gw_id: int):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    endpoint = GET_GW_V1_API.format(uri) + "/{}/connect-ssh".format(gw_id)

    ssh_connect_api_request = requests.post(endpoint.format(uri), headers=headers)
    ssh_dict = ssh_connect_api_request.json()

    if ssh_dict.get('success') and ssh_dict.get('body') and ssh_dict.get('body').get('port'):
        body = ssh_dict.get('body')
        host = body.get("host")
        port = body.get("port")
        timeout = body.get("timeout")
        user = body.get("user")

        connection_string = 'ssh -f -L {}:127.0.0.1:{} {}@{} /bin/sleep 600 && ssh root@127.0.0.1 -o ' \
                            'IdentitiesOnly=yes -p {}'.format(port, port, user, host, port)
        ret = {
            'success': True,
            'connection_string': connection_string,
            'timeout': timeout
        }
    else:
        ret = ssh_dict

    return print(json.dumps(ret, indent=4))


def add_gateway(uri: str, user: str, password: str, registration_code: str, serial_number: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    if not registration_code or not serial_number:
        return print(json.dumps({
            "success": False,
            "message": "Either serialnumber and registrationcode are required to add a gatrway"
        }, indent=4))

    body = {
        "registration_code": registration_code,
        "serial_number": serial_number
    }

    req = requests.post(GET_GW_V1_API.format(uri), headers=headers, params=body)
    response = req.json()

    print(json.dumps(response))


def __clean_gateway(gateway: dict):
    new_gw = {
        "id": gateway.get("id"),
        "hardware_id": gateway.get("hardware_id"),
        "serial_number": gateway.get("serial_number"),
        "connected": gateway.get("connected"),
        "status": gateway.get("status"),
        "device_manager_version": gateway.get("device_manager_version"),
        "last_seen": gateway.get("last_seen"),
        "imei": gateway.get("imei"),
        "sim_card": gateway.get("id"),
    }

    model = gateway.get("model")
    if model:
        new_gw["model"] = {
            "id": model.get("id"),
            "vendor": model.get("id"),
            "name": model.get("id")
        }

    os = gateway.get("os")
    if os:
        new_gw["os"] = {
            "provisioning_status": os.get("provisioning_status")
        }

    device = gateway.get("device")
    if device:
        new_gw["device"] = {
            "id": device.get("id"),
            "serial_number": device.get("serial_number")
        }

    return new_gw
