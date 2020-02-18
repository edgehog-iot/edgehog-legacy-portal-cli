import requests
import pprint
from ep_operations.auth import login, logout
from ep_operations.common import get_authorized_headers
from ep_operations.operating_systems import get_oses_request

GET_COMPANIES_V1_API = "{}/iapi/v1/companies"
ADD_OS_V1_API = GET_COMPANIES_V1_API + "/{}/operating-systems"


def get_companies(uri: str, user: str, password: str, company_code: str = None):
    pprint.pprint(get_companies_request(uri, user, password, company_code), indent=4)


def get_companies_request(uri: str, user: str, password: str, company_code: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    params = {}
    if company_code is not None:
        params = {
            '$filter': "{ \"filters\": [ {\"field\": \"code\", \"operator\": \"eq\", \"value\": \"" + company_code +
                       "\"}],\"logic\": \"and\"}"
        }

    get_companies_api_request = requests.get(GET_COMPANIES_V1_API.format(uri), headers=headers, params=params)
    companies_dict = get_companies_api_request.json()

    companies = []
    for company in companies_dict.get('rows', []):
        companies.append({
            "id": company.get("id"),
            "code": company.get("code"),
            "name": company.get("name"),
            "active": company.get("active")
        })

    logout(uri, token)
    return companies


def add_os(uri: str, user: str, password: str, company_code: str, os_code_id: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    companies = get_companies_request(uri, user, password, company_code=company_code)
    if companies.__len__() != 1:
        print("{{ \"success\": false,"
              "\"message\":\"Error in company_code filter: expected 1 Company, {} found\"}}".format(companies.__len__()))
        return
    else:
        company_id = companies[0].get('id')

    oses = get_oses_request(uri, user, password, os_code_id)
    if oses.__len__() != 1:
        print("{{ \"success\": false,"
              "\"message\":\"Error in os_code filter: expected 1 OS, {} found\"}}".format(oses.__len__()))
        return
    else:
        os_id = oses[0].get('id')

    body = {
        "os_id": os_id
    }

    add_os_request = requests.post(ADD_OS_V1_API.format(uri, company_id), headers=headers, params=body)
    result = add_os_request.json()

    logout(uri, token)

    pprint.pprint(result, indent=4)


def get_os(uri: str, user: str, password: str, company_code: str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    companies = get_companies_request(uri, user, password, company_code=company_code)
    if companies.__len__() != 1:
        print("{ \"success\": false,"
              "\"message\":\"Error in company_code filter: expected 1 Company, {} found\"}".format(companies.__len__()))
        return
    else:
        company_id = companies[0].get('id')

    get_os_request = requests.get(ADD_OS_V1_API.format(uri, company_id), headers=headers)
    result = get_os_request.json()

    logout(uri, token)

    pprint.pprint(result, indent=4)
