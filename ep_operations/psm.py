import requests
import pprint

from ep_operations.auth import login
from ep_operations.common import get_authorized_headers

BINDING_API_V1 = "{}/iapi/v1/psm/sn-binding"
POST_BINDING_API_V1 = "{}/iapi/v1/psm/sn-binding/{}"


def binding(uri: str, user: str, password: str, company: str = None, hardware_id: str = None,
            gateway_serial_number: str = None, input_file = None, output_file = None,
            dryrun: bool = False):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    responses = []

    if hardware_id and gateway_serial_number and company:
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
        print("Error:\n[--hardware_id, --serial_number, --company] or [--input, [--company]] "
              "required parameters for 'binding' operation")
        return

    if output_file:
        success = True
        for response in responses:
            output_file.write(pprint.pformat(response, indent=4))
            success = success and response.get('success', False)
        output_file.close()
        print('{} operations elaborated'.format(len(responses)))
        if not success:
            print('Some error occurred. For more info see: {}.'.format(output_file.name))
    else:
        for response in responses:
            pprint.pprint(response, indent=4)


def __binding_request(uri: str, token: str, company: str = None, hardware_id: str = None,
                      gateway_serial_number: str = None, dryrun: bool = False):
    binding_headers = get_authorized_headers(token)
    body = {
        "hardware_id": hardware_id,
        "gateway_serial_number": gateway_serial_number,
        "customer_code": company
    }
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

    return response.get('success', False)
