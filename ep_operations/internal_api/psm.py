import json
import random
import requests
from io import TextIOWrapper

from ep_operations.auth import internal_login as login
from ep_operations.auth import internal_logout as logout
from ep_operations.common import get_authorized_headers

BINDING_API_V1 = "{}/iapi/v1/psm/sn-binding"
POST_BINDING_API_V1 = "{}/iapi/v1/psm/sn-binding/{}"
DEREGISTER_API_V1 = "{}/iapi/v1/gateways/deregister"


def binding(uri: str, user: str, password: str, company: str = None, hardware_id: str = None,
            gateway_serial_number: str = None, input_file: TextIOWrapper = None,
            output_file: TextIOWrapper = None, dryrun: bool = False):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    responses = []

    if hardware_id and gateway_serial_number:
        responses.append(__binding_request(uri, token, company, hardware_id, gateway_serial_number, dryrun))
    elif input_file:
        line = input_file.readline()
        while line:
            params = line.split(',')
            if len(params) == 3:
                responses.append(__binding_request(uri, token, params[2], params[0], params[1], dryrun))
            elif len(params) == 2:
                if not company:
                    print("--company parameter required if not present in input file")
                responses.append(__binding_request(uri, token, company, params[0], params[1], dryrun))
            else:
                print("{}: CSV line ill formatted".format(line))
                return
            line = input_file.readline()
        input_file.close()
    else:
        print("Error:\n[--hardware_id, --serial_number] or [--input, [--company]] "
              "required parameters for 'binding' operation")
        return

    if output_file:
        success = True
        for response in responses:
            json.dump(response, output_file, indent=4)
            # output_file.write(pprint.pformat(response, indent=4))
            success = success and response.get('success', False)
        output_file.close()
        print('{} operations elaborated'.format(len(responses)))
        if not success:
            print('Some error occurred. For more info see: {}.'.format(output_file.name))
    else:
        for response in responses:
            # pprint.pprint(response, indent=4)
            print(json.dumps(response, indent=4))

    logout(uri, token)


def deregister(uri: str, user: str, password: str, hardware_id: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    uri = DEREGISTER_API_V1.format(uri)
    headers = get_authorized_headers(token)
    body = {"hardware_id": hardware_id}

    deregister_request = requests.post(uri, headers=headers, data=body)
    response = deregister_request.json()

    logout(uri, token)
    print(json.dumps(response, indent=4))


def __binding_request(uri: str, token: str, company: str = None, hardware_id: str = None,
                      gateway_serial_number: str = None, dryrun: bool = False):
    binding_headers = get_authorized_headers(token)
    body = {
        "hardware_id": hardware_id,
        "device_serial_number": gateway_serial_number
    }
    if company:
        body["customer_code"] = company
    else:
        rnd1 = random.randint(100, 999)
        rnd2 = random.randint(100, 999)
        rnd3 = random.randint(100, 999)
        body["registration_code"] = "RC{}-{}-{}".format(rnd1,rnd2, rnd3)
    binding_request = requests.post(BINDING_API_V1.format(uri), headers=binding_headers, params=body)
    result = binding_request.json()
    if dryrun and result.get('success', False) and result.get('data'):
        __delete_binding_request(uri, token, result['data'].get('id'))

    try:
        return result
    except ValueError:
        return {}


def __delete_binding_request(uri: str, token: str, binding_id: int):
    binding_headers = get_authorized_headers(token)
    binding_request = requests.delete(POST_BINDING_API_V1.format(uri, binding_id), headers=binding_headers)
    response = binding_request.json()
    print("Gateway id {}: removed".format(binding_id))
    return response.get('success', False)
