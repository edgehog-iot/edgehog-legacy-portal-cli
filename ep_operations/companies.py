import requests
import pprint
from ep_operations.auth import login
from ep_operations.common import get_authorized_headers

GET_COMPANIES_V1_API = "{}/iapi/v1/companies"


def get_companies(uri: str, user:str, password:str):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)
    get_companies_request = requests.get(GET_COMPANIES_V1_API.format(uri), headers=headers)
    companies_dict = get_companies_request.json()

    companies = []
    for company in companies_dict.get('rows', []):
        companies.append({
            "code": company.get("code"),
            "name": company.get("name"),
            "active": company.get("active")
        })

    pprint.pprint(companies, indent=4)
