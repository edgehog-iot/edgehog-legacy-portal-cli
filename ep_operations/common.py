HEADERS = {"Accept": "application/json"}


def get_authorized_headers(token:str, content_type: str = "application/json"):
    authorized_headers = HEADERS.copy()
    authorized_headers['Authorization'] = 'Bearer {}'.format(token)
    authorized_headers['Content-Type'] = content_type
    return authorized_headers
